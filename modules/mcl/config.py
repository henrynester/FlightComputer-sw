class Config:
    class autosequence:
        FUEL_TANK_PRESSURE_BAR = 40
        FUEL_INJ_PRESSURE_BAR = 35
        OX_INJ_PRESSURE_BAR = 35
        OX_TRICKLE_POS = 10
        FUEL_TRICKLE_POS = 10
        COUNTDOWN_DURATION = 15
        IGNITOR_FIRE_DURATION = 1
        ENGINE_VENT_DURATION = 10
        FUEL_TANK_VENT_DURATION = 10
        OX_TRICKLE_START_TIME = 0.0
        IGNITOR_FIRE_START_TIME = 0.5
        FUEL_TRICKLE_START_TIME = 1.0
        RAMPUP_START_TIME = 2.0
        BURN_START_TIME = 6.0
        SHUTDOWN_START_TIME = 15.0

    class valves:
        pass

    class run_options:
        desktop = False
        loop_delay = 0.5
