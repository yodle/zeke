from __future__ import print_function

import argparse
import sys

from kazoo.client import KazooClient

from . import commands, dns


def connect(hosts):
    if not hosts:
        hosts = ",".join(dns.discover_zk_via_dns())
    zk = KazooClient(hosts=hosts)
    zk.start()
    return zk


def get_value(key, address):
    zk = connect(address)
    data, stat = zk.get(key)
    return data


def main():
    parser = argparse.ArgumentParser(description='Mess around with Zookeeper')
    parser.add_argument('--discover', action='store_true', help='discover zookeeper via DNS and output its host:port')
    parser.add_argument('-g', '--get', help="get value out of zookeeper and print it")
    parser.add_argument('-a', '--address', help="specify the host/port of zookeeper")
    parser_results = vars(parser.parse_args())

    if parser_results['discover']:
        commands.discover()
    elif parser_results['get']:
        commands.print_value(parser_results['get'], parser_results['address'])

if __name__ == '__main__':
    sys.exit(main())
