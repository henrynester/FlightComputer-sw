from smbus import SMBus
import typing


class I2C:
    def __init__(self, bus_num=1):
        self._bus = SMBus(bus_num)
        self._bus.open()

    def write(self, address_byte: int, command_byte: int,
              data_bytes: list(int)) -> bool:
        try:
            self._bus.write_i2c_block_data(
                address_byte, command_byte, data_bytes)
        except OSError:
            return False
        return True

    def read(self, address_byte: int, command_byte: int,
             num_bytes: int) -> typing.Union[[int], None]:
        try:
            return self._bus.read_i2c_block_data(address_byte, command_byte,
                                                 num_bytes)
        except OSError:
            return None
