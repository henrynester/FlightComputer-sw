from modules.tasks.task import Task
# from modules.mcl.config import Config
# , ActuatorData  # , SensorData
from modules.drivers.valve import ValveBoardDriver
from modules.mcl.system_state import SystemState


class ValvesTask(Task):
    def __init__(self, state: SystemState):
        self.driver = ValveBoardDriver(0x44)
        super().__init__('Valves', state)

    def sense(self):
        self.driver.read()
        pass

    def control(self):
        pass

    def actuate(self):
        self.driver.write()
        pass
