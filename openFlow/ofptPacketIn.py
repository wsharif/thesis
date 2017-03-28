from ofptHeader import ofptHeader
from generateMatch import generateMatch

from os import urandom
from random import randint
from struct import Struct

def ofptPacketIn(maxLength):
	payloadLength = randint(18 + 4 + 14, maxLength - 8)

	bufferId = urandom(4)
	totalLen = urandom(2)
	reason = Struct('! B').pack(randint(0, 2))
	tableId = urandom(1)
	cookie = urandom(8)
	pad = urandom(2)

	if randint(0, 1):
		match = generateMatch(payloadLength - 18 - 14)
		data = urandom(randint(14, payloadLength - len(match)))
	else:
		data = urandom(randint(14, payloadLength - 4))
		match = generateMatch(payloadLength - len(data))

	payload = bufferId + totalLen + reason + tableId + cookie + match + pad + data

	header = ofptHeader(10, payload)

	return header + payload