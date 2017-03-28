from random import randint, choice, shuffle
from os import urandom
from struct import Struct

from generateOxm import generateOxm

def generateTableFeatureProps(maxLength):
	tableFeatureProps = []

	while True:
		tableFeaturePropLength = randint(0, maxLength - len(''.join(tableFeatureProps)) - 4)

		if tableFeaturePropLength % 8 != 0:
			tableFeaturePropLength = tableFeaturePropLength - (tableFeaturePropLength % 8)

		type = choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])

		if type in (0, 1):
			instructions = []

			while True:
				instructionType = choice([1, 2, 3, 4, 5, 6, 65535])

				if instructionType == 65535:
					experimenterId = urandom(4)
					instruction = experimenterId
				else:
					instruction = ''

				instruction = Struct('! H').pack(instructionType) + Struct('! H').pack(4 + len(instruction)) + instruction

				if len(''.join(instructions)) + len(instruction) <= tableFeaturePropLength:
					instructions.append(instruction)

					if len(''.join(instructions)) + 8 > tableFeaturePropLength:
						break

				else:
					break

			instructionsLength = randint(0, len(instructions))
			tableFeatureProp = ''.join(instructions[:instructionsLength])

		elif type in (2, 3):
			nextTableIds = urandom(randint(0, tableFeaturePropLength))

			tableFeatureProp = nextTableIds

		elif type in (4, 5, 6, 7):
			actions = []

			while True:
				actionType = choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 65535])

				if actionType == 65535:
					vendor = urandom(4)
					action = vendor
				else:
					action = ''

				action = Struct('! H').pack(actionType) + Struct('! H').pack(len(action)) + action

				if len(''.join(actions)) + len(action) <= tableFeaturePropLength:
					actions.append(action)

					if len(''.join(actions)) + 8 > tableFeaturePropLength:
						break

				else:
					break

			actionsLength = randint(0, len(actions))
			tableFeatureProp = ''.join(actions[:actionsLength])

		elif type in (8, 9, 10, 11, 12, 13):
			oxms = []

			while True:
				oxmClass = choice([0, 1, 32768, 65535])

				if oxmClass in (0, 1):
					oxm = generateOxm(oxmClass, randint(0, 255))
				elif oxmClass == 65535:
					oxm = generateOxm(oxmClass, randint(0, 255), urandom(4))
				else:
					oxmField = randint(0, 39)

					if oxmField in (2, 3, 4, 6, 11, 12, 22, 23, 24, 25, 26, 27, 28, 37, 38, 39):
						if randint(0, 1):
							oxm = generateOxm(oxmClass, oxmField << 1)
						else:
							oxm = generateOxm(oxmClass, oxmField << 1 | 1)
					else:
						oxm = generateOxm(oxmClass, oxmField << 1)

				if len(''.join(oxms)) + len(oxm) <= tableFeaturePropLength:
					oxms.append(oxm)

					if len(''.join(oxms)) + 8 > tableFeaturePropLength:
						break

				else:
					break

			oxmsLength = randint(0, len(oxms))
			tableFeatureProp = ''.join(oxms[:oxmsLength])

		tableFeatureProp = Struct('! H').pack(type) + Struct('! H').pack(4 + len(tableFeatureProp)) + tableFeatureProp

		if len(tableFeatureProp) % 8 != 0:
			tableFeatureProp += urandom(8 - (len(tableFeatureProp) % 8))

		if len(''.join(tableFeatureProps)) + len(tableFeatureProp) <= maxLength:
			tableFeatureProps.append(tableFeatureProp)

			if len(''.join(tableFeatureProps)) + 8 > maxLength:
				break

		else:
			break

	shuffle(tableFeatureProps)
	tableFeaturePropsLength = randint(0, len(tableFeatureProps))
	return ''.join(tableFeatureProps[:tableFeaturePropsLength])