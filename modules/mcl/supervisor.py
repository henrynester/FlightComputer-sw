from modules.tasks.task import Task
from modules.tasks.led_task import LEDTask
from modules.tasks.phase_task import PhaseTask
from modules.mcl.system_state import SystemState
from modules.mcl.config import Config
import time


class Supervisor(Task):
    def __init__(self):
        self.tasks: [Task]
        self.tasks = [PhaseTask(), LEDTask()]
        self.system_state = SystemState()
        self.loop_delay = Config.run_options.loop_delay
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

    def deinitialize(self):
        for task in self.tasks:
            task.deinitialize()

    def run(self):
        self.initialize(self.system_state)
        print('mcl start')
        try:
            while True:
                self.sense(self.system_state)
                self.control(self.system_state)
                self.actuate(self.system_state)
                if self.loop_delay > 0:
                    time.sleep(self.loop_delay)
        except KeyboardInterrupt:
            self.deinitialize()
        print('mcl exit')
