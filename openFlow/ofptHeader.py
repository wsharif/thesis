from os import urandom
from struct import Struct

def ofptHeader(type, payload = ""):
	version = Struct('! B').pack(4)
	type = Struct('! B').pack(type)
	length = Struct('! H').pack(8 + len(payload))
	xid = urandom(4)

	header = version + type + length + xid

	return header