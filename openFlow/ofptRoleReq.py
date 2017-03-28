from ofptHeader import ofptHeader

from os import urandom
from random import randint
from struct import Struct

def ofptRoleReq():
	role = Struct('! I').pack(randint(0, 3))
	pad = urandom(4)
	generationId = urandom(8)
	payload = role + pad + generationId

	header = ofptHeader(24, payload)

	return header + payload