import pymem
from pymem.exception import ProcessNotFound


class TR2013Connector:
    COLLECTIBLE_MANAGER = 0x1CDEC40

    def __init__(self, pm: "pymem.Pymem"):
        self.pm = pm
        self.base = pm.base_address

    @classmethod
    def attach(cls, name: str = "TombRaider.exe") -> "TR2013Connector":
        try:
            pm = pymem.Pymem(name)
        except ProcessNotFound:
            raise RuntimeError(f"process not found: {name!r} (is the game running?)")
        return cls(pm)

    def read_int(self, addr):
        return self.pm.read_int(self.base + addr)

    def write_int(self, addr, val):
        self.pm.write_int(self.base + addr, val)

    def read_bytes(self, addr, n):
        return self.pm.read_bytes(self.base + addr, n)

    def write_bytes(self, addr, b):
        self.pm.write_bytes(self.base + addr, b, len(b))

    def collectible_manager(self) -> int:
        return int(self.pm.read_uint(self.base + self.COLLECTIBLE_MANAGER))

    def read_collectible_flag(self, manager: int, offset: int) -> int:
        return int(self.pm.read_uchar(manager + offset))

    def clear_collectible_flag(self, manager: int, offset: int):
        self.pm.write_uchar(manager + offset, 0)
