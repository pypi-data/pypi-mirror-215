from abc import ABC, abstractmethod
import socket
import struct
import fcntl
from typing import Any, Callable

import asyncio
import os

F_SETPIPE_SZ = 1031

_msg_hdr = struct.Struct('I')
_msg_hdr_pack = _msg_hdr.pack
_msg_hdr_unpack = _msg_hdr.unpack
_msg_hdr_size = _msg_hdr.size
_int_from_bytes = int.from_bytes
_int_to_bytes = int.to_bytes

_os_read = os.read
_os_write = os.write


def _get_max_pipe_size() -> int:
    with open('/proc/sys/fs/pipe-max-size', 'r') as fd:
        return int(fd.read())
    
def _recvall(recv_func: Callable[[int], bytes], size: int) -> bytearray:
    res = bytearray()
    while len(res) != size:
        res += recv_func(size - len(res))
    return res

async def _recvall_async(recv_func: Callable[[int], bytes], size: int) -> bytearray:
    res = bytearray()
    while len(res) != size:
        res += await recv_func(size - len(res))
    return res

class MessageSocket(ABC):
    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def recv_msg(self) -> bytes:
        pass

    @abstractmethod
    def send_msg(self, msg: bytes) -> None:
        pass
    
    @abstractmethod
    async def recv_msg_async(self) -> bytes:
        pass

    @abstractmethod
    async def send_msg_async(self, msg: bytes) -> None:
        pass

_loop = asyncio.get_event_loop()

class TCPMessageSocket(MessageSocket):
    __slots__ = ('_socket', '_sendall', '_recv', '_shutdown')
    def __init__(self, s: socket.socket, shutdown: bool = False):
        self._socket = s
        self._sendall = s.sendall
        self._recv = s.recv
        self._shutdown = shutdown

    async def _sendall_async(self, data: bytes) -> int:
        return await _loop.sock_sendall(self._socket, data)

    async def _recv_async(self, num_bytes: int) -> bytes:
        return await _loop.sock_recv(self._socket, num_bytes)

    @property
    def socket(self) -> socket.socket:
        return self._socket

    def close(self) -> None:
        if self._shutdown:
            try:
                self._socket.shutdown(socket.SHUTDOWN_RDWR)
            except:
                pass
        self._socket.close()

    def recv_msg(self) -> bytes:
        _recv = self._recv
        return _recvall(_recv, *_msg_hdr_unpack(_recvall(_recv, _msg_hdr_size)))

    def send_msg(self, msg: bytes) -> None:
        self._sendall(_msg_hdr_pack(len(msg))+msg)
    
    async def recv_msg_async(self) -> bytes:
        _recv_async = self._recv_async
        return await _recvall_async(_recv_async, *_msg_hdr_unpack(await _recvall_async(_recv_async, _msg_hdr_size)))

    async def send_msg_async(self, msg: bytes) -> None:
        await self._sendall_async(_msg_hdr_pack(len(msg))+msg)

class PipeMessageSocket(MessageSocket):
    __slots__ = ('_in', '_out')
    def __init__(self, in_pipe: int, out_pipe: int):
        self._in = in_pipe
        self._out = out_pipe
        try:
            fcntl.fcntl(out_pipe, F_SETPIPE_SZ, _get_max_pipe_size())
        except:
            pass

    def close(self) -> None:
        os.close(self._in)
        os.close(self._out)

    def recv_msg(self) -> bytes:
        _in = self._in
        s = _int_from_bytes(_os_read(_in, 4), 'little')
        return _os_read(_in, s)

    def send_msg(self, msg: bytes) -> None:
        _out = self._out
        _os_write(_out, _int_to_bytes(len(msg), 4, 'little'))
        _os_write(_out, msg)

class TCPListener:
    def __init__(self, no_delay: bool):
        self._listener = None
        self._port = None
        self._no_delay = int(no_delay)

    def __enter__(self, *args) -> Any:
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        if self._listener:
            self._listener.close()
            self._listener = None

    def open(self) -> None:
        if self._listener: raise RuntimeError("TCPListener already open")
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(('', 0))
        listener.listen()
        self._listener = listener
        self._port = listener.getsockname()[1]

    @property
    def port(self) -> int:
        return self._port
            
    def accept(self) -> TCPMessageSocket:
        # Accept connection from admin node
        conn, _ = self._listener.accept()
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
        conn.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, self._no_delay)
        return TCPMessageSocket(conn, True)


def open_tcp_socket(port: int, no_delay: bool) -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
    s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, int(no_delay))
    s.connect(('', port))
    return s

