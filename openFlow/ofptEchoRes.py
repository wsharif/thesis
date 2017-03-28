from ofptHeader import ofptHeader

from os import urandom
from random import randint

def ofptEchoRes(maxLength):
	payload = urandom(randint(0, maxLength - 8))

	header = ofptHeader(3, payload)

	return header + payload