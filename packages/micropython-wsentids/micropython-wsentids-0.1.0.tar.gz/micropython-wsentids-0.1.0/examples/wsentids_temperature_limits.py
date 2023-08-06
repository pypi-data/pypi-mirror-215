# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_wsentids import wsentids

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
wsen = wsentids.WSENTIDS(i2c)

wsen.low_limit = 20
wsen.high_limit = 26

print("High limit", wsen.high_limit)
print("Low limit", wsen.low_limit)

while True:
    print("Temperature: {:.1f}C".format(wsen.temperature))
    alert_status = wsen.alert_status
    if alert_status.high_alert:
        print("Temperature above high set limit!")
    if alert_status.low_alert:
        print("Temperature below low set limit!")
    print("Low alert:", alert_status.low_alert)
    print("High alert:", alert_status.high_alert)
    time.sleep(1)
