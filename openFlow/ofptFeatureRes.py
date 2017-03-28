from ofptHeader import ofptHeader
from generateFlags import generateFlags

from os import urandom
from struct import Struct

def ofptFeatureRes():
	dataPathID = urandom(8)
	nBuffers = urandom(4)
	nTables = urandom(1)
	auxiliaryID = urandom(1)
	pad = urandom(2)
	capabilities = Struct('! I').pack(generateFlags([1, 2, 4, 8, 32, 64, 256]))
	reserved = urandom(4)
	payload = dataPathID + nBuffers + nTables + auxiliaryID + pad + capabilities + reserved

	header = ofptHeader(6, payload)

	return header + payload