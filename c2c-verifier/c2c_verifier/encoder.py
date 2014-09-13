import zbase32


def c2c_encode_a(bits):
    return 'a' + zbase32.b2a(bits)
