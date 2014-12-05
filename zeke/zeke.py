import argparse
import sys

from . import commands


def main():
    parser_results = parse_options(sys.argv[1:])

    try:
        if parser_results['discover']:
            commands.discover()
        elif parser_results['get']:
            commands.print_value(parser_results['get'], parser_results['address'])
    except commands.CommandError:
        return 1
    return 0


def parse_options(args):
    parser = argparse.ArgumentParser(description='Mess around with Zookeeper')
    parser.add_argument('--discover', action='store_true', help='discover zookeeper via DNS and output its host:port')
    parser.add_argument('-g', '--get', help='get value out of zookeeper and print it', metavar='KEY')
    parser.add_argument('-a', '--address', help='specify the host/port of zookeeper', metavar='ADDR')
    return vars(parser.parse_args(args))


if __name__ == '__main__':
    sys.exit(main())
