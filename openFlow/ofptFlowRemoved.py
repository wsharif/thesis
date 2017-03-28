from ofptHeader import ofptHeader
from generateMatch import generateMatch

from os import urandom
from random import randint
from struct import Struct

def ofptFlowRemoved(maxLength):
	cookie = urandom(8)
	priority = urandom(2)
	reason = Struct('! B').pack(randint(0, 3))
	tableId = urandom(1)
	durationSec = urandom(4)
	durationNSec = urandom(4)
	idleTimeout = urandom(2)
	hardTimeout = urandom(2)
	packetCount = urandom(8)
	byteCount = urandom(8)
	match = generateMatch(maxLength - 8 - 40)
	payload = cookie + priority + reason + tableId + durationSec + durationNSec + idleTimeout + hardTimeout + packetCount + byteCount + match

	header = ofptHeader(11, payload)

	return header + payload