# main.py
# Henry Nester
# 13 May 2021

# Starts up the main control loop for the flight computer. This code is
# intended to run on a Raspberry Pi built into the rocket and connected to
# several microcontrollers, but I'll work on spoofing these peripherals so
# we can test the code on a regular PC.

from modules.mcl.supervisor import Supervisor
# from modules.mcl.config import Config


def main():
    mcl = Supervisor()
    mcl.run()
    print('exiting main.py')


if __name__ == '__main__':
    main()
