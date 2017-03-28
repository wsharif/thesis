from ofptHeader import ofptHeader
from generateMeterBands import generateMeterBands

from random import choice, randint
from struct import Struct

def ofptMeterMod(maxLength):
	payloadLength = randint(8, maxLength - 8)

	command = Struct('! H').pack(randint(0, 2))
	flags = Struct('! H').pack(randint(0, 15))
	meterId = Struct('! I').pack(choice([0, 4294901760, 4294967293, 4294967294, 4294967295]))
	meterBands = generateMeterBands(payloadLength - 8)
	payload = command + flags + meterId + meterBands

	header = ofptHeader(29, payload)

	return header + payload