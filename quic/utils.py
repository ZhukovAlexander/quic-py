class Alarm:
    """
    Simple alarm implementation

    """

    def __init__(self, loop, on_fired=lambda: None):
        self._callback = on_fired
        self._loop = loop
        self._handler = None

    def set(self, when):
        self._handler = self._loop.call_at(when, self._callback)

    def reset(self):
        self._handler.cancel()


FLOAT_16_EXPONENT_BITS = 5
FLOAT_16_MANTISSA_BITS = 16 - FLOAT_16_EXPONENT_BITS  # 11
FLOAT_16_MANTISSA_EFFECTIVE_BITS = FLOAT_16_MANTISSA_BITS + 1  # 12
FLOAT_16_MANTISSA_EFFECTIVE_VALUE = 1 << FLOAT_16_MANTISSA_EFFECTIVE_BITS
FLOAT_16_MAX_VALUE = 0x3FFC0000000


def read_ufloat16(buffer):
    value = read_int(2, buffer)
    if value < FLOAT_16_MANTISSA_EFFECTIVE_VALUE:
        return value

    exponent = value >> FLOAT_16_MANTISSA_BITS
    exponent -= 1
    value -= exponent << FLOAT_16_MANTISSA_BITS
    res = value << exponent
    return min(res, FLOAT_16_MAX_VALUE)


def write_ufloat16(value):
    res = 0
    if value < FLOAT_16_MANTISSA_EFFECTIVE_VALUE:
        res = value
    elif value > FLOAT_16_MAX_VALUE:
        res = 0x3FFC0000000
    else:
        exponent = 0
        offset = 16
        while offset >= 1:
            if value >= (1 << (FLOAT_16_MANTISSA_BITS + offset)):
                exponent += offset
                value >>= offset

        res = int(value) + (exponent << FLOAT_16_MANTISSA_BITS)
    return res.to_bytes(2, 'big')


def read_int(size, buffer):
    return int.from_bytes(buffer.read1(size), 'big')


def write_int(size, i):
    return i.to_bytes(size, 'big')
