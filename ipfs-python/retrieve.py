import ipfshttpclient
import sys

client = ipfshttpclient.connect()

file_hash = sys.argv[1]
client.get(file_hash)
print(f"File retrieved: {file_hash}")
