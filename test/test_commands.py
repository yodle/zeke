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
