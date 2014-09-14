_C2C_HASH_ALGORITHM = 'sha256'


def get_cert_hash(cert):
    '''Given an OpenSSL.crypto.X509 instance, return it's c2c hash.'''
    return cert.digest(_C2C_HASH_ALGORITHM).replace(':', '').decode('hex')
