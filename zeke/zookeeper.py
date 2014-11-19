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


class NoNodeError(kazooExceptions.NoNodeError):
    pass
