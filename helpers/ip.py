import ipaddress

def ip_to_network(ip_with_mask):
    # Split the IP address and the subnet mask
    ip, subnet_mask = ip_with_mask.split('/')

    # Create an IP network object
    network = ipaddress.ip_network(ip_with_mask, strict=False)

    # Get the network address
    network_address = network.network_address

    return str(network_address)+"/"+subnet_mask


def ip_in_same_subnet(ip_to_check, ip_list):
    # Convert the target IP to an IP address object
    target_ip = ipaddress.ip_address(ip_to_check)

    # Check each IP in the list
    for ip_with_mask in ip_list:
        # Split the IP address and the subnet mask
        ip, subnet_mask = ip_with_mask.split('/')
        # Convert the list IP to an IP address object
        current_ip = ipaddress.ip_address(ip)

        # Create a network object using the IP address and subnet mask
        current_network = ipaddress.ip_network(ip_with_mask, strict=False)

        # Check if the target IP is within the current network
        if target_ip in current_network:
            ipWithMask = str(current_ip)+'/'+subnet_mask
            return ipWithMask

    return None
