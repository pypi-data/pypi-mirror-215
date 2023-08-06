from pyperspace import Daemon, Config
from pyperspace.data import Entry, NamedEntry
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import logging

LOG = logging.getLogger(__name__)

def _to_nanoseconds(value: Union[datetime, int]) -> int:
    try:
        # Assume it's an int
        return int(value)
    except:
        # Otherwise it's a datetime...
        return int(value.timestamp() * 1000000000)

def datetime_from_nanoseconds(ns: int) -> datetime:
    return datetime.fromtimestamp(ns / 1000000000)

class DataEntry(BaseModel):
    time: Union[int, datetime]
    data: bytes

class NamedDataEntry(DataEntry):
    name: str

def generate_api(cfg: Config) -> FastAPI:
    tags = [
        {"name":"datasets","description":"Dataset operations"},
        {"name":"data","description":"Operations on data within a dataset"},
    ]
    app = FastAPI(title="Pyperspace Frontend", version="0.1.13", docs_url="/", openapi_tags=tags)
    db = Daemon(cfg.data_dir, cfg.datasets, cfg.storage)

    @app.on_event("startup")
    async def startup():
        LOG.info("starting daemon...")
        db.start()

    @app.on_event("shutdown")
    async def shutdown():
        LOG.info("shutting down daemon...")
        db.stop()
        db.close()

    @app.put("/api/v1/dataset/{name:path}", tags=['datasets'])
    async def create_dataset(name: str):
        try:
            await db.send_create_async(name)
        except Exception as e:
            return {"ok": False, "error": str(e)}
        return {"ok": True}

    @app.delete("/api/v1/dataset/{name:path}", tags=['datasets'])
    async def drop_dataset(name: str):
        try:
            await db.send_drop_async(name)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @app.get("/api/v1/dataset", tags=['datasets'])
    async def list_datasets():
        try:
            return {"ok": True, "datasets": list(db.datasets)}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    @app.get("/api/v1/dataset/{name:path}", tags=['datasets'])
    async def get_dataset_stats(name: str, nanoseconds: bool = True):
        ds = db.open_lsm_dataset(name)
        try:
            begin_time, end_time, num_entries = await ds.get_stats_async()
            if not nanoseconds:
                begin_time, end_time = datetime_from_nanoseconds(begin_time), datetime_from_nanoseconds(end_time)
            return {"ok": True, "dataset": name, "begin_time": begin_time, "end_time": end_time, "num_entries": num_entries}
        except Exception as e:
            return {"ok": False, "error": str(e)}
        finally:
            ds.close()

    @app.put("/api/v1/data/{name:path}", tags=['data'])
    async def insert_rows(name: str, rows: List[DataEntry]):
        try:
            await db.send_insert_many_async(name, (Entry(_to_nanoseconds(e.time), e.data) for e in rows))
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    @app.put("/api/v1/bulk-insert", tags=['data'])
    async def bulk_insert_rows(rows: List[NamedDataEntry]):
        try:
            await db.send_bulk_insert_many_async((NamedEntry(e.name, _to_nanoseconds(e.time), e.data) for e in rows))
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @app.delete("/api/v1/data/{name:path}", tags=['data'])
    async def delete_range(name: str, begin: Union[int, datetime], end: Union[int, datetime]):
        ds = db.open_lsm_dataset(name)
        try:
            await ds.delete_async(_to_nanoseconds(begin), _to_nanoseconds(end))
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}
        finally:
            ds.close()

    @app.get("/api/v1/data/{name:path}", tags=['data'])
    async def select_range(name: str, begin: Optional[Union[int, datetime]] = None, end: Optional[Union[int, datetime]] = None, nanoseconds: bool = True):
        ds = db.open_lsm_dataset(name)
        try:
            res = []
            begin = _to_nanoseconds(begin) if begin is not None else None
            end = _to_nanoseconds(end) if end is not None else None
            if nanoseconds:
                async for e in ds.find_range_async(begin, end):
                    res.append( {"time": e.time, "data": e.data.tobytes()} )
            else:
                async for e in ds.find_range_async(begin, end):
                   res.append( {"time": datetime_from_nanoseconds(e.time), "data": e.data.tobytes()} )

            return {"ok": True, "data": res}
        except Exception as e:
            return {"ok": False, "error": str(e)}
        finally:
            ds.close()

    return app
