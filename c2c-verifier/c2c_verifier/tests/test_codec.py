import hashlib
import unittest

from OpenSSL.crypto import X509

from c2c_verifier.codec import get_certificate_hash_encoding_a, decode_a, encode_a


class encode_a_tests (unittest.TestCase):

    @unittest.skip('Exposes zbase32 bug\n\n*** FIXME: File a bug with the upstream dependency.')
    def test_encode_empty(self):
        self.assertEqual('a', encode_a(''))

    def test_encode_hash(self):
        hashbits = hashlib.sha256('test input').digest()
        actual = encode_a(hashbits[:16])
        expected = 'auz9g6fqtip349nc88rhw9wtx4h'

        self.assertEqual(expected, actual)


class decode_a_tests (unittest.TestCase):

    @unittest.skip('Exposes zbase32 bug\n\n*** FIXME: File a bug with the upstream dependency.')
    def test_decode_empty(self):
        self.assertEqual('', decode_a('a'))

    def test_decode_hash(self):
        encstr = 'auz9g6fqtip349nc88rhw9wtx4h'
        actual = decode_a(encstr)
        expected = hashlib.sha256('test input').digest()[:16]

        self.assertEqual(expected, actual)


class get_certificate_hash_encoding_a_tests (unittest.TestCase):

    def test_empty_x509_hash(self):
        cert = X509()
        expected = 'ajwehjgcua5ak6ykeqe8zhrysqo'

        self.assertEqual(expected, get_certificate_hash_encoding_a(cert))

