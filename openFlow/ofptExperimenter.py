from ofptHeader import ofptHeader

from os import urandom
from random import randint

def ofptExperimenter(maxLength):
	experimenterId = urandom(4)
	experimenterType = urandom(4)
	data = urandom(randint(0, maxLength - 8 - 8))

	payload = experimenterId + experimenterType + data

	header = ofptHeader(4, payload)

	return header + payload