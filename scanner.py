import nmap
import json
from datetime import datetime

OUI_FILE = "oui.json"

# Load vendors
try:
    with open(OUI_FILE) as f:
        OUI = json.load(f)
except:
    OUI = {}

def lookup_vendor(mac):
    if not mac:
        return "Unknown"
    prefix = mac.upper()[0:8]
    return OUI.get(prefix, "Unknown Vendor")

def scan_network(network_cidr="192.168.1.0/24"):
    nm = nmap.PortScanner()
    nm.scan(hosts=network_cidr, arguments='-sn')  # ping scan

    devices = []
    for host in nm.all_hosts():
        if "mac" in nm[host]['addresses']:
            mac = nm[host]['addresses']['mac']
            devices.append({
                "ip": host,
                "mac": mac,
                "vendor": lookup_vendor(mac),
                "last_seen": datetime.utcnow().isoformat() + "Z"
            })

    return devices

if __name__ == "__main__":
    print(json.dumps(scan_network("192.168.1.0/24"), indent=2))
