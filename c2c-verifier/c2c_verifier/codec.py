import zbase32


def decode_a(encstr):
    assert encstr.startswith('a'), "Precondition failure: {!r} does not start with 'a'.".format(encstr)
    return zbase32.a2b(encstr[1:])


def encode_a(bits):
    return 'a' + zbase32.b2a(bits)


def get_certificate_hash_encoding_a(cert):
    return encode_a(cert.digest('sha256').replace(':', '').decode('hex')[16:])
