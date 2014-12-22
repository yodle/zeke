from __future__ import print_function

import sys
import json

from . import zookeeper, dnsops


def discover():
    for result in dnsops.discover_zk_via_dns():
        print(result)


def print_value(key, host):
    try:
        zk = get_zk(host)
        result = zk.get_value(key)
        print(result.decode('utf-8'))
    except zookeeper.NoNodeError as e:
        print('Node not found:', key, file=sys.stderr)
        raise CommandError(e)


def set_value(key, value, host):
    zk = get_zk(host)
    zk.set_or_create(key, value)


def dump(key, host):
    try:
        zk = get_zk(host)
        pairs = _get_sorted_list_of_descendants_with_values(zk, key)
        print(_format_pairs_for_output(pairs))
    except zookeeper.NoNodeError as e:
        print('Node not found', file=sys.stderr)
        raise(CommandError(e))


def _get_sorted_list_of_descendants_with_values(zk, key):
    descendants = list(zk.get_descendants_of_node(key))
    descendants.sort()
    return zk.get_values(descendants)


def _format_pairs_for_output(pairs):
    pairs_of_strings = map(_get_pairs_of_strings_if_possible, pairs)
    list_of_json_lists = map(_convert_pair_to_json, pairs_of_strings)
    return '\n'.join(list_of_json_lists)


def _get_pairs_of_strings_if_possible(pair):
    return pair[0], _clean_value(pair[1])


def _clean_value(value):
    if not value:
        return ''

    try:
        return value.decode('utf-8')
    except UnicodeDecodeError:
        return value


def _convert_pair_to_json(pair):
    try:
        return json.dumps(pair)
    except (TypeError, UnicodeDecodeError) as e:
        print("Unable to encode value for key: %s\n" % pair[0], file=sys.stderr)
        raise e


def load(host):
    pairs = _parse_all_lines(sys.stdin)
    _load_pairs(get_zk(host), pairs)


def _load_pairs(zk, pairs):
    for pair in pairs:
        zk.set_or_create(pair[0], pair[1])


def _parse_all_lines(line_source):
    pairs = []
    for line in line_source:
        pairs.append(_parse_line(line))
    return pairs


def _parse_line(line):
    try:
        pair = json.loads(line)
    except ValueError as e:
        raise CommandError(e)
    if type(pair) != list:
        raise CommandError('expected line to be of type list but found something else: %s' % type(pair))
    if len(pair) != 2:
        raise CommandError('expected 2 elements in line (key/value), but got %d' % len(pair))
    return tuple(map(lambda item: str(item), pair))


def get_zk(host):
    return zookeeper.Zookeeper(get_zk_hosts(host))


def get_zk_hosts(host):
    if host:
        return [host]
    else:
        return dnsops.discover_zk_via_dns()


class CommandError(Exception):
    pass