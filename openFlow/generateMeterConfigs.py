from generateMeterBands import generateMeterBands

from os import urandom
from random import randint, shuffle
from struct import Struct

def generateMeterConfigs(maxLength):
	meterConfigs = []

	while True:
		meterConfigLength = randint(8, maxLength - len(''.join(meterConfigs)))

		flags = Struct('! H').pack(randint(0, 15))
		meterId = urandom(4)
		meterConfig = flags + meterId

		meterConfig += generateMeterBands(meterConfigLength - 2 - len(meterConfig))
		meterConfig = Struct('! H').pack(2 + len(meterConfig)) + meterConfig

		if len(''.join(meterConfigs)) + len(meterConfig) <= maxLength:
			meterConfigs.append(meterConfig)

			if len(''.join(meterConfigs)) + 8 > maxLength:
				break

		else:
			break

	shuffle(meterConfigs)
	meterConfigsLength = randint(0, len(meterConfigs))
	return ''.join(meterConfigs[:meterConfigsLength])