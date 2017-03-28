from ofptHeader import ofptHeader
from generateFlags import generateFlags

from os import urandom
from random import choice, randint
from struct import Struct

def ofptPortStatus():
	reason = Struct('! B').pack(randint(0, 2))
	padding = urandom(7)

	portID = Struct('! I').pack(choice([4294967040, 4294967288, 4294967289, 4294967290, 4294967291, 4294967292, 4294967293, 4294967294, 4294967295]))
	pad = urandom(4)
	hwAddr = urandom(6)
	pad2 = urandom(2)
	name = urandom(16)
	config = Struct('! I').pack(generateFlags([1, 4, 32, 64]))
	state = Struct('! I').pack(randint(0, 15))
	current = Struct('! I').pack(randint(0, 65535))
	advertised = Struct('! I').pack(randint(0, 65535))
	supported = Struct('! I').pack(randint(0, 65535))
	peer = Struct('! I').pack(randint(0, 65535))
	currSpeed = urandom(4)
	maxSpeed = urandom(4)
	port = portID + pad + hwAddr + pad2 + name + config + state + current + advertised + supported + peer + currSpeed + maxSpeed

	payload = reason + padding + port

	header = ofptHeader(12, payload)

	return header + payload