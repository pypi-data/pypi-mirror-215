# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_mpl3115a2 import mpl3115a2

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
mpl = mpl3115a2.MPL3115A2(i2c)

mpl.oversample_ratio = mpl3115a2.OS4

while True:
    for oversample_ratio in mpl3115a2.oversample_ratio_values:
        print("Current Oversample ratio setting: ", mpl.oversample_ratio)
        for _ in range(10):
            press = mpl.pressure
            print("Pressure: {:.2f}Hpa".format(mpl.pressure))
            print()
            time.sleep(0.5)
        mpl.oversample_ratio = oversample_ratio
