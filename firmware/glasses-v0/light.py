# The VEML7700 light sensor on the QT Py's STEMMA QT port, read directly. (Adafruit's library
# is too big to fit in this board's memory next to the rest of the program.)

import board

ADDR = 0x10
# Gain 1/8 and 25 ms per reading: the lowest sensitivity, so full sun doesn't overload it.
# Each count is 2.1504 lux (the same figure Adafruit's library uses), up to about 140,000 lux.
CONFIG = 0x1300    # gain 1/8 in bits 12-11, 25 ms in bits 9-6, power on in bit 0
LUX_PER_COUNT = 2.1504

i2c = board.STEMMA_I2C() if hasattr(board, "STEMMA_I2C") else board.I2C()
_cmd = bytearray(3)
_reg = bytearray(1)
_data = bytearray(2)


def start():
    # Raises OSError if the sensor doesn't answer.
    _cmd[0] = 0
    _cmd[1] = CONFIG & 0xFF
    _cmd[2] = CONFIG >> 8
    while not i2c.try_lock():
        pass
    try:
        i2c.writeto(ADDR, _cmd)
    finally:
        i2c.unlock()


def read():
    # Light level in lux. Raises OSError if the sensor doesn't answer.
    _reg[0] = 4
    while not i2c.try_lock():
        pass
    try:
        i2c.writeto_then_readfrom(ADDR, _reg, _data)
    finally:
        i2c.unlock()
    return (_data[0] | (_data[1] << 8)) * LUX_PER_COUNT
