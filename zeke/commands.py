from __future__ import print_function

import sys

from . import zookeeper, dnsops


def discover():
    for result in dnsops.discover_zk_via_dns():
        print(result)


def print_value(key, host):
    try:
        zk = zookeeper.Zookeeper(get_zk_hosts(host))
        result = zk.get_value(key)
        print(result.decode('utf-8'))
    except zookeeper.NoNodeError as e:
        print('Node not found:', key, file=sys.stderr)
        raise CommandError(e)


def set_value(key, value, host):
    zk = zookeeper.Zookeeper(get_zk_hosts(host))
    zk.set_or_create(key, value)


def get_zk_hosts(host):
    if host:
        return [host]
    else:
        return dnsops.discover_zk_via_dns()


class CommandError(Exception):
    pass