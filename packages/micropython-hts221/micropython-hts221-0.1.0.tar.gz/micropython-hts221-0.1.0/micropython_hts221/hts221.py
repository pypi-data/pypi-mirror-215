# SPDX-FileCopyrightText: 2020 Bryan Siepert for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`hts221`
================================================================================

MicroPython Driver for the HTS221 Humidity Sensor


* Author(s): Jose D. Montoya


"""

from micropython import const
from micropython_hts221.i2c_helpers import CBits, RegisterStruct


__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/MicroPython_HTS221.git"


_WHO_AM_I = const(0x0F)

_CTRL_REG1 = const(0x20)
_CTRL_REG2 = const(0x21)
_CTRL_REG3 = const(0x22)
_STATUS_REG = const(0x27)
# some addresses are anded to set the  top bit so that multi-byte reads will work
_HUMIDITY_OUT_L = const(0x28 | 0x80)  # Humidity output register (LSByte)
_TEMP_OUT_L = const(0x2A | 0x80)  # Temperature output register (LSByte)

_H0_RH_X2 = const(0x30)  # Humididy calibration LSB values
_H1_RH_X2 = const(0x31)  # Humididy calibration LSB values

_T0_DEGC_X8 = const(0x32)  # First byte of T0, T1 calibration values
_T1_DEGC_X8 = const(0x33)  # First byte of T0, T1 calibration values
_T1_T0_MSB = const(0x35)  # Top 2 bits of T0 and T1 (each are 10 bits)

_H0_T0_OUT = const(0x36 | 0x80)  # Humididy calibration Time 0 value
_H1_T1_OUT = const(0x3A | 0x80)  # Humididy calibration Time 1 value

_T0_OUT = const(0x3C | 0x80)  # T0_OUT LSByte
_T1_OUT = const(0x3E | 0x80)  # T1_OUT LSByte


ONE_SHOT = const(0b00)
RATE_1_HZ = const(0b01)
RATE_7_HZ = const(0b10)
RATE_12_5_HZ = const(0b11)
data_rate_values = (ONE_SHOT, RATE_1_HZ, RATE_7_HZ, RATE_12_5_HZ)

BDU_DISABLED = const(0b0)
BDU_ENABLED = const(0b1)
block_data_update_values = (BDU_DISABLED, BDU_ENABLED)


class HTS221:
    """Driver for the HTS221 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the HTS221 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x5F`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`HTS221` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_hts221 import hts221

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        hts221 = hts221.HTS221(i2c)

    Now you have access to the attributes

    .. code-block:: python

        hum = hts.relative_humidity

    """

    _device_id = RegisterStruct(_WHO_AM_I, "<B")
    _boot_bit = CBits(1, _CTRL_REG2, 7)
    enabled = CBits(1, _CTRL_REG1, 7)
    """Controls the power down state of the sensor. Setting to `False` will shut the sensor down"""
    _data_rate = CBits(2, _CTRL_REG1, 0)
    _block_data_update = CBits(1, _CTRL_REG1, 2)

    _one_shot_bit = CBits(1, _CTRL_REG2, 0)
    _raw_temperature = RegisterStruct(_TEMP_OUT_L, "<h")
    _raw_humidity = RegisterStruct(_HUMIDITY_OUT_L, "<h")

    _t0_deg_c_x8_lsbyte = CBits(8, _T0_DEGC_X8, 0)
    _t1_deg_c_x8_lsbyte = CBits(8, _T1_DEGC_X8, 0)
    _t1_t0_deg_c_x8_msbits = CBits(4, _T1_T0_MSB, 0)

    _t0_out = RegisterStruct(_T0_OUT, "<h")
    _t1_out = RegisterStruct(_T1_OUT, "<h")

    _h0_rh_x2 = RegisterStruct(_H0_RH_X2, "<B")
    _h1_rh_x2 = RegisterStruct(_H1_RH_X2, "<B")

    _h0_t0_out = RegisterStruct(_H0_T0_OUT, "<h")
    _h1_t0_out = RegisterStruct(_H1_T1_OUT, "<h")

    def __init__(self, i2c, address: int = 0x5F) -> None:
        self._i2c = i2c
        self._address = address

        if self._device_id != 0xBC:
            raise RuntimeError("Failed to find HTS221")

        self._boot()
        self.enabled = True
        self.data_rate = RATE_12_5_HZ
        self._block_data_update = BDU_ENABLED

        t1_t0_msbs = self._t1_t0_deg_c_x8_msbits
        self.calib_temp_value_0 = self._t0_deg_c_x8_lsbyte
        self.calib_temp_value_0 |= (t1_t0_msbs & 0b0011) << 8

        self.calibrated_value_1 = self._t1_deg_c_x8_lsbyte
        self.calibrated_value_1 |= (t1_t0_msbs & 0b1100) << 6

        self.calib_temp_value_0 >>= 3  # divide by 8 to remove x8
        self.calibrated_value_1 >>= 3  # divide by 8 to remove x8

        self.calib_temp_meas_0 = self._t0_out
        self.calib_temp_meas_1 = self._t1_out

        self.calib_hum_value_0 = self._h0_rh_x2
        self.calib_hum_value_0 >>= 1  # divide by 2 to remove x2

        self.calib_hum_value_1 = self._h1_rh_x2
        self.calib_hum_value_1 >>= 1  # divide by 2 to remove x2

        self.calib_hum_meas_0 = self._h0_t0_out
        self.calib_hum_meas_1 = self._h1_t0_out

    def _boot(self) -> None:
        self._boot_bit = True
        while self._boot_bit:
            pass

    @property
    def relative_humidity(self) -> float:
        """The current relative humidity measurement in %rH"""
        calibrated_value_delta = self.calib_hum_value_1 - self.calib_hum_value_0
        calibrated_measurement_delta = self.calib_hum_meas_1 - self.calib_hum_meas_0

        calibration_value_offset = self.calib_hum_value_0
        calibrated_measurement_offset = self.calib_hum_meas_0
        zeroed_measured_humidity = self._raw_humidity - calibrated_measurement_offset

        correction_factor = calibrated_value_delta / calibrated_measurement_delta

        adjusted_humidity = (
            zeroed_measured_humidity * correction_factor + calibration_value_offset
        )

        return adjusted_humidity

    @property
    def temperature(self) -> float:
        """The current temperature measurement in Celsius"""

        calibrated_value_delta = self.calibrated_value_1 - self.calib_temp_value_0
        calibrated_measurement_delta = self.calib_temp_meas_1 - self.calib_temp_meas_0

        calibration_value_offset = self.calib_temp_value_0
        calibrated_measurement_offset = self.calib_temp_meas_0
        zeroed_measured_temp = self._raw_temperature - calibrated_measurement_offset

        correction_factor = calibrated_value_delta / calibrated_measurement_delta

        adjusted_temp = (
            zeroed_measured_temp * correction_factor
        ) + calibration_value_offset

        return adjusted_temp

    @property
    def data_rate(self) -> str:
        """
        Sensor data_rate

        Note that setting :attr:`data_rate` to ONE_SHOT will cause
        :attr:`relative_humidity` and :attr:`temperature` measurements to only
        update when :meth:`take_measurements` is called.

        +---------------------------------+------------------+
        | Mode                            | Value            |
        +=================================+==================+
        | :py:const:`hts221.ONE_SHOT`     | :py:const:`0b00` |
        +---------------------------------+------------------+
        | :py:const:`hts221.RATE_1_HZ`    | :py:const:`0b01` |
        +---------------------------------+------------------+
        | :py:const:`hts221.RATE_7_HZ`    | :py:const:`0b10` |
        +---------------------------------+------------------+
        | :py:const:`hts221.RATE_12_5_HZ` | :py:const:`0b11` |
        +---------------------------------+------------------+
        """
        values = ("ONE_SHOT", "RATE_1_HZ", "RATE_7_HZ", "RATE_12_5_HZ")
        return values[self._data_rate]

    @data_rate.setter
    def data_rate(self, value: int) -> None:
        if value not in data_rate_values:
            raise ValueError("Value must be a valid data_rate setting")
        self._data_rate = value

    def take_measurements(self) -> None:
        """Update the value of :attr:`relative_humidity` and :attr:`temperature` by taking a single
        measurement. Only meaningful if :attr:`data_rate` is set to ``ONE_SHOT``"""
        self._one_shot_bit = True
        while self._one_shot_bit:
            pass

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

        +---------------------------------+-----------------+
        | Mode                            | Value           |
        +=================================+=================+
        | :py:const:`hts221.BDU_DISABLED` | :py:const:`0b0` |
        +---------------------------------+-----------------+
        | :py:const:`hts221.BDU_ENABLED`  | :py:const:`0b1` |
        +---------------------------------+-----------------+
        """
        values = ("BDU_DISABLED", "BDU_ENABLED")
        return values[self._block_data_update]

    @block_data_update.setter
    def block_data_update(self, value: int) -> None:
        if value not in block_data_update_values:
            raise ValueError("Value must be a valid block_data_update setting")
        self._block_data_update = value
