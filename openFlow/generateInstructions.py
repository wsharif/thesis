from generateActions import generateActions

from os import urandom
from random import choice, randint, shuffle
from struct import Struct

def generateInstructions(maxLength):		
	instructions = []

	while True:
		instructionLength = randint(24, maxLength - len(''.join(instructions)))
		
		type = choice([1, 2, 3, 4, 5, 6, 65535])

		if type == 1:
			tableId = urandom(1)
			pad = urandom(3)
			instruction = tableId + pad

		elif type == 2:
			pad = urandom(4)
			metadata = urandom(8)
			metadataMask = urandom(8)
			instruction = pad + metadata + metadataMask

		elif type in (3, 4, 5):
			pad = urandom(4)
			actionsLength = randint(0, instructionLength - 4 - 4)
			actions = generateActions(actionsLength)
			instruction = pad + actions

		elif type == 6:
			meterId = urandom(4)
			instruction = meterId

		elif type == 65535:
			experimenterId = urandom(4)
			instruction = experimenterId

		instruction = Struct('! H').pack(type) + Struct('! H').pack(4 + len(instruction)) + instruction

		if len(''.join(instructions)) + len(instruction) <= maxLength:
			instructions.append(instruction)

			if len(''.join(instructions)) + 24 > maxLength:
				break

		else:
			break

	shuffle(instructions)
	instructionsLength = randint(0, len(instructions))
	return ''.join(instructions[:instructionsLength])