import traceback
from serial import Serial
import threading

from ..core.device import Device
from ..core.observer import dispatcher
from ..core.events import ApplicationEvents, DeviceEvents
from ..core.logger import log
from ..core.message.base import Message
from .base import DeviceConnector


DEFAULT_PORT = "COM3"
MAX_PAYLOAD_SIZE = 4 * 1024



class PacketsHandler(object):
    """
    This class is here to handle the packets (before handling the message)
    It allows to check packet header and to collatione the packet if message is not
    complete
    """
    def __init__(self):
        self._buffer = bytearray([])
        self._pid = -1
         
    def push(self, packet):
        if not packet:
            raise RuntimeError("Connection error, empty packet")

        header = packet[:2]
        payload = packet[2:]

        #check version
        version = ((header[0]>>4)&0xF)
        issecure = (header[0]&8)
        msgtyp = ((header[0]&6)>>1)
        islast = (header[0]&1)
        pid = header[1]

        if (version != 1):
            raise RuntimeError("Bad protocol version %d, only supporting version 1" % version)

        if (msgtyp != 1):
            raise RuntimeError("Bad msg type %d, only supporting application message (1)" % msgtyp)

        if (self._pid != -1 and pid != self._pid):
            raise RuntimeError("This version of proxy doesn't support interleaved messages")

        self._pid = pid
        self._buffer += payload

        if not islast:
            return None

        self._pid = -1
        message = self._buffer
        self._buffer = bytearray([])


        return Message.from_msgpack(message)


class RecvStatus:
    def __init__(self, device):
        self.device = device
        self.expected = 0
        self.binary_data = []


class SerialConnector(DeviceConnector):

    def __init__(self, config: dict = {}) -> None:
        self._port = config.get("port", DEFAULT_PORT)
        self._serial = None
        self._run = False

        self._handler = PacketsHandler()

        dispatcher.add_observer(ApplicationEvents.ON_QUIT, self.on_exit)

    def on_exit(self):
        self._run = False

    def open(self) -> None:
        self._serial = Serial(self._port)
        self._serial.baudrate = 115200;


    def close(self) -> None:
        log(f"Closing serial port")
        self._serial.close()

    def new_device(self) -> None:
        device = Device(self._port)
        dispatcher.notify(DeviceEvents.CONNECTED, device)
        x = threading.Thread(target=self._device_sender, args=(device,),daemon=True)
        x.start()

        return device

    def read_device(self) -> Message:
        length_array = self._serial.read(4)
        length =  int.from_bytes(length_array, "little")
        data = self._serial.read(length)

        try:
            msg = self._handler.push(data)
        except Exception as e:
            log(f"Error while handling packet: {e}")
            return None
        return msg

    def _device_sender(self,device):
        
        log("Serial Sender waiting for data...")
        while(self._run):
            if len(device.out_data) == 0:
                continue

            data = device.out_data[0]
            length =  len(data)
            if length > MAX_PAYLOAD_SIZE:
                log(f"Payload too big, max size is {MAX_PAYLOAD_SIZE} bytes")
                raise RuntimeError("Payload too big, max size is %d bytes" % MAX_PAYLOAD_SIZE)

            log(f"Sending {length} bytes to device")
            l1 = self._serial.write(length.to_bytes(4, "little"))
            self._serial.flush()
            l2 = self._serial.write(data)
            self._serial.flush()
            log(f"Sent {l1} header + {l2} payload to device")

            device.out_data = device.out_data[1:]
        log("Serial Sender ended")

    def run(self) -> None:
        log(f"Listening to serial port {self._port}")

        try:
            device = self.new_device()
            self._run = True
            while self._run:
                msg = self.read_device()
                if msg:
                    log("Got message from device: %s" % msg.to_json())
                    dispatcher.notify(DeviceEvents.ON_MESSAGE, device, msg)


        except KeyboardInterrupt:
            self._run = False
        finally:
            log("Closing case 3")
            traceback.print_exc()
            self.close()
