from kazoo import exceptions as KazooExceptions


def discover():
    for result in discover_zk_via_dns():
        print(result)


def print_value(key, address):
    try:
        result = get_value(key, address)
        print(result.decode('utf-8'))
        sys.exit(0)
    except KazooExceptions.NoNodeError as e:
        print('Node not found:', key, file=sys.stderr)
        sys.exit(1)
