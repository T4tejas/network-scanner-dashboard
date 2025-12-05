"""
scanner.py

Performs an ARP scan on the local network and returns devices
with IP, MAC, and vendor lookup.
"""

from scapy.all import ARP, Ether, srp
import json
from datetime import datetime

OUI_FILE = "oui.json"

# Load OUI database safely
try:
    with open(OUI_FILE) as f:
        OUI = json.load(f)
except Exception:
    OUI = {}

def lookup_vendor(mac):
    if not mac:
        return "Unknown"
    prefix = mac.upper()[0:8]   # first 8 chars (XX:XX:XX)
    return OUI.get(prefix, "Unknown Vendor")

def scan_network(network_cidr="192.168.1.0/24", timeout=2):
    """Perform ARP scan and return list of devices."""
    arp = ARP(pdst=network_cidr)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    answered = srp(packet, timeout=timeout, verbose=0)[0]

    devices = []
    for sent, received in answered:
        mac = received.hwsrc
        devices.append({
            "ip": received.psrc,
            "mac": mac,
            "vendor": lookup_vendor(mac),
            "last_seen": datetime.utcnow().isoformat() + "Z"
        })

    return devices

# Debug test
if __name__ == "__main__":
    print("Scanning network…")
    result = scan_network("192.168.1.0/24")
    print(json.dumps(result, indent=2))
