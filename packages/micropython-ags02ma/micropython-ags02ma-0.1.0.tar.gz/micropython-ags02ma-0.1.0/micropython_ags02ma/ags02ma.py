# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`ags02ma`
================================================================================

MicroPython Driver for the AGS02MA TVOC sensor


* Author(s): ladyada, Jose D. Montoya


"""

import time
import struct
from micropython import const


__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/MicroPython_AGS02MA.git"


_DATA = const(0x00)
_AGS02MA_CRC8_POLYNOMIAL = const(0x31)
_AGS02MA_CRC8_INIT = const(0xFF)


class AGS02MA:
    """Driver for the AGS02MA Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the AGS02MA is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x69`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`AGS02MA` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        import ags02ma

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(sda=Pin28), scl=Pin(3))
        ags02ma = ags02ma.AGS02MA(i2c)

    Now you have access to the attributes

    .. code-block:: python

    """

    def __init__(self, i2c, address: int = 0x1A) -> None:
        self._i2c = i2c
        self._addr = address

        self._check_device()

    def _check_device(self):
        return self._read_reg(0x11, 30)

    @property
    def TVOC(self) -> float:
        """The calculated Total Volatile Organic Compound measurement, in ppb"""
        val = self._read_reg(_DATA, 1500)

        return val & 0xFFFFFF

    def _read_reg(self, addr: int, delayms: int) -> int:
        """Read a register

        :param int addr: The address to read
        :param int delayms: The delay between writes and reads, in milliseconds

        :raises RunTimeError: When CRC check have failed.

        """
        data = bytearray(5)
        self._i2c.writeto(self._addr, bytes([addr]))
        time.sleep(delayms / 1000)
        self._i2c.readfrom_into(self._addr, data)

        if self._generate_crc(data) != 0:
            raise RuntimeError("CRC check failed")

        val, _ = struct.unpack(">IB", data)
        return val

    @property
    def gas_resistance(self) -> float:
        """The resistance of the MEMS gas sensor in 0.1 Kohm"""
        return self._read_reg(0x20, 1500) * 100

    @staticmethod
    def _generate_crc(data: bytearray) -> int:
        """8-bit CRC algorithm for checking data

        :param int data: The data to generate a CRC for
        """

        crc = _AGS02MA_CRC8_INIT

        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc <<= 1
            crc &= 0xFF
        return crc & 0xFF
