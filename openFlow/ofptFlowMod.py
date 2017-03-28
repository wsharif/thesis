from ofptHeader import ofptHeader
from generateFlags import generateFlags
from generateMatch import generateMatch
from generateInstructions import generateInstructions

from os import urandom
from random import randint
from struct import Struct

def ofptFlowMod(maxLength):
	payloadLength = randint(40 + 52 + 24, maxLength - 8)

	cookie = Struct('! Q').pack(randint(0, 18446744073709551614))
	cookieMask = urandom(8)
	tableId = Struct('! B').pack(randint(0, 254))
	command = Struct('! B').pack(randint(0, 4))
	idleTimeout = urandom(2)
	hardTimeout = urandom(2)
	priority = urandom(2)
	bufferID = urandom(4)
	outPort = urandom(4)
	outGroup = urandom(4)
	flags = Struct('! H').pack(generateFlags([1, 2, 4, 10, 20]))
	pad = urandom(2)
	payload = cookie + cookieMask + tableId + command + idleTimeout + hardTimeout + priority + bufferID + outPort + outGroup + flags + pad

	if randint(0, 1):
		match = generateMatch(payloadLength - len(payload) - 24)
		instructions = generateInstructions(payloadLength - len(payload) - len(match))
	else:
		instructions = generateInstructions(payloadLength - len(payload) - 52)
		match = generateMatch(payloadLength - len(payload) - len(instructions))

	payload += match + instructions

	header = ofptHeader(14, payload)

	return header + payload