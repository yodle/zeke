import argparse
import sys

from . import commands


def main():
    return dispatch(parse_options(sys.argv[1:]))


def parse_options(args):
    parser = argparse.ArgumentParser(description='Mess around with Zookeeper')
    parser.add_argument('--version', action='store_true', help='echoes the version of zeke you are using')
    parser.add_argument('--discover', action='store_true', help='discover zookeeper via DNS and output its host:port')
    parser.add_argument('-g', '--get', help='get value out of zookeeper and print it', metavar='KEY')
    parser.add_argument('-s', '--set', help='set value in zookeeper', nargs=2, metavar=('KEY', 'VAL'))
    parser.add_argument('-d', '--dump', help='dump child nodes of given key to stdout', metavar='KEY')
    parser.add_argument('-l', '--load', action='store_true', help='load nodes and values in to zookeeper from stdin')
    parser.add_argument('-a', '--address', help='specify the host/port of zookeeper', metavar='ADDR')
    parser.add_argument('--delete', help='delete value from zookeeper', metavar='KEY')
    parser.add_argument('--purge', help='purge a node from zookeeper', metavar='KEY')
    
    if len(args) == 0:
        parser.print_help()

    return vars(parser.parse_args(args))


def dispatch(parser_results):
    try:
        if 'version' in parser_results and parser_results['version']:
            commands.version()
        elif 'discover' in parser_results and parser_results['discover']:
            commands.discover()
        elif parser_results['get']:
            commands.print_value(parser_results['get'], parser_results['address'])
        elif parser_results['set']:
            commands.set_value(parser_results['set'][0], parser_results['set'][1], parser_results['address'])
        elif parser_results['dump']:
            commands.dump(parser_results['dump'], parser_results['address'])
        elif parser_results['delete']:
            commands.delete(parser_results['delete'], parser_results['address'])
        elif parser_results['purge']:
            commands.purge(parser_results['purge'], parser_results['address'])
        elif 'load' in parser_results and parser_results['load']:
            commands.load(parser_results['address'])
    except commands.CommandError:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
