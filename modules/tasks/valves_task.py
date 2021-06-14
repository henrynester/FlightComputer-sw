from modules.tasks.task import Task
# from modules.mcl.config import Config
from modules.drivers.valve import ValveDriver, ActuatorData  # , SensorData
from modules.mcl.system_state import SystemState


class ValvesTask(Task):
    def __init__(self, state: SystemState):
        self.driver = ValveDriver()
        super().__init__('Valves', state)

    def sense(self):
        pass

    def control(self):
        pass

    def actuate(self):
        self.driver.write(ActuatorData())
        pass
