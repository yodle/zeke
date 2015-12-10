import unittest
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# the abomination below is used to detect where 'print' is defined so we can mock it
# the builtins module changed from __builtin__ to builtins in the python 2.x -> 3.x transition
builtins_name = 'builtins'
try:
    import builtins
except ImportError:
    builtins_name = '__builtin__'

import sys
from zeke import commands, zookeeper


class TestCommands(unittest.TestCase):
    @patch(builtins_name + '.print')
    @patch('zeke.commands.dnsops')
    def test_command_discover(self, mock_dnsops, mock_print):
        mock_dnsops.discover_zk_via_dns.return_value = ['host.example.com:1234']
        commands.discover()
        mock_dnsops.discover_zk_via_dns.assert_called_once_with()
        mock_print.assert_called_once_with('host.example.com:1234')

    @patch('zeke.commands.dnsops')
    def test_get_zk_hosts_given_host_returns_it(self, mock_dnsops):
        result = commands.get_zk_hosts('host:123')
        self.assertEqual(result, ['host:123'])
        self.assertFalse(mock_dnsops.discover_zk_via_dns.called)

    @patch('zeke.commands.dnsops')
    def test_get_zk_hosts_without_host_calls_discover(self, mock_dnsops):
        mock_dnsops.discover_zk_via_dns.return_value = ['host.example.com:1234']
        result = commands.get_zk_hosts(None)
        self.assertEqual(result, ['host.example.com:1234'])
        mock_dnsops.discover_zk_via_dns.assert_called_once_with()

    @patch(builtins_name + '.print')
    @patch('zeke.commands.zookeeper.Zookeeper')
    def test_print_value_success(self, mock_zookeeper, mock_print):
        mock_kazoo = Mock()
        mock_kazoo.get_value.return_value = b'value'
        mock_zookeeper.return_value = mock_kazoo

        commands.print_value('key', 'host:123')
        mock_zookeeper.assert_called_once_with(['host:123'])
        mock_kazoo.get_value.assert_called_once_with('key')
        mock_print.assert_called_once_with('value')

    @patch(builtins_name + '.print')
    @patch('zeke.commands.zookeeper.Zookeeper')
    def test_print_value_with_exception(self, mock_zookeeper, mock_print):
        mock_kazoo = Mock()
        mock_kazoo.get_value.side_effect = zookeeper.NoNodeError
        mock_zookeeper.return_value = mock_kazoo

        with self.assertRaises(commands.CommandError):
            commands.print_value('key', 'host:123')
        self.assertTrue(mock_print.called)

    def test_format_pairs_for_output(self):
        pairs = [
            ['/a/b', b'3'],
            ['/c/d', None]
        ]
        result = commands._format_pairs_for_output(pairs)
        expected = '["/a/b", "3"]\n["/c/d", ""]'
        self.assertEqual(result, expected)

    def test_clean_value_decodes_string_properly(self):
        self.assertEqual("abc", commands._clean_value(b'abc'))

    def test_clean_value_returns_blank_string_for_none(self):
        self.assertEqual("", commands._clean_value(None))

    def test_clean_value_does_base64_conversion(self):
        badutf8 = b'\xb7'
        self.assertEqual("base64:tw==", commands._clean_value(badutf8))

    def test_convert_pair_to_json(self):
        pair = ("key", "value")
        self.assertEqual('["key", "value"]', commands._convert_pair_to_json(pair))

    @patch(builtins_name + '.print')
    def test_convert_pair_to_json_on_error(self, mock_print):
        bad = b'\xb7'
        pair = ("key", bad)

        # raises UnicodeDecodeError for python2, TypeError in python3
        with self.assertRaises((TypeError, UnicodeDecodeError)):
            commands._convert_pair_to_json(pair)
        mock_print.assert_called_once_with("Unable to encode value for key: key\n", file=sys.stderr)

    def test_get_sorted_list_of_descendants_sorts_results(self):
        mock_zk = Mock()
        mock_zk.get_descendants_of_node.return_value = {'/a/c', '/a/b', '/a/d'}
        commands._get_sorted_list_of_descendants_with_values(mock_zk, '/a')
        mock_zk.get_values.assert_called_once_with(['/a/b', '/a/c', '/a/d'])

    @patch(builtins_name + '.print')
    @patch('zeke.commands.zookeeper.Zookeeper')
    def test_dump_prints_results_properly(self, mock_zookeeper, mock_print):
        mock_zk = Mock()
        mock_zk.get_descendants_of_node.return_value = {'/a/b'}
        mock_zk.get_values.return_value = [('/a/b', b'1')]
        mock_zookeeper.return_value = mock_zk

        commands.dump('/a', 'host')
        expected = '["/a/b", "1"]'
        mock_print.assert_called_once_with(expected)

    @patch(builtins_name + '.print')
    @patch('zeke.commands.zookeeper.Zookeeper')
    def test_dump_prints_error_on_no_node_error(self, mock_zookeeper, mock_print):
        mock_zk = Mock()
        mock_zk.get_descendants_of_node.side_effect = zookeeper.NoNodeError
        mock_zookeeper.return_value = mock_zk

        with self.assertRaises(commands.CommandError):
            commands.dump('/a', 'host')
        mock_print.assert_called_once_with('Node not found', file=sys.stderr)

    @patch('zeke.commands.zookeeper.Zookeeper')    
    def test_delete_calls_zk(self, mock_zookeeper):
        mock_zk = Mock()
        mock_zookeeper.return_value = mock_zk
        
        commands.delete('key', 'host')
        mock_zk.delete.assert_called_once_with('key', recursive = False)

    @patch('zeke.commands.zookeeper.Zookeeper')    
    def test_delete_does_nothing_on_no_node_error(self, mock_zookeeper):
        mock_zk = Mock()
        mock_zk.delete.side_effect = zookeeper.NoNodeError
        mock_zookeeper.return_value = mock_zk

        commands.delete('key', 'host')

    @patch(builtins_name + '.print')    
    @patch('zeke.commands.zookeeper.Zookeeper')
    def test_delete_fails_when_not_empty(self, mock_zookeeper, mock_print):
        mock_zk = Mock()
        mock_zk.delete.side_effect = zookeeper.NotEmptyError
        mock_zookeeper.return_value = mock_zk

        with self.assertRaises(commands.CommandError):
            commands.delete('key', 'host')
        mock_print.assert_called_once_with('Tried to delete: key but node contains child nodes', file=sys.stderr)

    @patch('zeke.commands.zookeeper.Zookeeper')
    def test_purge_calls_zk(self, mock_zookeeper):
        mock_zk = Mock()
        mock_zookeeper.return_value = mock_zk

        commands.purge('key', 'host')
        mock_zk.delete.assert_called_once_with('key', recursive = True)

    @patch('zeke.commands.zookeeper.Zookeeper')
    def test_purge_does_nothing_on_no_node_error(self, mock_zookeeper):
        mock_zk = Mock()
        mock_zk.delete.side_effect = zookeeper.NoNodeError
        mock_zookeeper.return_value = mock_zk

        commands.purge('key', 'host')
        
    def test_parse_line_raises_command_error_for_bad_json(self):
        with self.assertRaises(commands.CommandError):
            commands._parse_line('some line that is not json')

    def test_parse_line_raises_when_given_too_few_items(self):
        with self.assertRaises(commands.CommandError):
            commands._parse_line('["/a/b"]')

    def test_parse_line_raises_when_given_too_many_items(self):
        with self.assertRaises(commands.CommandError):
            commands._parse_line('["/a/b", "val", "something extra"]')

    def test_parse_line_raises_when_given_dictionary(self):
        with self.assertRaises(commands.CommandError):
            commands._parse_line('{"hello": "there", "more": "stuff"}')

    def test_parse_line_converts_items_to_bytes(self):
        results = commands._parse_line('["/a", 3]')
        self.assertEqual(results[1], b"3")

    def test_parse_line_converts_base64_to_binary(self):
        results = commands._parse_line('["/a", "base64:tw=="]')
        self.assertEqual(results[1], b'\xb7')

    def test_parse_line_works_properly_given_normal_input(self):
        results = commands._parse_line('["/a", "hello"]')
        self.assertEqual(("/a", b"hello"), results)

    def test_parse_all_lines_can_parse_multiple_lines(self):
        lines = [
            '["/a", "hello"]',
            '["/b", "there"]'
        ]
        results = commands._parse_all_lines(lines)
        expected = [
            ("/a", b"hello"),
            ("/b", b"there")
        ]
        self.assertEqual(results, expected)

    def test_load_pairs_calls_zk_set_or_create_properly(self):
        zk = Mock()
        pairs = [
            ("/a", "hello"),
            ("/b", "there")
        ]
        commands._load_pairs(zk, pairs)
        zk.set_or_create.assert_any_call("/a", "hello")
        zk.set_or_create.assert_any_call("/b", "there")
        self.assertEqual(zk.set_or_create.call_count, 2)

    @patch('zeke.commands.sys.stdin')
    @patch('zeke.commands.zookeeper.Zookeeper')
    def test_load_parses_lines_from_stdin_and_loads_them(self, mock_zookeeper, mock_stdin):
        zk = Mock()
        mock_zookeeper.return_value = zk
        mock_stdin.__iter__.return_value = ['["/a", "hey"]', '["/b", "there"]']

        commands.load('host:1234')

        zk.set_or_create.assert_any_call("/a", b"hey")
        zk.set_or_create.assert_any_call("/b", b"there")
        self.assertEqual(zk.set_or_create.call_count, 2)

