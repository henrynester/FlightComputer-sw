from modules.tasks.task import Task
from modules.tasks.led_task import LEDTask
from modules.tasks.phase_task import PhaseTask
from modules.mcl.system_state import SystemState
import time


class Supervisor(Task):
    def __init__(self):
        self.tasks: [Task]
        self.tasks = [PhaseTask(), LEDTask()]
        self.system_state = SystemState()
        super().__init__('Supervisor')

    def initialize(self, state):
        for task in self.tasks:
            task.initialize(state)

    def sense(self, state):
        for task in self.tasks:
            task.sense(state)

    def control(self, state):
        for task in self.tasks:
            task.control(state)

    def actuate(self, state):
        for task in self.tasks:
            task.actuate(state)

    def run(self):
        self.initialize(self.system_state)
        while True:
            self.sense(self.system_state)
            self.control(self.system_state)
            self.actuate(self.system_state)
            time.sleep(0.5)
