from random import randint, shuffle
from os import urandom
from struct import Struct

def generateGroupStats(maxLength):
	groupStats = []

	while True:
		groupStatLength = randint(40, maxLength - len(''.join(groupStats)))

		pad = urandom(2)
		groupId = urandom(4)
		refCount = urandom(4)
		pad2 = urandom(4)
		packetCount = urandom(8)
		byteCount = urandom(8)
		durationSec = urandom(4)
		durationNSec = urandom(4)
		groupStat = pad + groupId + refCount + pad2 + packetCount + byteCount + durationSec + durationNSec

		maxCount = (groupStatLength - 2 - len(groupStat)) / 16

		for i in range(randint(0, maxCount)):
			packetCount = urandom(8)
			byteCount = urandom(8)
			bucketCounter = packetCount + byteCount

			groupStat += bucketCounter

		groupStat += Struct('! H').pack(len(groupStat)) + groupStat

		groupStats.append(groupStat)

		if len(''.join(groupStats)) + 40 > maxLength:
			break

	shuffle(groupStats)
	groupStatsLength = randint(0, len(groupStats))
	return ''.join(groupStats[:groupStatsLength])