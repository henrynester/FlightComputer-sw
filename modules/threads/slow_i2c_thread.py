import threading
import time
import typing
from modules.drivers.valve import ValveBoard


class SlowI2CThread(threading.Thread):
    def __init__(self, valve_boards: typing.List[ValveBoard]):
        self.valve_boards = valve_boards
        self.t_fast_loop = 0
        self.fast_loop_counter = 0
        super().__init__(name='slow_i2c_thread', daemon=True)

    def run(self):
        while True:
            if (time.time() - self.t_fast_loop) > 0.5:
                self.t_fast_loop = time.time()
                self.fast_loop()
                self.fast_loop_counter += 1
            if self.fast_loop_counter >= 5:
                self.slow_loop()
                self.fast_loop_counter = 0

    def fast_loop(self):
        for valve_board in self.valve_boards:
            valve_board.valve_control.communicate()
            valve_board.sensor.communicate()

    def slow_loop(self):
        for valve_board in self.valve_boards:
            valve_board.valve_status.communicate()
