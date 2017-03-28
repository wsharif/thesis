from generateActions import generateActions

from os import urandom
from random import randint, shuffle
from struct import Struct

def generateBuckets(maxLength):
	buckets = []

	while True:
		bucketLength = randint(16 + 16, maxLength - len(''.join(buckets)))

		weight = Struct('! H').pack(1)
		watchPort = urandom(4)
		watchGroup = urandom(4)
		pad = urandom(4)
		action = generateActions(bucketLength - 16)

		bucket = weight + watchPort + watchGroup + pad + action
		bucket = Struct('! H').pack(2 + len(bucket)) + bucket

		if len(''.join(buckets)) + len(bucket) <= maxLength:
			buckets.append(bucket)

			if len(''.join(buckets)) + 32 > maxLength:
				break

		else:
			break

	shuffle(buckets)
	bucketsLength = randint(0, len(buckets))
	return ''.join(buckets[:bucketsLength])