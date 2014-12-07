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
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        zookeeper.Zookeeper.connect(['host:1234'])
        mock_zk.start.assert_called_once_with()

    @patch('zeke.zookeeper.KazooClient')
    def test_connect_handles_multiple_hosts(self, mock_kazoo_client):
        zookeeper.Zookeeper.connect(['host1:1234', 'host2:3456'])
        mock_kazoo_client.assert_called_once_with(hosts='host1:1234,host2:3456')

    @patch('zeke.zookeeper.KazooClient')
    def test_get_value_success(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        mock_zk.get.return_value = (b'value', 'stat')

        zk = zookeeper.Zookeeper(['host:1234'])
        result = zk.get_value('key')
        self.assertEqual(result, b'value')

    @patch('zeke.zookeeper.KazooClient')
    def test_get_value_no_node(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        mock_zk.get.side_effect = kazooExceptions.NoNodeError

        zk = zookeeper.Zookeeper(['host:1234'])
        with self.assertRaises(zookeeper.NoNodeError):
            zk.get_value('key')

    @patch('zeke.zookeeper.KazooClient')
    def test_exists_when_true(self, mock_kazoo_client):
        result = self.get_desired_return_value_from_exists({'fakeZKNodeStat': True}, mock_kazoo_client)
        self.assertTrue(result)

    @patch('zeke.zookeeper.KazooClient')
    def test_exists_when_true(self, mock_kazoo_client):
        result = self.get_desired_return_value_from_exists(None, mock_kazoo_client)
        self.assertFalse(result)

    def get_desired_return_value_from_exists(self, return_value, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        mock_zk.exists.return_value = return_value
        zk = zookeeper.Zookeeper(['host:1234'])
        return zk.key_exists('key')

    @patch('zeke.zookeeper.KazooClient')
    def test_create_calls_proper_create(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        zk = zookeeper.Zookeeper(['host:1234'])
        zk.create_node('key', 'value')
        mock_zk.create.assert_called_once_with('key', b'value', makepath=True)

    @patch('zeke.zookeeper.KazooClient')
    def test_create_throws_node_exists_error(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        mock_zk.create.side_effect = kazooExceptions.NodeExistsError

        zk = zookeeper.Zookeeper(['host:1234'])
        with self.assertRaises(zookeeper.NodeExistsError):
            zk.create_node('key', 'value')

    @patch('zeke.zookeeper.KazooClient')
    def test_set_calls_proper_kazoo_method(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        zk = zookeeper.Zookeeper(['host:1234'])
        zk.set_value('key', 'value')
        mock_zk.set.assert_called_once_with('key', b'value')

    @patch('zeke.zookeeper.KazooClient')
    def test_set_throws_no_node_error(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        mock_zk.set.side_effect = kazooExceptions.NoNodeError

        zk = zookeeper.Zookeeper(['host:1234'])
        with self.assertRaises(zookeeper.NoNodeError):
            zk.set_value('key', 'value')

    @patch('zeke.zookeeper.KazooClient')
    @patch('zeke.zookeeper.Zookeeper.key_exists')
    @patch('zeke.zookeeper.Zookeeper.set_value')
    def test_set_or_create_sets_properly(self, mock_set_value, mock_key_exists, _):
        mock_key_exists.return_value = True
        zk = zookeeper.Zookeeper(['host:1234'])
        zk.set_or_create('key', 'value')
        mock_set_value.assert_called_once_with('key', 'value')

    @patch('zeke.zookeeper.KazooClient')
    @patch('zeke.zookeeper.Zookeeper.key_exists')
    @patch('zeke.zookeeper.Zookeeper.create_node')
    def test_set_or_create_sets_properly(self, mock_create_node, mock_key_exists, _):
        mock_key_exists.return_value = False
        zk = zookeeper.Zookeeper(['host:1234'])
        zk.set_or_create('key', 'value')
        mock_create_node.assert_called_once_with('key', 'value')

    @staticmethod
    def setup_mock_zk(mock_kazoo_client):
        mock_zk = Mock()
        mock_kazoo_client.return_value = mock_zk
        return mock_zk