from ofptHeader import ofptHeader
from generateMatch import generateMatch
from generateInstructions import generateInstructions
from generateGroupStats import generateGroupStats
from generateGroupDescriptions import generateGroupDescriptions
from generateMeterStats import generateMeterStats
from generateMeterConfigs import generateMeterConfigs
from generateTableFeatures import generateTableFeatures
from generateBuckets import generateBuckets
from generateFlags import generateFlags
from generateMeterBands import generateMeterBands
from generateTableFeatureProps import generateTableFeatureProps

from os import urandom
from struct import Struct
from random import choice, randint, shuffle

def ofptMultipartRes(maxLength):
	type = choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 65535])
	flags = Struct('! H').pack(randint(0, 1))
	pad = urandom(4)
	payload = Struct('! H').pack(type) + flags + pad

	if type == 0:
		mfrDesc	= urandom(256)
		hwDesc = urandom(256)
		swDesc = urandom(256)
		serialNum = urandom(32)
		dpDesc = urandom(256)
		payload += mfrDesc + hwDesc + swDesc + serialNum + dpDesc

	elif type == 1:
		payloadLength = randint(8 + 48 + 52 + 24, maxLength - 8)

		tableId = urandom(1)
		pad = urandom(1)
		durationSec = urandom(4)
		durationNSec = urandom(4)
		priority = urandom(2)
		idleTimeout = urandom(2)
		hardTimeout = urandom(2)
		pad2 = urandom(6)
		cookie = urandom(8)
		packetCount = urandom(8)
		byteCount = urandom(8)
		tempPayload = tableId + pad + durationSec + durationNSec + priority + idleTimeout + hardTimeout + pad2 + cookie + packetCount + byteCount

		if randint(0, 1):
			match = generateMatch(payloadLength - len(payload) - 2 - len(tempPayload) - 24)
			instructions = generateInstructions(payloadLength - len(payload) - 2 - len(tempPayload) - len(match))
		else:
			instructions = generateInstructions(payloadLength - len(payload) - 2 - len(tempPayload) - 52)
			match = generateMatch(payloadLength - len(payload) -2 - len(tempPayload) - len(instructions))

		tempPayload += match + instructions
		payload += Struct('! H').pack(2 + len(tempPayload)) + tempPayload

	elif type == 2:
		packetCount = urandom(8)
		byteCount = urandom(8)
		flowCount = urandom(4)
		pad = urandom(4)
		payload += packetCount + byteCount + flowCount + pad

	elif type == 3:
		tableId = urandom(1)
		pad = urandom(3)
		activeCount = urandom(4)
		lookupCount = urandom(8)
		matchedCount = urandom(8)
		payload += tableId + pad + activeCount + lookupCount + matchedCount

	elif type == 4:
		portNumber = Struct('! I').pack(randint(0, 4294967279))
		pad = urandom(4)
		rxPackets = urandom(8)
		txPackets = urandom(8)
		rxBytes = urandom(8)
		txBytes = urandom(8)
		rxDropped = urandom(8)
		txDropped = urandom(8)
		rxErrors = urandom(8)
		txErrors = urandom(8)
		rxFrameErr = urandom(8)
		rxOverErr = urandom(8)
		rxCrcErr = urandom(8)
		collisions = urandom(8)
		durationSec = urandom(4)
		durationNSec = urandom(4)
		payload += portNumber + pad + rxPackets + txPackets + rxBytes + txBytes + rxDropped + txDropped + rxErrors + txErrors + rxFrameErr + rxOverErr + rxCrcErr + collisions + durationSec + durationNSec

	elif type == 5:
		portNumber = Struct('! I').pack(randint(0, 4294967279))
		queueId = urandom(4)
		txBytes = urandom(8)
		txPackets = urandom(8)
		txErrors = urandom(8)
		durationSec = urandom(4)
		durationNSec = urandom(4)
		payload += portNumber + queueId + txBytes + txPackets + txErrors + durationSec + durationNSec

	elif type == 6:
		payloadLength = randint(48, maxLength - 8)

		groupStats = generateGroupStats(payloadLength - len(payload))
		payload += groupStats

	elif type == 7:
		payloadLength = randint(48, maxLength - 8)

		groupDescriptions = generateGroupDescriptions(payloadLength - len(payload))
		payload += groupDescriptions

	elif type == 8:
		types = Struct('! I').pack(randint(0, 15))
		capabilities = Struct('! I').pack(randint(0, 15))
		maxGroups = urandom(4)
		maxGroups2 = urandom(4)
		maxGroups3 = urandom(4)
		maxGroups4 = urandom(4)
		actions = Struct('! I').pack(generateFlags([2**i for i in ([0, 11, 12] + range(15, 28))]))
		actions2 = Struct('! I').pack(generateFlags([2**i for i in ([0, 11, 12] + range(15, 28))]))
		actions3 = Struct('! I').pack(generateFlags([2**i for i in ([0, 11, 12] + range(15, 28))]))
		actions4 = Struct('! I').pack(generateFlags([2**i for i in ([0, 11, 12] + range(15, 28))]))
		payload += types + capabilities + maxGroups + maxGroups2 + maxGroups3 + maxGroups4 + actions + actions2 + actions3 + actions4

	elif type == 9:
		payloadLength = randint(64, maxLength - 8)

		meterStats = generateMeterStats(payloadLength - len(payload))
		payload += meterStats

	elif type == 10:
		payloadLength = randint(16, maxLength - 8)

		meterConfigs = generateMeterConfigs(payloadLength - len(payload))
		payload += meterConfigs

	elif type == 11:
		maxMeter = urandom(4)
		bandType = urandom(4)
		capabilities = urandom(4)
		maxBands = urandom(1)
		maxColor = urandom(1)
		pad = urandom(2)
		payload += maxMeter + bandType + capabilities + maxBands + maxColor + pad

	elif type == 12:
		payloadLength = randint(80, maxLength - 8)

		tableFeatures = generateTableFeatures(payloadLength - len(payload))
		payload += tableFeatures

	elif type == 13:
		maxCount = (maxLength - 8 - 8) / 64

		for i in range(randint(0, maxCount)):
			portID = Struct('! I').pack(choice([4294967040, 4294967288, 4294967289, 4294967290, 4294967291, 4294967292, 4294967293, 4294967294, 4294967295]))
			pad = urandom(4)
			hwAddr = urandom(6)
			pad2 = urandom(2)
			name = urandom(16)
			config = Struct('! I').pack(generateFlags(2**i for i in [0, 2, 5, 6]))
			state = Struct('! I').pack(randint(0, 7))
			current = Struct('! I').pack(randint(0, 65535))
			advertised = Struct('! I').pack(randint(0, 65535))
			supported = Struct('! I').pack(randint(0, 65535))
			peer = Struct('! I').pack(randint(0, 65535))
			currSpeed = urandom(4)
			maxSpeed = urandom(4)
			payload += portID + pad + hwAddr + pad2 + name + config + state + current + advertised + supported + peer + currSpeed + maxSpeed

	elif type == 65535:
		experimenterId = urandom(4)
		experimenterType = urandom(4)
		payload += experimenterId + experimenterType

	header = ofptHeader(19, payload)

	return header + payload