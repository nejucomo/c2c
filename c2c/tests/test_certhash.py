import unittest

from OpenSSL.crypto import X509

from c2c.certhash import get_cert_hash


class LiteralChainVerifierTests (unittest.TestCase):

    def test_default_hash(self):
        expected = (b'Ph\xd4\xd7"\xa1\xd4\xee\xd1\xe8\xf9\xe6\x17\xe2\xa6\\'
                    + b'M\x11\xc4\x99\x93\xc6\xf0\xaf\x01Hr\x0f~\x10\x16t')
        actual = get_cert_hash(X509())

        self.assertEqual(expected, actual)
