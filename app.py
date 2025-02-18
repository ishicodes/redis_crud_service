from flask import Flask, request, jsonify
import redis
import json

# Initialize Flask app
app = Flask(__name__)

# Connect to Redis
r = redis.Redis(
    host='redis-13933.c282.east-us-mz.azure.redns.redis-cloud.com',
    port=13933,
    decode_responses=True,
    username="default",
    password="nYff56ymVDJrVbXURVIJtyoXzHpKQeK1",
)

# Function to check for the INCIDENT_ key prefix
def check_incident_key(data):
    for key in data:
        if key.startswith('INCIDENT_'):
            return key, data[key]
    return None, None

@app.route('/incident', methods=['POST'])
def create_incident():
    data = request.get_json()
    key, value = check_incident_key(data)

    if not key:
        return jsonify({"error": "No key with prefix 'INCIDENT_' found"}), 400

    serial_value = json.dumps(value)
    r.set(key, serial_value)
    return jsonify({"message": f"Key '{key}' set with value '{value}'"}), 201

@app.route('/incident/<key>', methods=['GET'])
def read_incident(key):
    value = r.get(key)
    if value is None:
        return jsonify({"error": "Key not found"}), 404
    return jsonify({key: value}), 200

@app.route('/incident/<key>', methods=['PUT'])
def update_incident(key):
    if not r.exists(key):
        return jsonify({"error": "Key not found"}), 404
    
    data = request.get_json()
    _, value = check_incident_key(data)

    if not value:
        return jsonify({"error": "No key with prefix 'INCIDENT_' found"}), 400

    r.set(key, value)
    return jsonify({"message": f"Key '{key}' updated with value '{value}'"}), 200

@app.route('/incident/<key>', methods=['DELETE'])
def delete_incident(key):
    if not r.delete(key):
        return jsonify({"error": "Key not found"}), 404
    return jsonify({"message": f"Key '{key}' deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
