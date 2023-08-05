class Device(object):

    def __init__(self, name: str) -> None:
        self.name: str = str(name)
        self.out_data = []
        self.in_data = b""
        self.hid = 0

    def send(self, data: bytes) -> None:
        self.out_data += [b"\x12"+self.hid.to_bytes(1,"little")+data]
        self.hid = (self.hid + 1) % 255
