import unittest
from unittest.mock import Mock

from zeke import commands, zookeeper


class TestCommands(unittest.TestCase):
    def setUp(self):
        commands.dnsops.discover_zk_via_dns = Mock(return_value=['host.example.com:1234'])
        commands.print = Mock()
        self.mock_zk = Mock()
        self.mock_zk.get_value = Mock(return_value=b'value')
        commands.zookeeper.Zookeeper = Mock(return_value=self.mock_zk)

    def test_command_discover(self):
        commands.discover()
        commands.dnsops.discover_zk_via_dns.assert_called_once_with()
        commands.print.assert_called_once_with('host.example.com:1234')

    def test_get_zk_hosts_given_host_returns_it(self):
        result = commands.get_zk_hosts('host:123')
        self.assertEqual(result, ['host:123'])
        self.assertFalse(commands.dnsops.discover_zk_via_dns.called)

    def test_get_zk_hosts_without_host_calls_discover(self):
        result = commands.get_zk_hosts(None)
        self.assertEqual(result, ['host.example.com:1234'])
        commands.dnsops.discover_zk_via_dns.assert_called_once_with()

    def test_print_value_success(self):
        commands.print_value('key', 'host:123')
        commands.zookeeper.Zookeeper.assert_called_once_with(['host:123'])
        self.mock_zk.get_value.assert_called_once_with('key')
        commands.print.assert_called_once_with('value')

    def test_print_value_with_exception(self):
        self.mock_zk.get_value.side_effect = zookeeper.NoNodeError
        with self.assertRaises(commands.CommandError):
            commands.print_value('key', 'host:123')
        self.assertTrue(commands.print.called)
