class Thermometer:
    def __init__(self):
        self._temperature = 32.8

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value


t = Thermometer()
pass
