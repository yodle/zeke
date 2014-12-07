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

    def key_exists(self, key):
        stat = self.zk.exists(key)
        return stat is not None

    def create_node(self, key, value):
        try:
            self.zk.create(key, self.value_str_to_bytestring(value), makepath=True)
        except kazooExceptions.NodeExistsError as e:
            raise NodeExistsError(e)

    def set_value(self, key, value):
        try:
            self.zk.set(key, self.value_str_to_bytestring(value))
        except kazooExceptions.NoNodeError as e:
            raise NoNodeError(e)

    def set_or_create(self, key, value):
        if self.key_exists(key):
            self.set_value(key, value)
        else:
            self.create_node(key, value)

    @staticmethod
    def value_str_to_bytestring(value):
        return value.encode('utf-8')


class NodeExistsError(kazooExceptions.NodeExistsError):
    pass


class NoNodeError(kazooExceptions.NoNodeError):
    pass
