import sqlite3
from datetime import datetime

DB = "devices.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            ip TEXT PRIMARY KEY,
            mac TEXT,
            vendor TEXT,
            last_seen TEXT
        )
    """)
    conn.commit()
    conn.close()


def upsert_device(device):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        INSERT INTO devices (ip, mac, vendor, last_seen)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(ip) DO UPDATE SET
            mac=excluded.mac,
            vendor=excluded.vendor,
            last_seen=excluded.last_seen
    """, (
        device["ip"],
        device["mac"],
        device["vendor"],
        device["last_seen"]
    ))

    conn.commit()
    conn.close()


def get_all_devices():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT ip, mac, vendor, last_seen FROM devices")
    rows = c.fetchall()

    conn.close()

    devices = []
    for r in rows:
        devices.append({
            "ip": r[0],
            "mac": r[1],
            "vendor": r[2],
            "last_seen": r[3]
        })

    return devices
