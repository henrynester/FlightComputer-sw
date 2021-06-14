from modules.tasks.task import Task
from modules.mcl.system_state import SystemState, Phase
# import threading
from modules.drivers.led import LEDDriver, LEDColor


# class KeyboardThread(threading.Thread):
#     def __init__(self, input_cbk=None, name='keyboard-input-thread'):
#         self.input_cbk = input_cbk
#         super(KeyboardThread, self).__init__(name=name)
#         self.start()

#     def run(self):
#         while True:
#             try:
#                 self.input_cbk(input())  # waits to get input + Return
#             except (EOFError):
#                 return


class LEDTask(Task):
    def __init__(self, state: SystemState):
        self.next_phase: Phase = None
        self.driver = LEDDriver()
        super().__init__('LED', state)

    def actuate(self):
        print(self.state.phase)
        self.driver.color = LEDColor.RED

    def deinitialize(self):
        self.driver.deinitialize()
