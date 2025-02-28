from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# In-memory storage for IoT device data
device_data = {}
device_registry = {}

@app.route('/register_device', methods=['POST'])
def register_device():
    """Register a new IoT device."""
    data = request.json
    device_id = data.get('device_id')
    device_name = data.get('device_name')

    if device_id in device_registry:
        return jsonify({'status': 'Device already registered'}), 400

    device_registry[device_id] = device_name
    logging.info(f"Device registered: {device_id} - {device_name}")
    return jsonify({'status': 'Device registered successfully'}), 201

@app.route('/send_data', methods=['POST'])
def send_data():
    """Receive data from an IoT device."""
    data = request.json
    device_id = data.get('device_id')
    sensor_data = data.get('sensor_data')

    if device_id not in device_registry:
        return jsonify({'status': 'Device not registered'}), 400

    if device_id not in device_data:
        device_data[device_id] = []

    device_data[device_id].append(sensor_data)
    logging.info(f"Data received from {device_id}: {sensor_data}")
    return jsonify({'status': 'Data received successfully'}), 200

@app.route('/get_device_data/<device_id>', methods=['GET'])
def get_device_data(device_id):
    """Retrieve data for a specific device."""
    if device_id not in device_registry:
        return jsonify({'status': 'Device not registered'}), 400

    data = device_data.get(device_id, [])
    return jsonify({'device_id': device_id, 'data': data}), 200

@app.route('/get_all_devices', methods=['GET'])
def get_all_devices():
    """Retrieve a list of all registered devices."""
    return jsonify(device_registry), 200

if __name__ == '__main__':
    app.run(debug=True)
