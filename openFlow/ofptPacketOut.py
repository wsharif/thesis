from ofptHeader import ofptHeader
from generateActions import generateActions

from os import urandom
from random import randint
from struct import Struct

def ofptPacketOut(maxLength):
	payloadLength = randint(16 + 16 + 14, maxLength - 8)

	bufferID = urandom(4)
	inPort = Struct('! I').pack(randint(0, 4294967040))
	pad = urandom(6)

	if randint(0, 1):
		actions = generateActions(payloadLength - 16 - 14, minimum = 1)
		data = urandom(randint(14, payloadLength - 16 - len(actions)))
	else:
		data = urandom(randint(14, payloadLength - 16 - 16))
		actions = generateActions(payloadLength - 16 - len(data), minimum = 1)

	actionsLength = Struct('! H').pack(len(actions))
	payload = bufferID + inPort + actionsLength + pad + actions + data

	header = ofptHeader(13, payload)

	return header + payload