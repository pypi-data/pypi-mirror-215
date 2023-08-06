# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_sht20 import sht20


i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
sht = sht20.SHT20(i2c)

print("Current Resolution")
print(sht.temp_rh_resolution)
sht.temp_rh_resolution = 0x81  # Take a look at the library for correct values
print("Changed Resolution")
print(sht.temp_rh_resolution)

while True:
    print("Temperature: {:.2f} C".format(sht.temperature))
    print("Humidity: {:.2f} %%".format(sht.humidity))
    print("")
    time.sleep(1)
