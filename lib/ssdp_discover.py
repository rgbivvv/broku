import socket

def discover_roku_devices(timeout=5):
    """
    Send an SSDP M-SEARCH request for Roku ECP devices and return a list of IP addresses.
    
    Args:
        timeout (int): Number of seconds to wait for responses.
    
    Returns:
        List[str]: List of responding device IPs.
    """
    SSDP_ADDR = "239.255.255.250"
    SSDP_PORT = 1900
    SSDP_MX = 2
    SSDP_ST = "roku:ecp"

    # Build M-SEARCH request
    request = "\r\n".join([
        "M-SEARCH * HTTP/1.1",
        f"HOST: {SSDP_ADDR}:{SSDP_PORT}",
        'MAN: "ssdp:discover"',
        f"MX: {SSDP_MX}",
        f"ST: {SSDP_ST}",
        "",
        ""
    ]).encode("utf-8")

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(timeout)

    # Send the request to the multicast address
    sock.sendto(request, (SSDP_ADDR, SSDP_PORT))

    ips = set()  # use a set to avoid duplicates

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            ips.add(addr[0])
    except socket.timeout:
        pass  # done collecting responses

    return list(ips)