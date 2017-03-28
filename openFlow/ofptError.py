from ofptHeader import ofptHeader

from random import randint
from struct import Struct
from os import urandom

def ofptError(maxLength):
	errorType = randint(0, 13)

	if errorType == 0:
		errorCode = Struct('! H').pack(randint(0, 1))

	elif errorType == 1:
		errorCode = Struct('! H').pack(randint(0, 13))

	elif errorType == 2:
		errorCode = Struct('! H').pack(randint(0, 15))

	elif errorType == 3:
		errorCode = Struct('! H').pack(randint(0, 8))

	elif errorType in (4, 12):
		errorCode = Struct('! H').pack(randint(0, 11))

	elif errorType == 5:
		errorCode = Struct('! H').pack(randint(0, 7))

	elif errorType == 6:
		errorCode = Struct('! H').pack(randint(0, 14))

	elif errorType == 7:
		errorCode = Struct('! H').pack(randint(0, 4))

	elif errorType in (8, 9, 10, 11):
		errorCode = Struct('! H').pack(randint(0, 2))

	elif errorType == 13:
		errorCode = Struct('! H').pack(randint(0, 5))

	data = urandom(randint(8, maxLength - 8 - 4))
	payload = Struct('! H').pack(errorType) + errorCode + data

	header = ofptHeader(1, payload)

	return header + payload