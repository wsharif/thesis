from os import urandom
from random import randint, shuffle
from struct import Struct

def generateQueues(maxLength):
	queues = []

	while True:
		queueLength = randint(32, maxLength - len(''.join(queues)))

		queueId = urandom(4)
		port = Struct('! I').pack(randint(0, 4294967039))

		maxCount = (queueLength - 16) / 16
		properties = ''

		for i in range(randint(1, maxCount)):
			property = Struct('! H').pack(1)
			length = Struct('! H').pack(16)
			pad = urandom(4)
			rate = urandom(2)
			pad2 = urandom(6)

			properties += property + length + pad + rate + pad2

		pad = urandom(6)

		queue = queueId + port + Struct('! H').pack(16 + len(properties)) + pad + properties

		if len(''.join(queues)) + len(queue) <= maxLength:
			queues.append(queue)

			if len(''.join(queues)) + 32 > maxLength:
				break

		else:
			break

	shuffle(queues)
	queuesLength = randint(0, len(queues))
	return ''.join(queues[:queuesLength])