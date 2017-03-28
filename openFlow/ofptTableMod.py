from ofptHeader import ofptHeader

from os import urandom
from random import randint
from struct import Struct

def ofptTableMod():
	tableId = Struct('! B').pack(randint(0, 254))
	pad = urandom(3)
	config = Struct('! I').pack(3)
	payload = tableId + pad + config

	header = ofptHeader(17, payload)

	return header + payload