import os
import mimetypes
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import ipfshttpclient

app = Flask(__name__)
CORS(app)

# Connect to local IPFS daemon (defaults to /ip4/127.0.0.1/tcp/5001/http)
client = ipfshttpclient.connect()

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Temporary dictionary to map IPFS file hashes to their original filenames
file_hash_map = {}

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and add them to IPFS using the ipfshttpclient library."""
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
        # result is typically a dict with keys like {'Hash': '...', 'Name': '...', 'Size': '...'}
        file_hash = result['Hash']
        file_hash_map[file_hash] = file.filename
    except Exception as e:
        return jsonify({"error": f"IPFS upload failed: {str(e)}"}), 500
    finally:
        # Clean up the local file once added to IPFS
        if os.path.exists(filepath):
            os.remove(filepath)

    return jsonify({"Hash": file_hash, "Filename": file.filename}), 200

@app.route('/retrieve/<file_hash>', methods=['GET'])
def retrieve_file(file_hash):
    """Retrieve a file from IPFS by its hash, and send it to the client."""
    try:
        # Download file content from IPFS directly into memory
        file_data = client.cat(file_hash)
    except Exception as e:
        return jsonify({"error": f"File retrieval failed: {str(e)}"}), 404

    # Use the stored name or default to <hash>.unknown if not found
    file_name = file_hash_map.get(file_hash, f"{file_hash}.unknown")
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    # Write the file to disk so we can return it with send_file
    with open(file_path, 'wb') as f:
        f.write(file_data)

    # Determine the MIME type for the response
    mime_type, _ = mimetypes.guess_type(file_name)
    mime_type = mime_type or "application/octet-stream"

    return send_file(file_path, as_attachment=True, download_name=file_name, mimetype=mime_type)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
