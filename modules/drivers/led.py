from enum import Enum
from modules.mcl.config import Config

DESKTOP = Config.run_options.desktop
if not DESKTOP:
    import RPi.GPIO


class Color(Enum):
    OFF = (False, False, False)
    BLUE = (False, False, True)
    GREEN = (False, True, False)
    RED = (True, False, False)
    YELLOW = (True, True, False)


class LEDDriver:
    def __init__(self):
        if DESKTOP:
            print('LED init')
        else:
            print('real shit')

    def set_color(self, color: Color):
        if DESKTOP:
            print(f'LED is {color}')
        else:
            print('yuh')
