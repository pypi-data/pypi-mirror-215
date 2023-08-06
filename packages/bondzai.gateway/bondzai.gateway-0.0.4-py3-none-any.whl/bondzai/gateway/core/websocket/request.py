from dataclasses import dataclass

from ..manager import Manager


ACT_SUB_TO_DEVICE = "sub-to-device"
ACT_UNSUB_FROM_DEVUCE = "unsub-from-device"
ACT_SEND_TO_DEVICE = "send-to-device"
ACT_GET_DEVICES_LIST = "get-device-list"

VALID_ACTIONS = [
    ACT_GET_DEVICES_LIST,
    ACT_SEND_TO_DEVICE,
    ACT_UNSUB_FROM_DEVUCE,
    ACT_SUB_TO_DEVICE
]


@dataclass
class WebsocketRequest:
    action: str
    device_name: str
    message: str

    def __init__(self, action: str, device_name: str = None, message: str = None) -> None:
        self.action = action
        self.device_name = device_name
        self.message = message

    def is_valid(self) -> bool:
        # not valid if action is not in valid actions list
        if self.action not in VALID_ACTIONS:
            return False
        
        # if action is get device list, we don't need more arguments, so it's valid
        if self.action == ACT_GET_DEVICES_LIST:
            return True

        # if the device required is not registered it's not valid
        device = Manager.GetDevice(self.device_name)
        if not device:
            return False

        # if the action is send to device and there is no message, it's not valid
        if self.action == ACT_SEND_TO_DEVICE and not self.message: # TODO : Validate message
            return False
        
        return True

    def to_string(self) -> str:
        if not self.message:
            msg = "NULL"
        elif len(self.message) <= 350:
            msg = self.message
        else:
            msg = f"{self.message[:150]} ... {len(self.message)-300} ... {self.message[-150:]}"     
            
        return f"{self.action} - {self.device_name if self.device_name else 'NULL'} - {msg}"
