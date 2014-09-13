import hashlib
import unittest

from c2c_verifier.encoder import c2c_encode_a


class c2c_encode_a_tests (unittest.TestCase):

    @unittest.skip('Exposes zbase32 bug\n\n*** FIXME: File a bug with the upstream dependency.')
    def test_encode_empty(self):
        self.assertEqual('a', c2c_encode_a(''))

    def test_encode_hash(self):
        hashbits = hashlib.sha256('test input').digest()
        actual = c2c_encode_a(hashbits[:16])
        expected = 'auz9g6fqtip349nc88rhw9wtx4h'

        self.assertEqual(expected, actual)
