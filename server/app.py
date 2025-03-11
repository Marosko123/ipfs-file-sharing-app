from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os
import mimetypes

app = Flask(__name__)
CORS(app)

IPFS_API_URL = "http://127.0.0.1:5001/api/v0"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Store filename alongside the hash
file_hash_map = {}  # Temporary dictionary to map hashes to filenames

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles file uploads and adds them to IPFS"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    with open(filepath, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{IPFS_API_URL}/add", files=files)

    os.remove(filepath)

    if response.status_code == 200:
        file_hash = response.json()["Hash"]
        file_hash_map[file_hash] = file.filename  # Store filename

        return jsonify({"Hash": file_hash, "Filename": file.filename}), 200
    else:
        return jsonify({"error": "IPFS upload failed"}), 500

@app.route('/retrieve/<file_hash>', methods=['GET'])
def retrieve_file(file_hash):
    """Retrieves a file from IPFS and ensures it downloads with the correct filename and type."""
    response = requests.post(f"{IPFS_API_URL}/cat?arg={file_hash}")

    if response.status_code == 200:
        file_name = file_hash_map.get(file_hash, f"{file_hash}.unknown")  # Default if filename not found
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        # Get correct MIME type for the file
        mime_type, _ = mimetypes.guess_type(file_name)
        mime_type = mime_type or "application/octet-stream"  # Default if unknown

        return send_file(file_path, as_attachment=True, download_name=file_name, mimetype=mime_type)
    else:
        return jsonify({"error": "File retrieval failed"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
