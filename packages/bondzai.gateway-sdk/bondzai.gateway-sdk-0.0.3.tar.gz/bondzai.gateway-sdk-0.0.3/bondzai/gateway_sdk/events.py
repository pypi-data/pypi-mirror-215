from dataclasses import dataclass
from typing import Union

from .utils import b2b64
from .enums import EventOperationID


EVENT_DATA_IN_CSTRUCT_SIZEOF = 14


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

    def get_size(self) -> int:
        #FIXME: size must depend on datatype
        #JDE: consider that data is float
        return EVENT_DATA_IN_CSTRUCT_SIZEOF + len(self.buffer) * 4

    def to_dict(self) -> str:
        return {
            "datasource": self.datasource,
            "datatype": self.datatype,
            "buffer": self.buffer
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

    def get_size(self) -> int:
        return 0

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

    def get_size(self) -> int:
        return 0

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
    appid: int
    mod: int
    timestamp: int
    level: int
    msg: str

    def get_size(self) -> int:
        return 0

    def to_dict(self) -> str:
        return {
            "appid": self.appid,
            "mod": self.mod,
            "timestamp": self.timestamp,
            "level": self.level,
            "msg": self.msg
        }

    def to_array(self) -> list:
        return [
            self.appid,
            self.mod,
            self.timestamp,
            self.level,
            self.msg
        ]


@dataclass
class EventPostProc:
    key: bin
    array_size: int
    buffer: list # TODO

    def get_size(self) -> int:
        return 0

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
        self.data = bytearray(data)

    def get_size(self) -> int:
        return len(self.data)

    def to_dict(self) -> str:
        return { "data": b2b64(self.data) }

    def to_array(self) -> list:
        return [ self.data ]
    
    @classmethod
    def from_dict(cls, data: dict) -> "EventCustom":
        return EventCustom(data.get("data"))


EventPayloadType = Union[
    EventCMDStatus, 
    EventCustom, 
    EventDataIn, 
    EventException, 
    EventLog, 
    EventPostProc
]    


OP_TO_EVENT_TYPES = {
    EventOperationID.EVT_EXT_EXCEPTION: EventException,
    EventOperationID.EVT_EXT_DATA_IN: EventDataIn,
    EventOperationID.EVT_EXT_CMD_STATUS: EventCMDStatus,
    EventOperationID.EVT_EXT_LOG: EventLog,
    EventOperationID.EVT_EXT_POSTPROC: EventPostProc, 
    EventOperationID.EVT_EXT_CUSTOM_1: EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_2: EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_3: EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_4: EventCustom
}


def get_event_class(event_type_id: EventOperationID):
    return OP_TO_EVENT_TYPES.get(event_type_id, None)
