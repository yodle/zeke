import unittest
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

from zeke import zookeeper
from kazoo import exceptions as kazooExceptions


class TestZookeeper(unittest.TestCase):
    @patch('zeke.zookeeper.KazooClient')
    def test_connect_calls_kazoo_start(self, mock_kazoo_client):
        mock_zk = Mock()
        mock_kazoo_client.return_value = mock_zk
        zookeeper.Zookeeper.connect(['host:1234'])
        mock_zk.start.assert_called_once_with()

    @patch('zeke.zookeeper.KazooClient')
    def test_connect_handles_multiple_hosts(self, mock_kazoo_client):
        zookeeper.Zookeeper.connect(['host1:1234', 'host2:3456'])
        mock_kazoo_client.assert_called_once_with(hosts='host1:1234,host2:3456')

    @patch('zeke.zookeeper.KazooClient')
    def test_get_value_success(self, mock_kazoo_client):
        mock_zk = Mock()
        mock_kazoo_client.return_value = mock_zk
        mock_zk.get.return_value = (b'value', 'stat')

        zk = zookeeper.Zookeeper(['host:1234'])
        result = zk.get_value('key')
        self.assertEqual(result, b'value')

    @patch('zeke.zookeeper.KazooClient')
    def test_get_value_no_node(self, mock_kazoo_client):
        mock_zk = Mock()
        mock_kazoo_client.return_value = mock_zk
        mock_zk.get.side_effect = kazooExceptions.NoNodeError

        zk = zookeeper.Zookeeper(['host:1234'])
        with self.assertRaises(zookeeper.NoNodeError):
            zk.get_value('key')