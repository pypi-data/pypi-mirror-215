# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`wsentids`
================================================================================

MicroPython library for the WSEN WSEN-TIDS temperature Sensor


* Author(s): Jose D. Montoya


"""

from math import ceil
from collections import namedtuple
from micropython import const
from micropython_wsentids.i2c_helpers import CBits, RegisterStruct

__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/MicroPython_WSENTIDS.git"

_WHO_AM_I = const(0x01)
_TEMP_HIGH_LIMIT = const(0x02)
_TEMP_LOW_LIMIT = const(0x03)
_CTRL_REG4 = const(0x04)
_STATUS = const(0x05)
_TEMP = const(0x06)
_SOFT_RESET = const(0x0C)

_RESOLUTION = const(0.64)

BDU_DISABLED = const(0b0)
BDU_ENABLED = const(0b1)
block_data_update_values = (BDU_DISABLED, BDU_ENABLED)

RATE_25_HZ = const(0b00)
RATE_50_HZ = const(0b01)
RATE_100_HZ = const(0b10)
RATE_200_HZ = const(0b11)
data_rate_values = (RATE_25_HZ, RATE_50_HZ, RATE_100_HZ, RATE_200_HZ)

CONTINUOUS_DISABLED = const(0b0)
CONTINUOUS_ENABLED = const(0b1)
continuous_mode_values = (CONTINUOUS_DISABLED, CONTINUOUS_ENABLED)

AlertStatus = namedtuple("AlertStatus", ["high_alert", "low_alert"])


class WSENTIDS:
    """Driver for the WSENTIDS Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the WSENTIDS is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x69`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`WSENTIDS` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_wsentids import wsentids

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        wsentids = wsentids.WSENTIDS(i2c)

    Now you have access to the attributes

    .. code-block:: python

    """

    _device_id = RegisterStruct(_WHO_AM_I, "B")
    _raw_high_limit = RegisterStruct(_TEMP_HIGH_LIMIT, "B")
    _raw_low_limit = RegisterStruct(_TEMP_LOW_LIMIT, "B")
    _temperature = RegisterStruct(_TEMP, "H")

    _block_data_update = CBits(1, _CTRL_REG4, 6)
    _data_rate = CBits(2, _CTRL_REG4, 4)
    _add_inc = CBits(1, _CTRL_REG4, 3)
    _continuous_mode = CBits(1, _CTRL_REG4, 2)

    _high_alert = CBits(1, _STATUS, 1)
    _low_alert = CBits(1, _STATUS, 2)

    _soft_reset = CBits(1, _SOFT_RESET, 1)

    def __init__(self, i2c, address: int = 0x3F) -> None:
        self._i2c = i2c
        self._address = address
        self._block_data_update = True
        self._continuous_mode = True
        self._add_inc = True

        if self._device_id != 0xA0:
            raise RuntimeError("Failed to find WSENTIDS")

    @property
    def high_limit(self) -> int:
        """The high temperature limit in Celsius. When the measured temperature exceeds this
        value, the `high_alert` attribute of the `alert_status` property will be True.
        """

        return int((self._raw_high_limit - 63) * _RESOLUTION)

    @high_limit.setter
    def high_limit(self, value: float) -> None:
        if value > 122.8 or value < -39.68:
            raise ValueError("Value must be a valid limit")
        self._raw_high_limit = ceil(value / _RESOLUTION) + 63

    @property
    def low_limit(self) -> int:
        """The low  temperature limit in Celsius. When the measured temperature goes below
        this value, the `low_alert` attribute of the `alert_status` property will be True.
        """

        return int((self._raw_low_limit - 63) * _RESOLUTION)

    @low_limit.setter
    def low_limit(self, value: float) -> None:
        self._raw_low_limit = ceil(value / _RESOLUTION) + 63

    @property
    def block_data_update(self) -> str:
        """
        Sensor block_data_update used to inhibit the output
        register update between the reading of the upper
        and lower register parts. In default mode (BDU = ‘0’), the
        lower and upper register parts are updated continuously.
        it is recommended to set the BDU bit to ‘1’. In this way,
        after the reading of the lower (upper) register part,
        the content of that output register is not updated until
        the upper (lower) part is read also.

        +-----------------------------------+-----------------+
        | Mode                              | Value           |
        +===================================+=================+
        | :py:const:`wsentids.BDU_DISABLED` | :py:const:`0b0` |
        +-----------------------------------+-----------------+
        | :py:const:`wsentids.BDU_ENABLED`  | :py:const:`0b1` |
        +-----------------------------------+-----------------+
        """
        values = ("BDU_DISABLED", "BDU_ENABLED")
        return values[self._block_data_update]

    @block_data_update.setter
    def block_data_update(self, value: int) -> None:
        if value not in block_data_update_values:
            raise ValueError("Value must be a valid block_data_update setting")
        self._block_data_update = value

    @property
    def data_rate(self) -> str:
        """
        Sensor data_rate

        +----------------------------------+------------------+
        | Mode                             | Value            |
        +==================================+==================+
        | :py:const:`wsentids.RATE_25_HZ`  | :py:const:`0b00` |
        +----------------------------------+------------------+
        | :py:const:`wsentids.RATE_50_HZ`  | :py:const:`0b01` |
        +----------------------------------+------------------+
        | :py:const:`wsentids.RATE_100_HZ` | :py:const:`0b10` |
        +----------------------------------+------------------+
        | :py:const:`wsentids.RATE_200_HZ` | :py:const:`0b11` |
        +----------------------------------+------------------+
        """
        values = ("RATE_25_HZ", "RATE_50_HZ", "RATE_100_HZ", "RATE_200_HZ")
        return values[self._data_rate]

    @data_rate.setter
    def data_rate(self, value: int) -> None:
        if value not in data_rate_values:
            raise ValueError("Value must be a valid data_rate setting")
        self._continuous_mode = False
        self._data_rate = value
        self._continuous_mode = True

    @property
    def continuous_mode(self) -> str:
        """
        Sensor continuous_mode

        The continuous mode constantly samples new temperature measurements
        and writes the data to the temperature data registers.

        The power-down mode can be configured by disabling :attr:`continuous_mode`
        In power-down mode, New measurements are not performed during this mode.
        The :attr:`temperature` contains the last sampled temperature value
        before going into power-down mode.
        Sensor is in power-down mode by default after the power-up sequence.


        +------------------------------------------+-----------------+
        | Mode                                     | Value           |
        +==========================================+=================+
        | :py:const:`wsentids.CONTINUOUS_DISABLED` | :py:const:`0b0` |
        +------------------------------------------+-----------------+
        | :py:const:`wsentids.CONTINUOUS_ENABLED`  | :py:const:`0b1` |
        +------------------------------------------+-----------------+
        """
        values = ("CONTINUOUS_DISABLED", "CONTINUOUS_ENABLED")
        return values[self._continuous_mode]

    @continuous_mode.setter
    def continuous_mode(self, value: int) -> None:
        if value not in continuous_mode_values:
            raise ValueError("Value must be a valid continuous_mode setting")
        self._continuous_mode = value

    @property
    def temperature(self) -> float:
        """
        Return the sensor temperature
        """
        return self._temperature * 0.01

    @property
    def alert_status(self):
        """The current triggered status of the high and low temperature alerts as a AlertStatus
        named tuple with attributes for the triggered status of each alert.

        .. code-block :: python

            import time
            from machine import Pin, I2C
            from micropython_wsentids import wsentids

            i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
            wsen = wsentids.WSENTIDS(i2c)

            wsen.low_limit = 20
            wsen.high_limit = 23

            print("High limit", wsen.high_limit)
            print("Low limit", wsen.low_limit)


            while True:
                print("Temperature: {:.1f}C".format(wsen.temperature))
                alert_status = tmp.alert_status
                if alert_status.high_alert:
                    print("Temperature above high set limit!")
                if alert_status.low_alert:
                    print("Temperature below low set limit!")
                print("Low alert:", alert_status.low_alert)
                time.sleep(1)

        """

        return AlertStatus(high_alert=self._high_alert, low_alert=self._low_alert)

    def reset(self) -> None:
        """
        Resets the sensor
        """
        self._soft_reset = True
