from kazoo.client import KazooClient
from kazoo import exceptions as kazooExceptions


class Zookeeper(object):
    def __init__(self, hosts):
        self.zk = self.connect(hosts)

    @staticmethod
    def connect(hosts):
        hosts = ",".join(hosts)
        zk = KazooClient(hosts=hosts)
        zk.start()
        return zk

    def get_value(self, key):
        try:
            data, stat = self.zk.get(key)
        except kazooExceptions.NoNodeError as e:
            raise NoNodeError(e)
        return data

    def get_values(self, keys):
        return list(map(lambda k: (k, self.get_value(k)), keys))

    def key_exists(self, key):
        stat = self.zk.exists(key)
        return stat is not None

    def create_node(self, key, value):
        try:
            self.zk.create(key, value, makepath=True)
        except kazooExceptions.NodeExistsError as e:
            raise NodeExistsError(e)

    def set_value(self, key, value):
        try:
            self.zk.set(key, value)
        except kazooExceptions.NoNodeError as e:
            raise NoNodeError(e)

    def set_or_create(self, key, value):
        if self.key_exists(key):
            self.set_value(key, value)
        else:
            self.create_node(key, value)

    def delete(self, key, recursive=False):
        try:
            # deletes all version of the key
            self.zk.delete(key, -1, recursive)
        except kazooExceptions.NoNodeError as e:
            raise NoNodeError(e)
        except kazooExceptions.NotEmptyError as e:
            raise NotEmptyError(e)
            
    def get_children(self, key):
        try:
            return self.zk.get_children(key)
        except kazooExceptions.NoNodeError as e:
            raise NoNodeError(e)
        
    def get_descendants_of_node(self, key):
        # remove trailing slash, and treat an empty path as the root path
        key = key.rstrip('/')
        if key == '':
            results = frozenset(['/'])
        else:
            results = frozenset([key])

        # get the full paths of this node's immediate children
        children = self.get_children(key)
        children_full_paths = frozenset(map(lambda c: key + '/' + c, children))

        # recursively call this function for each child, collect all results in a set
        for child in children_full_paths:
            results = results | self.get_descendants_of_node(child)

        return results


class NodeExistsError(kazooExceptions.NodeExistsError):
    pass


class NoNodeError(kazooExceptions.NoNodeError):
    pass


class NotEmptyError(kazooExceptions.NotEmptyError):
    pass
