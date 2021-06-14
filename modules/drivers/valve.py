from abc import ABC, abstractmethod
from dataclasses import dataclass
from modules.mcl.config import Config
from enum import IntEnum, IntFlag
import struct


class AbstractValveDriver(ABC):
    @dataclass
    class ActuatorData:
        goal_pos: int

    @dataclass
    class SensorData:
        pos: int
        goal_pos: int
        speed: int
        current_dA: int
        sensor_A1: int
        sensor_A2: int
        sensor_A3: int
        limit_switch: bool
        has_homed: bool

        class Faults(IntFlag):
            I2C_ERROR = 1
            DRV_FAILSAFE = 2
            OPEN_CIRCUIT = 4
            MOTOR_STALL = 8
            MOTOR_SLIP_ENCODER_DRIFT = 16
            HOMING_TIMEOUT = 32
            LIMIT_SWITCH_STUCK = 64

        faults: Faults

    actuator_struct = struct.Struct('B')
    sensor_struct = struct.Struct('B B b B H H H B B')

    class Command(IntEnum):
        SET_ACTUATOR_DATA = 0x01
        REQUEST_SENSOR_DATA = 0x02

    def __init__(self, address):
        self.address = address
        self.actuator_data = self.ActuatorData()
        self.sensor_data = self.SensorData()

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass


if Config.run_options.desktop:
    class ValveDriver(AbstractValveDriver):
        def read(self):
            pass

        def write(self, data):
            pass

else:
    from smbus import SMBus

    class ValveDriver(AbstractValveDriver):
        # I2C bus 0 is the bus used by the Pi to talk to PiHAT ROMs
        # use I2C 1, which is free
        def __init__(self, address):
            self.i2c = SMBus(1)
            super().__init__(self, address)

        def read(self) -> AbstractValveDriver.SensorData:
            rx_bytes = bytes(self.i2c.read_i2c_block_data(
                self.address, self.Command.REQUEST_SENSOR_DATA, len=32))
            return AbstractValveDriver.SensorData(
                AbstractValveDriver.sensor_struct.unpack(rx_bytes))

        def write(self, data: AbstractValveDriver.ActuatorData):
            self.i2c.write_i2c_block_data(
                self.address, self.Command.SET_ACTUATOR_DATA, [0xAB])
