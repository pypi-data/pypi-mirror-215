# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_hts221 import hts221

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
hts = hts221.HTS221(i2c)

hts.block_data_update = hts221.BDU_ENABLED

while True:
    for block_data_update in hts221.block_data_update_values:
        print("Current Block data update setting: ", hts.block_data_update)
        for _ in range(10):
            while True:
                humidity = hts.relative_humidity
                print("Humidity :{:.2f}%".format(humidity))
                print()
            time.sleep(0.5)
