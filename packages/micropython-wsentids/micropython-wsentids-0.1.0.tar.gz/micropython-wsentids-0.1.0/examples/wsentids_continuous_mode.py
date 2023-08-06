# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_wsentids import wsentids

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
wsen = wsentids.WSENTIDS(i2c)

wsen.continuous_mode = wsentids.CONTINUOUS_DISABLED

while True:
    for continuous_mode in wsentids.continuous_mode_values:
        print("Current Continuous mode setting: ", wsen.continuous_mode)
        for _ in range(10):
            wsen.continuous_mode = continuous_mode
            print("Temperature: {:.1f}C".format(wsen.temp))
            print()
            time.sleep(0.5)
        wsen.continuous_mode = continuous_mode
