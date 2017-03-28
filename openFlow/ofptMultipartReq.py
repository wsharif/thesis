from ofptHeader import ofptHeader
from generateMatch import generateMatch
from generateTableFeatureProps import generateTableFeatureProps

from os import urandom
from random import choice, randint
from struct import Struct

def ofptMultipartReq(maxLength):
	type = choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 65535])
	flags = Struct('! H').pack(randint(0, 1))
	pad = urandom(4)
	payload = Struct('! H').pack(type) + flags + pad

	if type in (0, 3, 7, 8, 11, 13):
		pass

	elif type in (1, 2):
		payloadLength = randint(92, maxLength - 8)

		tableId = urandom(1)
		pad = urandom(3)
		outPort = Struct('! I').pack(randint(0, 4294967279))
		outGroup = urandom(4)
		pad2 = urandom(4)
		cookie = urandom(8)
		cookieMask = urandom(8)
		payload += tableId + pad + outPort + outGroup + pad2 + cookie + cookieMask

		match = generateMatch(payloadLength - len(payload))
		payload += match

	elif type == 4:
		portNumber = Struct('! I').pack(randint(0, 4294967279))
		pad = urandom(4)
		payload += portNumber + pad

	elif type == 5:
		portNumber = Struct('! I').pack(randint(0, 4294967279))
		queueId = urandom(4)
		payload += portNumber + queueId

	elif type == 6:
		groupId = urandom(4)
		pad = urandom(4)
		payload += groupId + pad

	elif type in (9, 10):
		meterId = urandom(4)
		pad = urandom(4)
		payload += meterId + pad

	elif type == 12:
		payloadLength = randint(80, maxLength - 8)

		tableId = urandom(1)
		pad = urandom(5)
		name = urandom(32)
		metadataMatch = urandom(8)
		metadataWrite = urandom(8)
		config = urandom(4)
		maxEntries = urandom(4)
		tempPayload = tableId + pad + name + metadataMatch + metadataWrite + config + maxEntries

		tempPayload += generateTableFeatureProps(payloadLength - len(payload) - 2 - len(tempPayload))
		tempPayload = Struct('! H').pack(2 + len(tempPayload)) + tempPayload
		payload += tempPayload

	elif type == 65535:
		experimenterId = urandom(4)
		experimenterType = urandom(4)
		payload += experimenterId + experimenterType

	header = ofptHeader(18, payload)

	return header + payload