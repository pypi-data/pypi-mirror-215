# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_hts221 import hts221

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
hts = hts221.HTS221(i2c)

hts.data_rate = hts221.ONE_SHOT

while True:
    for data_rate in hts221.data_rate_values:
        print("Current Data rate setting: ", hts.data_rate)
        for _ in range(10):
            humidity = hts.relative_humidity
            print("Humidity :{:.2f}%".format(humidity))
            print()
            time.sleep(0.5)
