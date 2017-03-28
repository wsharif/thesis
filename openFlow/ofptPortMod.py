from ofptHeader import ofptHeader
from generateFlags import generateFlags

from os import urandom
from struct import Struct
from random import randint

def ofptPortMod():
	port = urandom(4)
	pad = urandom(4)
	hwAddr = urandom(6)
	pad2 = urandom(2)
	config = Struct('! I').pack(generateFlags([1, 4, 32, 64]))
	mask = Struct('! I').pack(generateFlags([1, 4, 32, 64]))
	advertise = Struct('! I').pack(randint(0, 65535))
	pad3 = urandom(4)
	payload = port + pad + hwAddr + pad2 + config + mask + advertise + pad3

	header = ofptHeader(16, payload)

	return header + payload