# IPFS File Sharing App

This repository provides a simple, practical introduction to decentralized file storage using IPFS (InterPlanetary File System). The project bridges theoretical understanding and practical implementation by demonstrating core IPFS operations in Python, complemented by an optional interactive GUI built with JavaScript.


## Features

**Command-Line Interface:** Basic file operations including uploading, retrieving, and listing files using IPFS.

**Interactive GUI:** Optional graphical interface enhancing user experience and interaction with IPFS.

**Educational Content:** Clearly documented Jupyter notebooks explaining theoretical concepts and implementation details.

**Modular and Tested:** Structured codebase with unit and integration tests ensuring reliability and ease of use.



## Technologies Used

- **IPFS:** Decentralized file storage protocol.
- **Python:** Backend implementation.
- **JavaScript:** Optional GUI frontend.
- **Jupyter Notebook:** Interactive documentation.


## Installation

1. Clone the repository:

```bash
git clone https://github.com/Marosko123/ipfs-file-sharing-app.git
```


2. **Navigate to the server directory:**

```bash
cd ipfs-file-sharing-app/server
```


3. **Install server dependencies:**

```bash
pip install -r requirements.txt
```

4. **Install Correct version of IPFS daemon**

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

