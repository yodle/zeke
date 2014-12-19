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
            ['/c/d', b'4']
        ]
        result = commands._format_pairs_for_output(pairs)
        expected = '["/a/b", "3"]\n["/c/d", "4"]'
        self.assertEqual(result, expected)

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