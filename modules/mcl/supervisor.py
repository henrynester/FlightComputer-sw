from modules.tasks.task import Task
from modules.tasks.led_task import LEDTask
from modules.tasks.phase_task import PhaseTask
from modules.tasks.valves_task import ValvesTask
from modules.mcl.system_state import SystemState
from modules.mcl.config import Config
import time


class Supervisor(Task):
    def __init__(self):
        s = SystemState()
        self.tasks: [Task]
        self.tasks = [PhaseTask(s), LEDTask(s), ValvesTask(s)]
        self.loop_delay = Config.run_options.loop_delay
        super().__init__('Supervisor', s)

    def sense(self):
        for task in self.tasks:
            task.sense()

    def control(self):
        for task in self.tasks:
            task.control()

    def actuate(self):
        for task in self.tasks:
            task.actuate()

    def deinitialize(self):
        for task in self.tasks:
            task.deinitialize()

    def run(self):
        print('mcl start')
        try:
            while True:
                self.sense()
                self.control()
                self.actuate()
                # if self.loop_delay > 0:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.deinitialize()
        print('mcl exit')
