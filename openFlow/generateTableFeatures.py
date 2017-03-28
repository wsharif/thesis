from generateTableFeatureProps import generateTableFeatureProps

from random import randint, shuffle
from os import urandom
from struct import Struct

def generateTableFeatures(maxLength):
	tableFeatures = []

	while True:
		tableFeatureLength = randint(64 + 8, maxLength - len(''.join(tableFeatures)))

		tableId = urandom(1)
		pad = urandom(5)
		name = urandom(32)
		metadataMatch = urandom(8)
		metadataWrite = urandom(8)
		config = urandom(4)
		maxEntries = urandom(4)
		tableFeature = tableId + pad + name + metadataMatch + metadataWrite + config + maxEntries

		tableFeature += generateTableFeatureProps(tableFeatureLength - 2 - len(tableFeature))
		tableFeature = Struct('! H').pack(len(tableFeature)) + tableFeature

		if len(''.join(tableFeatures)) + len(tableFeature) <= maxLength:
			tableFeatures.append(tableFeature)

			if len(''.join(tableFeatures)) + 64 + 8 > maxLength:
				break

		else:
			break

	shuffle(tableFeatures)
	tableFeaturesLength = randint(0, len(tableFeatures))
	return ''.join(tableFeatures[:tableFeaturesLength])