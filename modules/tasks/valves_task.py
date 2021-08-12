from modules.tasks.task import Task
# from modules.mcl.config import Config
# , ActuatorData  # , SensorData
from modules.drivers.valve import ValveBoard
from modules.mcl.system_state import SystemState
from modules.threads.slow_i2c_thread import SlowI2CThread
from modules.drivers.i2c import I2CBus


class ValvesTask(Task):
    def __init__(self, state: SystemState):
        i2c_bus = I2CBus()
        self.valve = ValveBoard(i2c_bus, 0x44)
        self.valve.valve_control.value = ValveBoard.ValveControlData(
            goal_pos=50)
        self.i2c_thread = SlowI2CThread([self.valve])
        self.i2c_thread.start()
        super().__init__('Valves', state)

    def sense(self):
        self.valve.sync_all()
        print(self.valve.sensor.value, self.valve.check_connected())
