import os
import sqlite3
import mimetypes
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import ipfshttpclient
from requests.exceptions import ConnectionError

app = Flask(__name__)
CORS(app)

# List of IPFS nodes (update with your node IPs)
IPFS_NODES = [
    '/ip4/127.0.0.1/tcp/5001',  # Local node
    '/ip4/192.168.1.101/tcp/5001',  # Second node IP
    '/ip4/192.168.1.102/tcp/5001',  # Third node IP
]

def get_ipfs_client():
    """Attempt to connect to IPFS nodes in order, return first successful client."""
    for node in IPFS_NODES:
        try:
            client = ipfshttpclient.connect(node)
            print(f"Connected to IPFS node: {node}")
            return client
        except ConnectionError:
            print(f"Failed to connect to IPFS node: {node}")
    raise Exception("No available IPFS nodes")

# Initialize IPFS client
client = get_ipfs_client()

# Initialize SQLite database
DB_FILE = 'file_map.db'
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS files (hash TEXT PRIMARY KEY, filename TEXT)')
conn.commit()

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve the Vue app's static files from the dist folder."""
    dist_dir = os.path.join(app.root_path, 'dist')
    if path != "" and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)
    return send_from_directory(dist_dir, 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and add them to IPFS."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save file locally
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Add file to IPFS
    try:
        result = client.add(filepath)
        file_hash = result['Hash']
        # Store in SQLite
        conn.execute('INSERT OR REPLACE INTO files (hash, filename) VALUES (?, ?)', (file_hash, file.filename))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"IPFS upload failed: {str(e)}"}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    return jsonify({"Hash": file_hash, "Filename": file.filename}), 200

@app.route('/retrieve/<file_hash>', methods=['GET'])
def retrieve_file(file_hash):
    """Retrieve a file from IPFS by its hash."""
    try:
        file_data = client.cat(file_hash)
    except Exception as e:
        return jsonify({"error": f"File retrieval failed: {str(e)}"}), 404

    # Get filename from SQLite
    cursor = conn.execute('SELECT filename FROM files WHERE hash = ?', (file_hash,))
    result = cursor.fetchone()
    file_name = result[0] if result else f"{file_hash}.unknown"

    # Save file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    with open(file_path, 'wb') as f:
        f.write(file_data)

    # Determine MIME type
    mime_type, _ = mimetypes.guess_type(file_name)
    mime_type = mime_type or "application/octet-stream"

    # Serve file and clean up
    response = send_file(file_path, as_attachment=True, download_name=file_name, mimetype=mime_type)
    if os.path.exists(file_path):
        os.remove(file_path)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5001)
