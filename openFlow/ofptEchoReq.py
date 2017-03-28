from ofptHeader import ofptHeader

from os import urandom
from random import randint

def ofptEchoReq(maxLength):
	payload = urandom(randint(0, maxLength - 8))

	header = ofptHeader(2, payload)

	return header + payload