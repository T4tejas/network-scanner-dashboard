"""
scanner.py


Performs a simple ARP scan for a /24 network and returns devices with IP, MAC & vendor.
This uses scapy; run with elevated privileges.
"""


from scapy.all import ARP, Ether, srp
import json
from datetime import datetime


# Load OUI database file (simple JSON mapping)
OUI_FILE = "oui.json"


try:
with open(OUI_FILE) as f:
OUI = json.load(f)
except Exception:
OUI = {}




def lookup_vendor(mac):
if not mac:
return "Unknown"
prefix = mac.upper()[0:8]
return OUI.get(prefix, "Unknown Vendor")




def scan_network(network_cidr="192.168.1.0/24", timeout=2):
"""Return list of devices found on local network"""
arp = ARP(pdst=network_cidr)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether/arp


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




# quick test when run directly
if __name__ == "__main__":
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--network", default="192.168.1.0/24")
args = parser.parse_args()
print("Scanning:", args.network)
d = scan_network(args.network)
print(json.dumps(d, indent=2))
