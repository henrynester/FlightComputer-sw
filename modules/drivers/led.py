from enum import Enum
from modules.mcl.config import Config
from abc import ABC, abstractmethod
from modules.drivers.pins import Pins


class LEDColor(Enum):
    OFF = (False, False, False)
    BLUE = (False, False, True)
    GREEN = (False, True, False)
    RED = (True, False, False)
    YELLOW = (True, True, False)


class AbstractLEDDriver(ABC):
    def __init__(self):
        self._color = LEDColor.OFF

    @property
    def color(self) -> LEDColor:
        return self._color

    @color.setter
    def color(self, value: LEDColor):
        self._color = value
        self.update_gpio()

    @abstractmethod
    def update_gpio(self):
        pass

    def deinitialize(self):
        pass


if Config.run_options.desktop:
    class LEDDriver(AbstractLEDDriver):
        def update_gpio(self):
            print(f'LED is {self.color}')
else:
    import RPi.GPIO as GPIO

    class LEDDriver(AbstractLEDDriver):
        def __init__(self):
            # use GPIOXX pin numbering (from broadcom pinout) instead of RPi
            # GPIO header 1-40 numbering. May vary b/w boards!
            GPIO.setmode(GPIO.BCM)
            self.pins = [Pins.LED_R, Pins.LED_G, Pins.LED_B]
            for pin in self.pins:
                GPIO.setup(pin, GPIO.OUT)
            super().__init__()

        def update_gpio(self):
            for pin, bit in zip(self.pins, self.color.value):
                GPIO.output(pin, bit)

        def deinitialize(self):
            GPIO.cleanup()
