# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_wsentids import wsentids

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
wsen = wsentids.WSENTIDS(i2c)

wsen.data_rate = wsentids.RATE_50_HZ

while True:
    for data_rate in wsentids.data_rate_values:
        print("Current Data rate setting: ", wsen.data_rate)
        for _ in range(10):
            wsen.data_rate = data_rate
            print("Temperature: {:.1f}C".format(wsen.temperature))
            time.sleep(0.5)
        wsen.data_rate = data_rate
