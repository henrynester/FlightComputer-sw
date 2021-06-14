from dataclasses import dataclass
import time
# from modules.mcl.config import Config
from enum import Enum, Flag
from smbus import SMBus


class ValveBoardDriver():
    @dataclass
    class ActuatorData():
        goal_pos: int = 0

    @dataclass
    class SensorData():
        pos: int = 0
        goal_pos: int = 0
        speed: int = 0
        current_dA: int = 0
        sensor_A1: int = 0
        sensor_A2: int = 0
        sensor_A3: int = 0

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

    class Command(Enum):
        SET_ACTUATOR_DATA = 0x01
        REQUEST_SENSOR_DATA = 0x02

    def __init__(self, address):
        self.address = address
        self.actuator_data = self.ActuatorData()
        self.sensor_data = self.SensorData()

        self.i2c = SMBus(1)
        time.sleep(1)  # SO said waiting after I2C init makes it work right

    def read(self):
        t0 = time.time()
        rx = None
        try:
            rx = self.i2c.read_i2c_block_data(
                self.address, self.Command.REQUEST_SENSOR_DATA.value, 12)
        except OSError as e:
            print('rx', e, time.time())
        print(time.time()-t0)
        if rx is not None:
            # print(time.time()-t0)
            self.sensor_data.pos = rx[0]
            self.sensor_data.goal_pos = rx[1]
            self.sensor_data.speed = rx[2] - 128
            self.sensor_data.current_dA = rx[3]
            self.sensor_data.sensor_A1 = rx[4] * 256 + rx[5]
            self.sensor_data.sensor_A1 = rx[6] * 256 + rx[7]
            self.sensor_data.sensor_A1 = rx[8] * 256 + rx[9]
        # self.sensor_data.homing = self.SensorData.Homing(rx[10])
        # self.sensor_data.faults = self.SensorData.Faults(rx[11])

    def write(self):
        tx_bytes = [self.actuator_data.goal_pos]
        t0 = time.time()

        try:
            self.i2c.write_i2c_block_data(
                self.address, self.Command.SET_ACTUATOR_DATA.value, tx_bytes)
        except OSError as e:
            print('tx', e, time.time())

        # print(time.time()-t0)
