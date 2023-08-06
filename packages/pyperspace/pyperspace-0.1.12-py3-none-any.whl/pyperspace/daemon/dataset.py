from pyperspace.storage import LSMDataSet
from pyperspace.workers import DataSetWorkerPool
from pyperspace.data import Entry, sort_readers
from typing import Iterable, Optional, Tuple

class HybridDataSet:
    def __init__(self, dswp: DataSetWorkerPool, name: str, sm_port: int):
        self._dswp = dswp
        self._name = name
        self._storage = LSMDataSet(name, sm_port)

    def close(self) -> None:
        self._storage.close()

    def delete(self, begin_time: int, end_time: int) -> None:
        self._storage.delete(begin_time, end_time)
        self._dswp.send_delete(self._name, begin_time, end_time)
    
    def find_range(self, begin_time: int, end_time: int) -> Iterable[Entry]:
        s = self._storage.find_range(begin_time, end_time)
        l = self._dswp.send_select(self._name, begin_time, end_time)
        return sort_readers([iter(l), iter(s)])

    def find_all(self) -> Iterable[Entry]:
        s = self._storage.find_all()
        l = self._dswp.send_select_all(self._name)
        return sort_readers([l, s])

    @property
    def stats(self) -> Tuple[Optional[int], Optional[int], int]:
        def get_value(a: Optional[int], b: Optional[int], op) -> Optional[int]:
            if a is not None and b is not None:
                return op(a, b)
            elif a is not None:
                return a
            elif b is not None:
                return b
            else:
                return None
            
        l = self._dswp.send_stats_request(self._name)
        s = self._storage.stats
        num_entries = l[2] + s[2]
        begin_time = get_value(l[0], s[0], min)
        end_time = get_value(l[1], s[1], max)
        return begin_time, end_time, num_entries
