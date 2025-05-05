# ipfs-web-interface

A full-stack Vue 3 + Vite application with an accompanying Node.js/Express server, enabling in-browser IPFS uploads, downloads, peer management, performance monitoring, and optional pinning via Web3.Storage.

Author: Maros Bednar
Date: 2025-05-05

---

## 🎯 Features

- **In-Browser IPFS Node**  
  Spin up a Helia (libp2p) node in your browser—no external daemon required.  
- **Upload & Download**  
  Add arbitrary files to IPFS and fetch them by CID, with automatic timing and clipboard integration.  
- **Peer Management**  
  View your peer ID and a live list of connected peers.  
- **Performance Monitoring**  
  Track upload/download durations and file sizes, persist them in `localStorage`, export CSV.  
- **History**  
  Browse past operations (uploads/downloads) with timestamps.  
- **Optional Pinning**  
  Pin CIDs to Web3.Storage via a simple Node.js/Express backend.  
- **Responsive UI**  
  Built with Vue 3, Vite, TypeScript, and Pinia.  

---

## 🛠 Tech Stack

- **Frontend:** Vue 3, Vite, TypeScript, Pinia, Vue Router  
- **IPFS:** Helia (libp2p + UnixFS)  
- **Backend:** Node.js, Express, Web3.Storage client  
- **Tooling:** ESLint, Prettier, vue-tsc  

---

## 🔧 Prerequisites

- **Node.js** 16+ & npm  
- **Modern Browser** (with Web Crypto API support)  

---

## Installation

1. Clone the repository:

```bash
# Clone repo
git clone https://github.com/yourusername/ipfs-web-interface.git
cd ipfs-web-interface

# Install both frontend
npm install
```

2. **Install server dependencies:**

```bash
cd ipfs-file-sharing-app/server
pip install -r requirements.txt

```

3. **Install Correct version of IPFS daemon**

```bash
curl -O https://dist.ipfs.tech/go-ipfs/v0.7.0/go-ipfs_v0.7.0_darwin-amd64.tar.gz
```

After installation is complete, extract the tarball and copy the IPFS binary to your system path:
```bash
tar xvf go-ipfs_v0.7.0_darwin-amd64.tar.gz
cd go-ipfs
sudo cp ipfs /usr/local/bin/
```

## Usage

1. **Start your IPFS daemon:**
Open new terminal window and run the following commands:

```bash
ipfs init
ipfs daemon
```

2. **Run app.py:**
Open new terminal window and run the following commands:

```bash
cd server
source venv/bin/activate
python3 app.py
```

3. **UPDATE GUI URL:**
Open .env.production file and update the VITE_API_BASE_URL variable to point to your server's IP address and port.
Server IP was generated using command above. (example: http://168.1.1:5001)

4. **Run GUI:**

```bash
cd gui
npm install
npm run build
```

Then, copy generated dist folder to the server directory next to app.py.

5. **Access the GUI:**
Open your web browser and navigate server url (example `http://168.1.1:5001` or the port you specified in the GUI configuration).

## Contributing

Contributions are encouraged! Please open issues or submit pull requests to propose enhancements or new features.

## License

Distributed under the MIT License. See LICENSE file for more information.

