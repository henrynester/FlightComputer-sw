from dataclasses import dataclass
# import time
# from modules.mcl.config import Config
from enum import Enum, Flag
from modules.drivers.i2c import I2C


class ValveBoardDriver():
    @dataclass
    class ValveControlData():
        goal_pos: int = 0

    @dataclass
    class ValveStatusData():
        pos: int = 0
        goal_pos: int = 0
        speed: int = 0
        current_dA: int = 0

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

    @dataclass
    class SensorData():
        sensor_A1: int = 0
        sensor_A2: int = 0
        sensor_A3: int = 0

        CMD_VALVE_CONTROL = 0x01
        CMD_VALVE_STATUS = 0x02
        CMD_SENSOR = 0x03

    def __init__(self, address: int, i2c: I2C):
        self.address = address
        self.i2c = i2c

        self.valve_control = self.ValveControlData()
        self.valve_status = self.ValveStatusData()
        self.sensor = self.SensorData()

    def read_status(self):
        rx = self.i2c.read(self.address, self.Command.VALVE_STATUS.value, 6)
        if rx is not None:
            self.sensor_data.pos = rx[0]
            self.sensor_data.goal_pos = rx[1]
            self.sensor_data.speed = rx[2] - 128
            self.sensor_data.current_dA = rx[3]
            self.sensor_data.homing = self.SensorData.Homing(rx[4])
            self.sensor_data.faults = self.SensorData.Faults(rx[5])

    # def read(self):
    #     t0 = time.time()
    #     rx = None
    #     try:
    #         rx = self.i2c.read_i2c_block_data(
    #             self.address, self.Command.REQUEST_SENSOR_DATA.value, 12)
    #     except OSError as e:
    #         print('rx', e, time.time())
    #     # print(time.time()-t0)
    #     if rx is not None:
    #         print(rx)
    #         # print(time.time()-t0)
    #         self.sensor_data.pos = rx[0]
    #         self.sensor_data.goal_pos = rx[1]
    #         self.sensor_data.speed = rx[2] - 128
    #         self.sensor_data.current_dA = rx[3]
    #         self.sensor_data.sensor_A1 = rx[4] * 256 + rx[5]
    #         self.sensor_data.sensor_A1 = rx[6] * 256 + rx[7]
    #         self.sensor_data.sensor_A1 = rx[8] * 256 + rx[9]
    #     # self.sensor_data.homing = self.SensorData.Homing(rx[10])
    #     # self.sensor_data.faults = self.SensorData.Faults(rx[11])

    # def write(self):
    #     tx_bytes = [0xCC]
    #     t0 = time.time()

    #     try:
    #         self.i2c.write_i2c_block_data(
    #             self.address, self.Command.SET_ACTUATOR_DATA.value, tx_bytes)
    #     except OSError as e:
    #         print('tx', e, time.time())

    #     # print(time.time()-t0)
