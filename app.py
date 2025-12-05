from flask import Flask, render_template, jsonify, request
from scanner import scan_network
import db


app = Flask(__name__)


# initialize DB
db.init_db()


@app.route('/')
def index():
devices = db.get_all_devices()
return render_template('index.html', devices=devices)


@app.route('/api/scan', methods=['POST'])
def api_scan():
data = request.get_json() or {}
network = data.get('network', '192.168.1.0/24')
devices = scan_network(network_cidr=network)
# upsert into DB
for d in devices:
db.upsert_device(d)
return jsonify({'devices': devices})


@app.route('/api/devices')
def api_devices():
return jsonify({'devices': db.get_all_devices()})


if __name__ == '__main__':
app.run(debug=True, host='0.0.0.0')
