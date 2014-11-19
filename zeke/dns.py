import dns.resolver


def discover_zk_via_dns():
    try:
        results = dns.resolver.query('_zookeeper._tcp', 'SRV')
    except dns.resolver.NXDOMAIN:
        return []
    return list(map(lambda r: str(r.target).rstrip('.') + ':' + str(r.port), results))