from dataclasses import dataclass

from ..logger import log
from .payload import MessagePayload
from .utils import B642B, unpack_buffer_to_list, B2B64


@dataclass
class EventHeader:
    mod: int 
    appid: int 
    timestamp: int
    payload_size: int

    def to_dict(self) -> str:
        return {
            "mod": self.mod,
            "appid": self.appid,
            "timestamp": self.timestamp,
            "payload_size": self.payload_size
        }

    def to_array(self) -> list:
        return [
            self.mod, 
            self.appid,
            self.timestamp, 
            self.payload_size
        ]


@dataclass
class EventDataIn:
    datasource: int
    datatype: str
    buffer: bytes

    def to_dict(self) -> str:
        return {
            "datasource": self.datasource,
            "datatype": self.datatype,
            "buffer": unpack_buffer_to_list(self.buffer, self.datatype[0] == "<", 4, self.datatype[1])
        }

    def to_array(self) -> list:
        return [
            self.datasource,
            self.datatype,
            self.buffer
        ]


@dataclass
class EventException:
    error: int
    msg: str

    def to_dict(self) -> str:
        return {
            "error": self.error,
            "msg": self.msg
        }

    def to_array(self) -> list:
        return [
            self.error,
            self.msg
        ]


@dataclass
class EventCMDStatus:
    mod: int
    op: int
    status: int

    def to_dict(self) -> str:
        return {
            "mod": self.mod,
            "op": self.op,
            "status": self.status
        }

    def to_array(self) -> list:
        return [
            self.mod,
            self.op,
            self.status
        ]


@dataclass
class EventLog:
    level: int
    msg: str

    def to_dict(self) -> str:
        return {
            "level": self.level,
            "msg": self.msg
        }

    def to_array(self) -> list:
        return [
            self.level,
            self.msg
        ]


@dataclass
class EventPostProc:
    key: bin
    array_size: int
    buffer: list # TODO

    def to_dict(self) -> str:
        return { "TO": "DO "}

    def to_array(self) -> list:
        return [
            "TO", "DO"
        ]


@dataclass
class EventCustom:
    data: bytearray

    def __init__(self, data) -> None:
        if(type(data) == str):
            data = B642B(data)
        self.data = bytearray(data)

    def to_dict(self) -> str:
        return { "data": B2B64(self.data) }

    def to_array(self) -> list:
        return [ self.data ]


OP_TO_EVENT_TYPES = {
    0: EventException,
    1: EventDataIn,
    256: EventCMDStatus,
    257: EventLog,
    512: EventPostProc, 
    3840: EventCustom,
    3841: EventCustom,
    3842: EventCustom,
    3843: EventCustom
}


def GetEventClass(event_type_id: int):
    return OP_TO_EVENT_TYPES.get(event_type_id, None)


class EventMessagePayload(MessagePayload):
    @classmethod
    def from_array(cls, operation: int, raw_data: list) -> "MessagePayload":
        EventClass = GetEventClass(operation)
        if EventClass is None:
            log(f"Operation {operation} unknown", logger_level="ERROR")
            return

        payload = cls()
        payload.header = EventHeader(*raw_data[:4])
        payload.event = EventClass(*raw_data[4:])

        return payload

    @classmethod
    def from_json(cls, operation: int, raw_data: list) -> "MessagePayload":
        EventClass = GetEventClass(operation)
        if EventClass is None:
            log(f"Operation {operation} unknown", logger_level="ERROR")
            return
            
        payload = cls()
        payload.header = EventHeader(**raw_data["header"])
        payload.event = EventClass(**raw_data["data"])

        return payload

    def to_dict(self) -> dict:
        return {
            "header": self.header.to_dict(),
            "data": self.event.to_dict()
        }
