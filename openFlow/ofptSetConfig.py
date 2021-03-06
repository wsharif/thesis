from ofptHeader import ofptHeader

from random import randint
from os import urandom
from struct import Struct

def ofptSetConfig():
	flags = Struct('! H').pack(randint(0, 3))
	missSendLen = urandom(2)
	payload = flags + missSendLen

	header = ofptHeader(9, payload)

	return header + payload