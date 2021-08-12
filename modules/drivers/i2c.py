from smbus import SMBus
import typing
from abc import ABC, abstractmethod
import threading
import time


class I2CBus:
    '''wrapper for smbus.SMBus, allowing I2C protocol operations only'''

    def __init__(self, bus_num=1):
        self._bus = SMBus(bus_num)

    def write(self, address_byte: int, command_byte: int,
              data_bytes: typing.List[int]) -> bool:
        '''writes the following to I2C:
        START
        address_byte (to select an I2C slave)
        R/W bit is LOW to indicate writing data
        command_byte (to select a function to write to)
        data_bytes
        STOP
        Returns True for success
        OSError occurs on bus glitches or when no device is connected'''
        try:
            self._bus.write_i2c_block_data(
                address_byte, command_byte, data_bytes)
        except OSError:
            return False
        return True

    def read(self, address_byte: int, command_byte: int,
             num_bytes: int) -> typing.Union[typing.List[int], None]:
        '''writes/reads the following to/from I2C:
        START
        address_byte (to select an I2C slave)
        R/W bit is HIGH to indicate writing the command
        command_byte (to select a function to read from)
        START
        address_byte
        R/W bit is LOW to indicate reading
        (slave puts out some bytes)
        STOP when num_bytes have been received
        returns a list of the bytes received, or None on failure
        OSError occurs on bus glitches or when no device is connected'''
        try:
            return self._bus.read_i2c_block_data(address_byte, command_byte,
                                                 num_bytes)
        except OSError:
            return None


T = typing.TypeVar('T')


class I2CInputOutput(ABC, typing.Generic[T]):
    '''class to represent I2C link with a specific device and command ID'''

    def __init__(self, bus: I2CBus, addr, cmd, length=0):
        self.lock = threading.Lock()
        self.bus = bus
        self.addr = addr
        self.cmd = cmd
        self.ok = False
        self.length = length
        self.value: T = None  # belongs to main thread
        self._i2cvalue: T = None  # belongs to I2C thread

    @abstractmethod
    def communicate(self):
        '''called on I2C thread to perform a single transaction.
        updates _i2cvalue'''
        pass

    @abstractmethod
    def sync_value(self):
        '''called on main thread to shift the self._i2cvalue data to the
        self.value data. Use self.lock to ensure the I2C thread can't modify
        self._i2cvalue during the operation'''
        pass


class I2CInput(I2CInputOutput[T]):
    def communicate(self):
        rx_bytes = self.bus.read(self.addr, self.cmd, self.length)
        self.ok = rx_bytes is not None
        if self.ok:
            self.lock.acquire()
            self._i2cvalue = self.convert(rx_bytes)
            self.lock.release()

    def sync_value(self):
        self.lock.acquire()
        self.value = self._i2cvalue
        self.lock.release()

    @abstractmethod
    def convert(self, rx_bytes: typing.List[int]) -> T:
        pass


class I2COutput(I2CInputOutput[T]):
    def communicate(self):
        self.lock.acquire()
        if self._i2cvalue is None:
            self.lock.release()
            return
        else:
            tx_bytes = self.convert(self._i2cvalue)
            self.lock.release()
            self.ok = self.bus.write(self.addr, self.cmd, tx_bytes)

    def sync_value(self):
        self.lock.acquire()
        self._i2cvalue = self.value
        self.lock.release()

    @abstractmethod
    def convert(self, data: T) -> typing.List[int]:
        pass


# class I2CInput(ABC):
#     def __init__(self, bus: I2CBus, addr, cmd, length):
#         self.bus = bus
#         self.addr = addr
#         self.cmd = cmd
#         self.length = length
#         self.ok = False

#     def update(self):
#         rx_bytes = self.bus.read(self.addr, self.cmd, self.length)
#         self.ok = rx_bytes is not None
#         if self.ok:
