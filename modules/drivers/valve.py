# import time
# from modules.mcl.config import Config
from enum import Flag
from modules.drivers.i2c import I2CBus, I2CInput, I2COutput
import typing


class ValveBoard():
    def __init__(self, bus: I2CBus, addr: int):
        self.addr = addr
        self.bus = bus

        self.valve_control = ValveBoard.ValveControlI2COutput(bus, addr)
        self.valve_status = ValveBoard.ValveStatusI2CInput(bus, addr)
        self.sensor = ValveBoard.SensorI2CInput(bus, addr)

    def check_connected(self):
        return all([self.valve_control.ok, self.valve_status.ok,
                    self.sensor.ok])

    def sync_all(self):
        self.valve_control.sync_value()
        self.valve_status.sync_value()
        self.sensor.sync_value()

    class ValveControlData(typing.NamedTuple):
        goal_pos: int = 0

    class ValveControlI2COutput(I2COutput[ValveControlData]):
        def __init__(self, bus, addr):
            super().__init__(bus, addr, 0x01)

        def convert(self, data):
            return [data.goal_pos]

    class ValveStatusData(typing.NamedTuple):
        pos: int
        goal_pos: int
        speed: int
        current: float

        class Homing(Flag):
            HOMING = 0
            LIMIT_SWITCH = 1
            HAS_HOMED = 2

        class Faults(Flag):
            OK = 0
            I2C_ERROR = 1
            DRV_FAILSAFE = 2
            OPEN_CIRCUIT = 4
            MOTOR_STALL = 8
            MOTOR_SLIP_ENCODER_DRIFT = 16
            HOMING_TIMEOUT = 32
            LIMIT_SWITCH_STUCK = 64

        homing: Homing = Homing.HOMING
        faults: Faults = Faults.OK

    class ValveStatusI2CInput(I2CInput[ValveStatusData]):
        def __init__(self, bus, addr):
            super().__init__(bus, addr, 0x02, 6)

        def convert(self, rx):
            return ValveBoard.ValveStatusData(
                pos=rx[0],
                goal_pos=rx[1],
                speed=rx[2] - 128,
                current=rx[3] / 10,
                homing=ValveBoard.ValveStatusData.Homing(rx[4]),
                faults=ValveBoard.ValveStatusData.Faults(rx[5]))

    class SensorData(typing.NamedTuple):
        sensor_A1: int = 0
        sensor_A2: int = 0
        sensor_A3: int = 0

    class SensorI2CInput(I2CInput[SensorData]):
        def __init__(self, bus, addr):
            super().__init__(bus, addr, 0x03, 6)

        def convert(self, rx):
            return ValveBoard.SensorData(
                sensor_A1=rx[0] + rx[1] * 256,
                sensor_A2=rx[2] + rx[3] * 256,
                sensor_A3=rx[4] + rx[5] * 256)
