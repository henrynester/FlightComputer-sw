from modules.tasks.task import Task
from modules.mcl.system_state import SystemState, Phase
import threading
import modules.drivers.led


class KeyboardThread(threading.Thread):
    def __init__(self, input_cbk=None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            try:
                self.input_cbk(input())  # waits to get input + Return
            except (EOFError):
                return


class LEDTask(Task):
    def __init__(self):
        self.next_phase: Phase = None
        super().__init__('LED')

    def my_callback(self, inp):
        self.next_phase = Phase(int(inp))

    def initialize(self, state):
        KeyboardThread(self.my_callback)

    def sense(self, state):
        pass

    def control(self, state):
        if (self.next_phase is not None):
            state.phase = self.next_phase
            self.next_phase = None

    def actuate(self, state: SystemState):
        print(state.phase)
        pass
