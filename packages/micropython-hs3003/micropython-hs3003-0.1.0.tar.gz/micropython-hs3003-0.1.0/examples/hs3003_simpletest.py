# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_hs3003 import hs3003

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
hs = hs3003.HS3003(i2c)

while True:
    temperature, relative_humidity = hs.measurements
    print("Temperature: {:.1f}C".format(temperature))
    print("Humidity: {:.1f}C".format(relative_humidity))
    print("")
    time.sleep(1)
