from ofptHeader import ofptHeader

from struct import Struct
from random import randint
from os import urandom

def ofptQueueGetConfigReq():
	port = Struct('! I').pack(randint(0, 4294967039))
	pad = urandom(4)
	payload = port + pad

	header = ofptHeader(22, payload)

	return header + payload