import hashlib
import unittest

from c2c_verifier.codec import encode_a


class encode_a_tests (unittest.TestCase):

    @unittest.skip('Exposes zbase32 bug\n\n*** FIXME: File a bug with the upstream dependency.')
    def test_encode_empty(self):
        self.assertEqual('a', encode_a(''))

    def test_encode_hash(self):
        hashbits = hashlib.sha256('test input').digest()
        actual = encode_a(hashbits[:16])
        expected = 'auz9g6fqtip349nc88rhw9wtx4h'

        self.assertEqual(expected, actual)
