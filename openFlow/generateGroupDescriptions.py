from generateBuckets import generateBuckets

from random import randint, shuffle
from os import urandom
from struct import Struct

def generateGroupDescriptions(maxLength):
	groupDescriptions = []

	while True:
		groupDescriptionLength = randint(8 + 32, maxLength - len(''.join(groupDescriptions)))

		type = urandom(1)
		pad = urandom(1)
		groupId = urandom(4)
		groupDescription = type + pad + groupId

		buckets = generateBuckets(groupDescriptionLength - 2 - len(groupDescription))
		groupDescription += buckets
		groupDescription = Struct('! H').pack(2 + len(groupDescription)) + groupDescription

		if len(''.join(groupDescriptions)) + len(groupDescription) <= maxLength:
			groupDescriptions.append(groupDescription)

			if len(''.join(groupDescriptions)) + 40 > maxLength:
				break

		else:
			break

	shuffle(groupDescriptions)
	groupDescriptionsLength = randint(0, len(groupDescriptions))
	return ''.join(groupDescriptions[:groupDescriptionsLength])