from random import randint, shuffle
from os import urandom
from struct import Struct

def generateMeterStats(maxLength):
	meterStats = []

	while True:
		meterStatLength = randint(56, maxLength - len(''.join(meterStats)))

		pad = urandom(6)
		flowCount = urandom(4)
		packetInCount = urandom(8)
		byteInCount = urandom(8)
		durationSec = urandom(4)
		durationNSec = urandom(4)
		meterStat = pad + flowCount + packetInCount + byteInCount + durationSec + durationNSec

		maxCount = (meterStatLength - 2 - 4 - len(meterStat)) / 16

		for i in range(randint(1, maxCount)):
			packetBandCount = urandom(8)
			byteBandCount = urandom(8)
			meterStat += packetBandCount + byteBandCount

		meterId = urandom(4)
		meterStat = meterId + Struct('! H').pack(6 + len(meterStat)) + meterStat

		if len(''.join(meterStats)) + len(meterStat) <= maxLength:
			meterStats.append(meterStat)

			if len(''.join(meterStats)) + 56 > maxLength:
				break

		else:
			break

	shuffle(meterStats)
	meterStatsLength = randint(0, len(meterStats))
	return ''.join(meterStats[:meterStatsLength])