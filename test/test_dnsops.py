import unittest

from zeke import dnsops


class MockDnsResult(object):
    def __init__(self, host, port):
        self.target = host
        self.port = port


class TestDns(unittest.TestCase):
    def test_clean_host(self):
        r1 = MockDnsResult('zk.domain.com.', 1234)
        actual = dnsops._clean_host(r1)
        self.assertEqual(actual, 'zk.domain.com:1234')