import unittest

from zeke import zeke


class TestZeke(unittest.TestCase):
    def test_discover_option_parsed(self):
        args = ['--discover']
        results = zeke.parse_options(args)
        self.assertTrue(results['discover'])

    def test_get_option_parsed_long(self):
        args = ['--get', 'a/b/c']
        results = zeke.parse_options(args)
        self.assertEqual(results['get'], 'a/b/c')

    def test_get_option_parsed_short(self):
        args = ['-g', 'a/b/c']
        results = zeke.parse_options(args)
        self.assertEqual(results['get'], 'a/b/c')

    def test_address_parsed_long(self):
        args = ['--address', 'host:port']
        results = zeke.parse_options(args)
        self.assertEqual(results['address'], 'host:port')

    def test_address_parsed_short(self):
        args = ['-a', 'host:port']
        results = zeke.parse_options(args)
        self.assertEqual(results['address'], 'host:port')