import ipfshttpclient
import sys

client = ipfshttpclient.connect()

filename = sys.argv[1]
res = client.add(filename)
print(f"File added with hash: {res['Hash']}")
