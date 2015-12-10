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
        zk.create_node('key', b'value')
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
        zk.set_value('key', b'value')
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

    @patch('zeke.zookeeper.KazooClient')    
    def test_detete_calls_kazoo_properly(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        zk = zookeeper.Zookeeper(['host:1234'])
        zk.delete('key', False)
        mock_zk.delete.called_once_with('key', False)

    @patch('zeke.zookeeper.KazooClient')
    def test_delete_raises_no_node_error(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        mock_zk.delete.side_effect = kazooExceptions.NoNodeError
        zk = zookeeper.Zookeeper(['host:1234'])
        with self.assertRaises(zookeeper.NoNodeError):
            zk.delete('key', False)

    @patch('zeke.zookeeper.KazooClient')
    def test_delete_raises_not_empty_error(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        mock_zk.delete.side_effect = kazooExceptions.NotEmptyError
        zk = zookeeper.Zookeeper(['host:1234'])
        with self.assertRaises(zookeeper.NotEmptyError):
            zk.delete('key', False)
        
    @patch('zeke.zookeeper.KazooClient')
    def test_get_children_calls_kazoo_properly(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        mock_zk.get_children.return_value = ['/key/one', '/key/two']
        zk = zookeeper.Zookeeper(['host:1234'])
        result = zk.get_children('/key')
        self.assertEqual(['/key/one', '/key/two'], result)
        mock_zk.get_children.called_once_with('/key')

    @patch('zeke.zookeeper.KazooClient')
    def test_get_children_raises_no_node_error(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        mock_zk.get_children.side_effect = kazooExceptions.NoNodeError
        zk = zookeeper.Zookeeper(['host:1234'])
        with self.assertRaises(zookeeper.NoNodeError):
            zk.get_children('/key')

    @patch('zeke.zookeeper.KazooClient')
    @patch('zeke.zookeeper.Zookeeper.get_children')
    def test_get_descendants_of_node_includes_slash_for_root(self, mock_get_children, _):
        zk = zookeeper.Zookeeper(['host:1234'])
        mock_get_children.return_value = []
        result = zk.get_descendants_of_node('/')
        self.assertEqual(frozenset(['/']), result)

    @patch('zeke.zookeeper.KazooClient')
    @patch('zeke.zookeeper.Zookeeper.get_children')
    def test_get_descendants_gets_children_properly(self, mock_get_children, _):
        zk = zookeeper.Zookeeper(['host:1234'])

        # this bit of magic makes the mock return ['abc','def'] only when called with a '', otherwise it returns []
        mock_results = {'': ['abc', 'def']}
        mock_get_children.side_effect = lambda x: mock_results.get(x, [])

        result = zk.get_descendants_of_node('/')
        self.assertEqual(frozenset(['/', '/abc', '/def']), result)

    @patch('zeke.zookeeper.KazooClient')
    @patch('zeke.zookeeper.Zookeeper.get_children')
    def test_get_descendants_gets_grandkids(self, mock_get_children, _):
        zk = zookeeper.Zookeeper(['host:1234'])

        # have the return value of the mock depend on the parameter it is called with
        mock_results = {'': ['abc', 'def'], '/abc': ['123']}
        mock_get_children.side_effect = lambda x: mock_results.get(x, [])

        result = zk.get_descendants_of_node('/')
        self.assertEqual(frozenset(['/', '/abc', '/abc/123', '/def']), result)

    @patch('zeke.zookeeper.KazooClient')
    @patch('zeke.zookeeper.Zookeeper.get_value')
    def test_get_values(self, mock_get_value, _):
        zk = zookeeper.Zookeeper(['host:1234'])

        # have the return value of the mock depend on the paramter it is called with
        mock_results = {'/a': '1', '/b': '2'}
        mock_get_value.side_effect = mock_results.get

        result = zk.get_values(['/a', '/b'])
        self.assertEqual([('/a', '1'), ('/b', '2')], list(result))

    @patch('zeke.zookeeper.KazooClient')
    def test_get_values_throws_no_node_error(self, mock_kazoo_client):
        mock_zk = self.setup_mock_zk(mock_kazoo_client)
        mock_zk.get.side_effect = kazooExceptions.NoNodeError

        zk = zookeeper.Zookeeper(['host:1234'])
        with self.assertRaises(zookeeper.NoNodeError):
            zk.get_values(['/a'])

    @staticmethod
    def setup_mock_zk(mock_kazoo_client):
        mock_zk = Mock()
        mock_kazoo_client.return_value = mock_zk
        return mock_zk
