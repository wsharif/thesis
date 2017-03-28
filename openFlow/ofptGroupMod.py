from ofptHeader import ofptHeader
from generateBuckets import generateBuckets

from os import urandom
from random import randint
from struct import Struct

def ofptGroupMod(maxLength):
	payloadLength = randint(8 + 32, maxLength - 8)

	command = Struct('! H').pack(randint(0, 2))
	type = Struct('! B').pack(randint(0, 3))
	pad = urandom(1)
	groupId = urandom(4)
	payload = command + type + pad + groupId

	buckets = generateBuckets(payloadLength - len(payload))
	payload += buckets

	header = ofptHeader(15, payload)

	return header + payload