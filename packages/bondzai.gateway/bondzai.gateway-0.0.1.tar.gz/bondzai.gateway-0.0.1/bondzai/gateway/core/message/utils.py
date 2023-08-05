import base64
import json
from typing import Any
import struct


def msg_serialize(o: Any) -> str:
    return json.dumps(o)


def msg_deserialize(o: str) -> Any:
    return json.loads(o)


def B2B64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def B642B(data: str) -> bytes:
    return base64.b64decode(data)


def unpack_buffer_to_list(buffer, is_little, data_len, pack_unit_format) -> list[Any]:
    buffer = bytearray(buffer)
    buffer_len = len(buffer)
    nb_items = int(buffer_len / data_len)
    struct_format = "".join([pack_unit_format for _ in range(0, nb_items)])
    return list(struct.unpack(f"{'<' if is_little else'>'}{struct_format}", buffer))


def pack_list_to_buffer(buffer: list[Any], is_little: bool, pack_unit_format: str) -> bytes:
    struct_format = "".join([pack_unit_format for _ in range(0, len(buffer))])
    return struct.pack(f"{'<' if is_little else' >'}{struct_format}", *buffer)
