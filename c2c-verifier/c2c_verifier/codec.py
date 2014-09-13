import zbase32


def encode_a(bits):
    return 'a' + zbase32.b2a(bits)
