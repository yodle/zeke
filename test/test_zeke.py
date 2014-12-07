import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

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

    def test_set_gets_key_and_value_short(self):
        args = ['-s', 'a', 'b']
        results = zeke.parse_options(args)
        self.assertEqual(results['set'], ['a', 'b'])

    def test_set_gets_key_and_value_long(self):
        args = ['--set', 'a', 'b']
        results = zeke.parse_options(args)
        self.assertEqual(results['set'], ['a', 'b'])

    @patch('zeke.commands.discover')
    def test_dispatch_to_discover(self, discover_mock):
        zeke.dispatch(self.create_parser_results({'discover': True}))
        discover_mock.assert_called_once_with()

    @patch('zeke.commands.print_value')
    def test_dispatch_to_print_value(self, print_value_mock):
        zeke.dispatch(self.create_parser_results({'get': 'keyname'}))
        print_value_mock.assert_called_once_with('keyname', None)

    @patch('zeke.commands.print_value')
    def test_dispatch_uses_custom_address_if_provided(self, print_value_mock):
        zeke.dispatch(self.create_parser_results({'get': 'keyname', 'address': 'host'}))
        print_value_mock.assert_called_once_with('keyname', 'host')

    @patch('zeke.commands.set_value')
    def test_dispatch_to_set_value(self, set_value_mock):
        zeke.dispatch(self.create_parser_results({'set': ('key', 'value')}))
        set_value_mock.assert_called_once_with('key', 'value', None)

    @patch('zeke.commands.set_value')
    def test_dispatch_to_set_value_with_custom_address(self, set_value_mock):
        zeke.dispatch(self.create_parser_results({'set': ('key', 'value'), 'address': 'host'}))
        set_value_mock.assert_called_once_with('key', 'value', 'host')

    @staticmethod
    def create_parser_results(args):
        results = {
            'discover': False,
            'get': None,
            'address': None,
            'set': None
        }
        results.update(args)
        return results