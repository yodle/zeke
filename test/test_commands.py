import unittest
from unittest.mock import Mock

from zeke import commands


class TestCommands(unittest.TestCase):
    def setUp(self):
        commands.dnsops.discover_zk_via_dns = Mock(return_value=['host.example.com:1234'])
        commands.print = Mock()

    def tearDown(self):
        commands.dnsops.discover_zk_via_dns.reset_mock()
        commands.print.reset_mock()

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