import sqlite3


DB = "network.db"


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS devices(
mac TEXT PRIMARY KEY,
ip TEXT,
vendor TEXT,
first_seen TEXT,
last_seen TEXT
)
"""




def init_db():
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute(CREATE_SQL)
conn.commit()
conn.close()




def upsert_device(device):
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute('''
INSERT INTO devices(mac, ip, vendor, first_seen, last_seen)
VALUES(?,?,?,?,?)
ON CONFLICT(mac) DO UPDATE SET
ip=excluded.ip,
vendor=excluded.vendor,
last_seen=excluded.last_seen
''', (device['mac'], device['ip'], device.get('vendor',''), device.get('last_seen'), device.get('last_seen')))
conn.commit()
conn.close()




def get_all_devices():
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute('SELECT mac, ip, vendor, first_seen, last_seen FROM devices')
rows = cur.fetchall()
conn.close()
return [dict(mac=r[0], ip=r[1], vendor=r[2], first_seen=r[3], last_seen=r[4]) for r in rows]
