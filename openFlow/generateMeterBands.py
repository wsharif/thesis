from os import urandom
from random import choice, randint, shuffle
from struct import Struct

def generateMeterBands(maxLength):
	if maxLength == 0:
		return ''

	maxCount = maxLength / 16
	meterBands = ''

	for i in range(randint(0, maxCount)):
		type = choice([1, 2, 65535])
		length = Struct('! H').pack(16)
		rate = urandom(4)
		burstSize = urandom(4)
		meterBands += Struct('! H').pack(type) + length + rate + burstSize

		if type == 65535:
			experimenterId = urandom(4)
			meterBands += experimenterId
		else:
			precedenceLevel = urandom(1)
			pad = urandom(3)
			meterBands += precedenceLevel + pad

	return meterBands