from ofptHeader import ofptHeader
from generateQueues import generateQueues

from os import urandom
from random import randint
from struct import Struct

def ofptQueueGetConfigRes(maxLength):
	payloadLength = randint(8 + 32, maxLength - 8)

	port = Struct('! I').pack(randint(0, 4294967039))
	pad = urandom(4)
	payload = port + pad

	queues = generateQueues(payloadLength - len(payload))
	payload += queues

	header = ofptHeader(23, payload)

	return header + payload