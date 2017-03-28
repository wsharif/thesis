from os import urandom
from random import choice, randint, shuffle
from struct import Struct

def generateActions(maxLength, minimum = 0):
	actions = []

	while True:
		type = choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 65535])

		if type == 0:
			port = Struct('! I').pack(randint(0, 65519))
			maxLen = urandom(2)
			pad = urandom(6)
			action = port + maxLen + pad

		elif type == 1:
			vlanVid = urandom(2)
			pad = urandom(2)
			action = vlanVid + pad

		elif type == 2:
			vlanPc = urandom(1)
			pad = urandom(3)
			action = vlanPc + pad

		elif type == 3:
			action = ''

		elif type == 4:
			setDlSrc = urandom(6)
			pad = urandom(6)
			action = setDlSrc + pad

		elif type == 5:
			setDlSrc = urandom(6)
			pad = urandom(6)
			action = setDlSrc + pad

		elif type == 6:
			nwAddr = urandom(4)
			action = nwAddr

		elif type == 7:
			nwAddr = urandom(4)
			action = nwAddr

		elif type == 8:
			nwToss = urandom(1)
			pad = urandom(3)
			action = nwToss + pad

		elif type in (9, 10):
			port = Struct('! H').pack(randint(0, 65519))
			pad = urandom(2)
			action = port + pad

		elif type == 10:
			port = Struct('! H').pack(randint(0, 65519))
			pad = urandom(2)
			action = port + pad

		elif type == 11:
			pad = urandom(4)
			action = pad

		elif type == 65535:
			vendor = urandom(4)
			action = vendor

		action = Struct('! H').pack(type) + Struct('! H').pack(4 + len(action)) + action

		if len(''.join(actions)) + len(action) <= maxLength:
			actions.append(action)

			if len(''.join(actions)) + 16 > maxLength:
				break

		else:
			break

	shuffle(actions)
	actionsLength = randint(minimum, len(actions))
	return ''.join(actions[:actionsLength])