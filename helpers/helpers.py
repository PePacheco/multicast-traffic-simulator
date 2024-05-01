import ipaddress

def parse_router_config(config_lines):
    """
    Parse router configuration and find connected routers.

    Args:
        config_lines (list): Lines of configuration from the #ROUTER section.

    Returns:
        dict: Dictionary with router connections.
    """
    routers = {}
    # Parse each router's configuration and store the IP networks
    for line in config_lines:
        parts = line.split(',')
        router_id = parts[0]
        num_interfaces = int(parts[1])
        # Adjust IP addresses to valid network addresses, turning off strict mode
        interfaces = [ipaddress.ip_network(ip.strip(), strict=False) for ip in parts[2:num_interfaces + 2]]
        routers[router_id] = interfaces

    # Determine direct connections based on network overlaps
    connections = {}
    for rid, networks in routers.items():
        for other_rid, other_networks in routers.items():
            if rid != other_rid:  # Avoid self-comparison
                for net in networks:
                    if any(net.overlaps(other_net) for other_net in other_networks):
                        connections.setdefault(rid, []).append(other_rid)

    return connections

# Example usage with network overlaps considered
router_section = [
    "r1,3,10.0.0.1/8,100.10.0.1/16,100.20.0.1/16",
    "r2,2,100.10.0.2/16,20.0.0.1/8",
    "r3,2,100.20.0.2/16,30.0.0.1/8"
]

connections = parse_router_config(router_section)
print(connections)
