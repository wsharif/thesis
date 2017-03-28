from ofptHeader import ofptHeader

from random import randint
from struct import Struct

def ofptSetAsync():
	packetInMask = Struct('! I').pack(randint(0, 7))
	packetInMask2 = Struct('! I').pack(randint(0, 7))
	packetStatusMask = Struct('! I').pack(randint(0, 7))
	packetStatusMask2 = Struct('! I').pack(randint(0, 7))
	flowRemovedMask = Struct('! I').pack(randint(0, 15))
	flowRemovedMask2 = Struct('! I').pack(randint(0, 15))
	payload = packetInMask + packetInMask2 + packetStatusMask + packetStatusMask2 + flowRemovedMask + flowRemovedMask2

	header = ofptHeader(28, payload)

	return header + payload