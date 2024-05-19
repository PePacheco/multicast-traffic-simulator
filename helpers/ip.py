import ipaddress

def ip_to_network(ip_with_no_mask):
    # Split the IP address and the subnet mask
    ip = ip_with_no_mask

    # Create an IP network object
    network = ipaddress.ip_network(ip_with_no_mask, strict=False)

    # Get the network address
    network_address = network.network_address

    return str(network_address)


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

def ip_in_same_subnet(ip1_with_no_mask: str, subnet_with_mask: str) -> bool:
    # Helper function to convert an IP string to a 32-bit integer
    def ip_to_int(ip: str) -> int:
        octets = ip.split('.')
        return (int(octets[0]) << 24) + (int(octets[1]) << 16) + (int(octets[2]) << 8) + int(octets[3])
    
    # Helper function to create a subnet mask of n bits
    def create_mask(bits: int) -> int:
        return (1 << 32) - (1 << (32 - bits))
    
    # Convert IP and subnet to integers
    ip1_int = ip_to_int(ip1_with_no_mask)
    
    subnet_ip, mask_length = subnet_with_mask.split('/')
    subnet_int = ip_to_int(subnet_ip)
    mask_length = int(mask_length)
    
    # Create the subnet mask
    mask = create_mask(mask_length)
    
    # Compare the network portions
    return (ip1_int & mask) == (subnet_int & mask)