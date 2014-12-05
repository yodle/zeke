import dns.resolver


def discover_zk_via_dns():
    try:
        results = dns.resolver.query('_zookeeper._tcp', 'SRV')
    except dns.resolver.NXDOMAIN:
        return []
    return list(map(_clean_host, results))


def _clean_host(resolved_name):
    return str(resolved_name.target).rstrip('.') + ':' + str(resolved_name.port)