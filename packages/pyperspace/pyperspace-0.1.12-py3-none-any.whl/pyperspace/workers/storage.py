from pyperspace.networking import TCPMessageSocket, TCPListener
from pyperspace.data import IntervalMap
from pyperspace.storage import LSMFileReader, DeletionMap, wal_to_lsm, StorageManagerClient, LSMFileMerger
from pyperspace.protocol.storage import Request, Response, AddRequest, DropRequest, OpenRequest, CloseRequest, \
                                        SelectRangeRequest, SelectAllRequest, ExitRequest, DeleteRequest, \
                                        PersistRequest, ShutdownRequest, TimeRange, DropDataSetRequest, \
                                        ListDataSetsRequest, DataSetStatsRequest

from collections import defaultdict, deque
from typing import Any, Iterable, Optional, Tuple, Deque
from pathlib import Path

import io
import os
import multiprocessing
import threading
import time
import logging
import shutil

LOG = logging.getLogger(__name__)

_spawn_lock = threading.Lock()
_merge_lock = multiprocessing.Lock()

def spawn(fn, args) -> None:
    p = None
    try:
        # https://stackoverflow.com/questions/62276345/call-to-pythons-mutliprocessing-process-join-fails
        with _spawn_lock:
            p = multiprocessing.Process(target=fn, args=args)
            p.start()
    finally:
        p.join()
        with _spawn_lock:
            if p: p.close()

class FileNode:
    __slots__ = ('filename', 'begin_time', 'end_time', 'num_entries')
    def __init__(self, filename: str, begin_time: int, end_time: int, num_entries: int):
        self.filename = filename
        self.begin_time = begin_time
        self.end_time = end_time
        self.num_entries = num_entries

    def __eq__(self, n) -> bool:
        return self.filename == n.filename \
                and self.begin_time == n.begin_time \
                and self.end_time == n.end_time

    def __hash__(self) -> int:
        return hash(self.filename)

    @staticmethod
    def from_lsm_file(filename: str):
        rd = LSMFileReader(filename)
        try:
            return FileNode(filename, rd.header.begin_time, rd.header.end_time, rd.header.num_entries)
        finally:
            rd.close()


class StorageData:
    def __init__(self, wal_path: str):
        self._path = wal_path
        self._files = IntervalMap()
        self._deletes = DeletionMap(wal_path)
        self._fns = dict()
        self._next_lsm_file = 0
        self._next_lsm_file_lock = threading.Lock()
        self._num_entries = 0
        self._removed = False

    @property
    def is_removed(self) -> bool:
        return self._removed

    def close(self) -> None:
        self._deletes.close()

    def drop(self) -> None:
        self.close()
        shutil.rmtree(self._path)
        self._removed = True

    @property
    def stats(self) -> Tuple[Optional[int], Optional[int], int]:
        return self._files.min_time, self._files.max_time, self._num_entries

    def merge(self, delete_list: Deque[str]) -> bool:
        wal_fn = self._deletes.filename
        del_queue = list(self._fns.keys())
        
        # Do nothing if single file and no deletions
        if len(del_queue) < 2 or (len(del_queue) == 1 and not self._deletes.empty):
            return False

        state_file = os.path.join(self._path, 'state.dat')
        lsm_file, new_file = self._get_next_lsm_file("data", "merge")
        while True:
            with _merge_lock:
                try:
                    LOG.info(f"beginning merge: {lsm_file}")
                    with open(state_file, 'w') as fd:
                        fd.write('merging')
                    m = LSMFileMerger(lsm_file)
                    try:
                        # Swap out old deletion WAL for new one
                        m.add_deletion_range(self._deletes.map)

                        # For all filenames, and delete map, merge into new files
                        for fn in del_queue: m.add_lsm_file(fn)
                        m.merge(validate=False)   # TODO: make configurable
                    finally:
                        m.close()
                        if new_file:
                            os.rename(lsm_file, new_file)
                            LOG.info(f"merge complete: {new_file}")
                        else:
                            LOG.info(f"merge complete: {lsm_file}")
                        with open(state_file, 'w') as fd:
                            fd.write('delete-pending')
                    self._deletes.reset()
                    break
                except:
                    LOG.exception(f"merge failed: {lsm_file}")
        
        # Add back
        # TODO: fix this to not erase self._files
        self._files = IntervalMap()
        self._num_entries = 0
        for fn in del_queue: self._fns.pop(fn, None)
        if new_file:
            self.add(FileNode.from_lsm_file(new_file))
        else:
            self.add(FileNode.from_lsm_file(lsm_file))

        # Mark old ones for deletion
        delete_list.extend(del_queue)
        delete_list.append(wal_fn)
        delete_list.append(state_file)
        return True

    def delete(self, begin_time: int, end_time: int, flush: bool) -> None:
        self._deletes.insert(begin_time, end_time, flush)

    def get_deletion_range(self, begin_time: int = None, end_time: int = None) -> Iterable[Tuple[int, int]]:
        if begin_time is not None and end_time is not None:
            return self._deletes.map.range(begin_time, end_time)
        else:
            return iter(self._deletes.map)

    def remove(self, fn: str) -> bool:
        fn = os.path.abspath(fn)
        n = self._fns.get(fn)
        if n:
            del self._fns[fn]
            self._files.remove(n.begin_time, n.end_time, n)
            return True
        else:
            return False

    def select(self, begin_time: int, end_time: int) -> Iterable[FileNode]:
        return self._files[begin_time:end_time]
    
    def select_all(self) -> Iterable[FileNode]:
        return (f for f in self._files.values())

    def add(self, n: FileNode) -> bool:
        fn = os.path.abspath(n.filename)
        if fn not in self._fns:
            self._fns[fn] = n
            self._files.insert(n.begin_time, n.end_time, n)
            self._num_entries += n.num_entries
            return True
        else:
            return False

    def persist(self, wal_file: str) -> None:
        lsm_file, _ = self._get_next_lsm_file("data")

        # Convert WAL to LSM
        spawn(wal_to_lsm, (wal_file, lsm_file))
        # TODO: throw if spawn fails
        self.add(FileNode.from_lsm_file(lsm_file))
    
    def _get_next_lsm_file(self, check_prefix: str, name_prefix: Optional[str] = None) -> Tuple[str, Optional[str]]:
        with self._next_lsm_file_lock:
            c = self._next_lsm_file
            path = Path(self._path)
            lsm_file = path / f"{check_prefix}_{c:06d}.dat"
            while lsm_file.exists():
                c += 1
                lsm_file = path / f"{check_prefix}_{c:06d}.dat"
            if name_prefix:
                lsm_file = path / f"{name_prefix}_{c:06d}.dat"
            lsm_file.touch()
            self._next_lsm_file = c+1
            if name_prefix:
                return str(lsm_file), str(path / f"{check_prefix}_{c:06d}.dat")
            else:
                return str(lsm_file), None

class OpenFileTable:
    def __init__(self):
        self._fns = dict()

    def is_open(self, fn: str) -> bool:
        return self._fns.get(fn, 0) != 0

    def open(self, fn: str) -> None:
        with open(fn, 'rb') as fd:
            if fn not in self._fns:
                self._fns[fn] = 1
            else:
                self._fns[fn] += 1

    def close(self, fn: str) -> bool:
        c = self._fns.get(fn)
        closed = False
        if c is not None:
            if c > 1:
                self._fns[fn] = c-1
            else:
                del self._fns[fn]
                closed = True
        else:
            closed = True
        return closed



class FileStorage:
    def __init__(self):
        self._names = dict()
        self._deletes = deque()
        self._merge_loop = list()
        self._next_merge = 0

    @property
    def count(self) -> int:
        return len(self._names)

    def stats(self, name: str) -> Tuple[Optional[int], Optional[int], int]:
        fname = name.lower()
        sd = self._names.get(fname)
        if sd: return sd.stats
        return None, None, 0
        #else: raise KeyError(f"dataset \"{name}\" not found")

    def drop(self, name: str) -> None:
        fname = name.lower()
        sd = self._names.get(fname)
        if sd:
            sd.drop()
            self._names.pop(fname)

    def delete_cycle(self, oft: OpenFileTable) -> int:
        _deletes = self._deletes
        dels, total = 0, len(_deletes)
        for _ in range(total):
            fn = _deletes.popleft()
            if oft.is_open(fn):
                _deletes.append(fn)
            else:
                try:
                    os.unlink(fn)
                    dels += 1
                except:
                    _deletes.append(fn)
                    LOG.exception(f"could not delete {fn}")
        return dels


    def merge_cycle(self) -> int:
        _merge_loop = self._merge_loop
        m, c = 0, len(_merge_loop)
        if c == 0:
            return 0

        _next_merge = self._next_merge
        if _next_merge >= c:
            _next_merge = c-1

        sd = _merge_loop[_next_merge]
        if sd.is_removed:
            _merge_loop.pop(_next_merge)
        elif sd.merge(self._deletes):
            m = 1

        if _next_merge == 0:
            self._next_merge = c-1
        else:
            self._next_merge = _next_merge-1

        return m

    def names(self) -> Iterable[str]:
        return self._names.keys()

    def init(self, name: str, path: str) -> StorageData:
        name = name.lower()
        sd = StorageData(path)
        self._names[name] = sd
        for filename in os.listdir(path):
            if filename.startswith("data_") and filename.endswith(".dat"):
                full_fn = os.path.join(path, filename)
                sd.add(FileNode.from_lsm_file(full_fn))
        self._merge_loop.append(sd)
        return sd

    def delete(self, name: str, begin_time: int, end_time: int) -> None:
        fname = name.lower()
        sd = self._names.get(fname)
        if sd: sd.delete(begin_time, end_time, True)
        else: raise KeyError(f"dataset \"{name}\" not found")

    def persist(self, name: str, wal_file: str) -> None:
        name = name.lower()
        sd = self._names.get(name)
        if sd is None:
            sd = StorageData(os.path.dirname(wal_file))
            self._names[name] = sd
            self._merge_loop.append(sd)
        sd.persist(wal_file)

    def add(self, name: str, lsm_file: str) -> None:
        fname = name.lower()
        sd = self._names.get(fname)
        if sd is None:
            sd = StorageData(os.path.dirname(wal_file))
            self._names[fname] = sd
            self._merge_loop.append(sd)
        if not sd.add(FileNode.from_lsm_file(lsm_file)):
            raise KeyError(f"LSM file \"{lsm_file}\" already added to dataset \"{name}\"")

    def select(self, name: str, begin_time: int, end_time: int) -> Iterable[FileNode]:
        fname = name.lower()
        sd = self._names.get(fname)
        if sd: yield from sd.select(begin_time, end_time)
        #else: raise KeyError(f"dataset \"{name}\" not found")
    
    def select_all(self, name: str) -> Iterable[FileNode]:
        fname = name.lower()
        sd = self._names.get(fname)
        if sd: yield from sd.select_all()
        #else: raise KeyError(f"dataset \"{name}\" not found")

    def remove(self, name: str, lsm_file: str) -> None:
        fname = name.lower()
        sd = self._names.get(fname)
        if sd: sd.remove(lsm_file)
        else: raise KeyError(f"dataset \"{name}\" not found")
    
    def get_deletion_range(self, name: str, begin_time: int = None, end_time: int = None) -> None:
        fname = name.lower()
        sd = self._names.get(fname)
        if sd: yield from sd.get_deletion_range(begin_time, end_time)
        #else: raise KeyError(f"dataset \"{name}\" not found")


class StorageManager:
    def __init__(self, data_dir):
        self._data_dir = data_dir
        self._files = FileStorage()
        self._fds = OpenFileTable()
        self._handler_map = {
            "Add": lambda c, rq, rs: self._handle_add(c, rq.Add, rs),
            "Drop": lambda c, rq, rs: self._handle_drop(c, rq.Drop, rs),
            "Persist": lambda c, rq, rs: self._handle_persist(c, rq.Persist, rs),
            "SelectRange": lambda c, rq, rs: self._handle_select_range(c, rq.SelectRange, rs),
            "SelectAll": lambda c, rq, rs: self._handle_select_all(c, rq.SelectAll, rs),
            "Open": lambda c, rq, rs: self._handle_open(c, rq.Open, rs),
            "Close": lambda c, rq, rs: self._handle_close(c, rq.Close, rs),
            "Exit": lambda c, rq, rs: self._handle_exit(c, rq.Exit, rs),
            "Shutdown": lambda c, rq, rs: self._handle_shutdown(c, rq.Shutdown, rs),
            "Delete": lambda c, rq, rs: self._handle_delete(c, rq.Delete, rs),
            "DropDataSet": lambda c, rq, rs: self._handle_drop_dataset(c, rq.DropDataSet, rs),
            "ListDataSets": lambda c, rq, rs: self._handle_list_datasets(c, rq.ListDataSets, rs),
            "DataSetStats": lambda c, rq, rs: self._handle_dataset_stats(c, rq.DataSetStats, rs),
        }
        self._load_datasets()

    def _load_datasets(self) -> None:
        _data_dir = self._data_dir
        _files = self._files
        try:
            for filename in os.listdir(_data_dir):
                try:
                    ds_dir = os.path.join(_data_dir, filename)
                    with open(os.path.join(ds_dir, 'name.dat'), 'r') as fd:
                        name = fd.read().rstrip()
                        _files.init(name, ds_dir)
                except:
                    LOG.exception(f"failed to load dataset node \"{filename}\"")
        except:
            LOG.exception(f"failed to load dataset directory \"{_data_dir}\"")

    def _handle_error(self, client: TCPMessageSocket, req: Request, res: Response) -> bool:
        res.Error.SetInParent()
        res.Error.error = f"invalid request type \"{req.WhichOneof('RequestType')}\""
        return False
    
    def _handle_exit(self, client: TCPMessageSocket, req: ExitRequest, res: Response) -> bool:
        res.Ack.SetInParent()
        return False
    
    def _handle_shutdown(self, client: TCPMessageSocket, req: ShutdownRequest, res: Response) -> bool:
        res.Ack.SetInParent()
        self._stop()
        return False
    
    def _handle_drop_dataset(self, client: TCPMessageSocket, req: DropDataSetRequest, res: Response) -> bool:
        try:
            self._files.drop(req.name)
            res.Ack.SetInParent()
        except Exception as e:
            LOG.exception("DropDataSetRequest failed")
            res.Error.SetInParent()
            res.Error.error = str(e.args[0])
        return True
    
    def _handle_list_datasets(self, client: TCPMessageSocket, req: ListDataSetsRequest, res: Response) -> bool:
        try:
            res.DataSets.SetInParent()
            res.DataSets.names.extend(self._files.names())
        except Exception as e:
            LOG.exception("ListDataSetsRequest failed")
            res.Error.SetInParent()
            res.Error.error = str(e.args[0])
        return True
    
    def _handle_dataset_stats(self, client: TCPMessageSocket, req: DataSetStatsRequest, res: Response) -> bool:
        try:
            res.DataSetStats.SetInParent()
            begin_time, end_time, num_entries = self._files.stats(req.name)
            res.DataSetStats.num_entries = num_entries
            if begin_time is not None: res.DataSetStats.begin_time = begin_time
            if end_time is not None: res.DataSetStats.end_time = end_time
        except Exception as e:
            LOG.exception("DataSetStatsRequest failed")
            res.Error.SetInParent()
            res.Error.error = str(e.args[0])
        return True
    
    def _handle_add(self, client: TCPMessageSocket, req: AddRequest, res: Response) -> bool:
        try:
            self._files.add(req.name, req.lsm_file)
            res.Ack.SetInParent()
        except Exception as e:
            LOG.exception("AddRequest failed")
            res.Error.SetInParent()
            res.Error.error = str(e.args[0])
        return True

    def _handle_drop(self, client: TCPMessageSocket, req: DropRequest, res: Response) -> bool:
        try:
            self._files.remove(req.name, req.lsm_file)
            res.Ack.SetInParent()
        except Exception as e:
            LOG.exception("DropRequest failed")
            res.Error.SetInParent()
            res.Error.error = str(e.args[0])
        return True

    def _handle_persist(self, client: TCPMessageSocket, req: PersistRequest, res: Response) -> bool:
        try:
            self._files.persist(req.name, req.wal_file)
            res.Ack.SetInParent()
        except Exception as e:
            LOG.exception("PersistRequest failed")
            res.Error.SetInParent()
            res.Error.error = str(e.args[0])
        return True

    def _handle_select_range(self, client: TCPMessageSocket, req: SelectRangeRequest, res: Response) -> bool:
        try:
            res.Select.SetInParent()
            files = res.Select.files
            fn_set = set()
            deletion_ranges = res.Select.deletion_ranges
            fn_set.update(node.filename for node in self._files.select(req.name, req.begin_time, req.end_time))
            files.extend(fn_set)
            for begin_time, end_time in self._files.get_deletion_range(req.name, begin_time=req.begin_time, end_time=req.end_time):
                t = TimeRange()
                t.begin_time = begin_time
                t.end_time = end_time
                deletion_ranges.append(t)
        except Exception as e:
            LOG.exception("SelectRangeRequest failed")
            res.Error.SetInParent()
            res.Error.error = str(e.args[0])
        return True
    
    def _handle_select_all(self, client: TCPMessageSocket, req: SelectAllRequest, res: Response) -> bool:
        try:
            res.Select.SetInParent()
            files = res.Select.files
            fn_set = set()
            deletion_ranges = res.Select.deletion_ranges
            fn_set.update(node.filename for node in self._files.select_all(req.name))
            files.extend(fn_set)
            for begin_time, end_time in self._files.get_deletion_range(req.name):
                t = TimeRange()
                t.begin_time = begin_time
                t.end_time = end_time
                deletion_ranges.append(t)
        except Exception as e:
            LOG.exception("SelectAllRequest failed")
            res.Error.SetInParent()
            res.Error.error = str(e.args[0])
        return True

    def _handle_open(self, client: TCPMessageSocket, req: OpenRequest, res: Response) -> bool:
        try:
            for name in req.lsm_names:
                self._fds.open(name)
            res.Ack.SetInParent()
        except Exception as e:
            LOG.exception("OpenRequest failed")
            res.Error.SetInParent()
            res.Error.error = str(e.args[0])
        return True

    def _handle_close(self, client: TCPMessageSocket, req: CloseRequest, res: Response) -> bool:
        try:
            for name in req.lsm_names:
                self._fds.close(name)
            # TODO: if closed, signal compactor
            res.Ack.SetInParent()
        except Exception as e:
            LOG.exception("CloseRequest failed")
            res.Error.SetInParent()
            res.Error.error = str(e.args[0])
        return True

    def _handle_delete(self, client: TCPMessageSocket, req: DeleteRequest, res: Response) -> bool:
        try:
            self._files.delete(req.name, req.begin_time, req.end_time)
            res.Ack.SetInParent()
        except Exception as e:
            LOG.exception("DeleteRequest failed")
            res.Error.SetInParent()
            res.Error.error = str(e.args[0])
        return True

    def _start_compactor(self, delay: int) -> None:
        self._compactor = threading.Thread(target=self._compactor_worker, args=(delay,), daemon=True)
        # TODO: event for killing thread
        self._compactor.start()

    def _compactor_worker(self, delay: int) -> None:
        _merge_cycle = self._files.merge_cycle
        _delete_cycle = self._files.delete_cycle
        _fds = self._fds
        while not self._shutdown:
            time.sleep(delay)
            for _ in range(self._files.count):
                # periodically compact LSM files, remove from selectable list.
                # if file was compacted, when last closed, move to delete queue.
                num_merged = _merge_cycle()
                # delete from delete queue
                _delete_cycle(_fds)

    def _stop(self) -> None:
        self._shutdown = True
        self._listener.close()
        # TODO: figure out why accept() blocks even when closed
        client = StorageManagerClient(self._listener.port)
        try:
            client.send_exit()
        finally:
            client.close()
        self._compactor.join()

    def run(self, q: multiprocessing.Queue, compactor_delay_sec: int) -> None:
        self._shutdown = False
        self._start_compactor(compactor_delay_sec)

        self._listener = TCPListener(True)
        listener = self._listener
        listener.open()
        q.put(listener.port)
        try:
            while not self._shutdown:
                s = listener.accept()
                self._run_client(s)
                # TODO: handle better, cap connections
                #threading.Thread(target=self._run_client, args=(s,), daemon=True).start()
        except KeyboardInterrupt:
            pass
        finally:
            if not self._shutdown:
                listener.close()

    def _run_client(self, client: TCPMessageSocket) -> None:
        try:
            req, res = Request.FromString(client.recv_msg()), Response()
            self._handler_map.get(req.WhichOneof("RequestType"), self._handle_error)(client, req, res)
            client.send_msg(res.SerializeToString())
        finally:
            client.close()

class StorageManagerWorker:
    def __init__(self, data_dir: str, compactor_cycle_sec: int):
        self._listener_port = None
        self._q = multiprocessing.Queue()
        self._data_dir = data_dir
        self._compactor_cycle_sec = compactor_cycle_sec

    @property
    def listener_port(self) -> int:
        return self._listener_port

    def _run(self, q: multiprocessing.Queue) -> None:
        sm = StorageManager(self._data_dir)
        sm.run(q, self._compactor_cycle_sec)

    def start(self) -> None:
        # TODO: handle better
        self._listener_port = None
        self._proc = multiprocessing.Process(target=self._run, args=(self._q,))
        self._proc.start()
        self._listener_port = self._q.get()

    def stop(self) -> None:
        client = StorageManagerClient(self._listener_port)
        client.send_shutdown()
        client.close()

    def join(self) -> None:
        self._proc.join(timeout=None)

    def close(self) -> None:
        if self._proc:
            self.join()
            self._proc.close()
