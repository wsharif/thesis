from generateOxm import generateOxm

from os import urandom
from random import choice, randint, shuffle
from struct import Struct

def checkOxm(oxms, oxm, maxLength):
	if 4 + len(''.join(oxms)) + len(oxm) <= maxLength:
		return True
	else:
		return False

def generateMatch(maxLength):
	if maxLength % 8 != 0:
		maxLength = maxLength - (maxLength % 8)

	oxms = []

	while True:
		oxmClass = choice([0, 1, 32768, 65535])

		if oxmClass in (0, 1):
			oxm = generateOxm(oxmClass, randint(0, 255))

			if checkOxm(oxms, oxm, maxLength):
				oxms.append(oxm)
			else:
				break

		elif oxmClass == 32768:
			oxmField = choice([0, 2, 3, 4, 5, 6, 38])

			if oxmField == 0:
				oxm = generateOxm(oxmClass, 0 << 1, urandom(4))

				if checkOxm(oxms, oxm, maxLength):
					oxms.append(oxm)
				else:
					break

				if randint(0, 1):
					oxm = generateOxm(oxmClass, 1 << 1, urandom(4))

					if checkOxm(oxms, oxm, maxLength):
						oxms.append(oxm)
					else:
						break

			elif oxmField == 2:
				if randint(0, 1):
					oxm = generateOxm(oxmClass, 2 << 1, urandom(8))
				else:
					oxm = generateOxm(oxmClass, 2 << 1 | 1, urandom(16))

				if checkOxm(oxms, oxm, maxLength):
					oxms.append(oxm)
				else:
					break

			elif oxmField == 3:
				if randint(0, 1):
					oxm = generateOxm(oxmClass, 3 << 1, urandom(6))
				else:
					oxm = generateOxm(oxmClass, 3 << 1 | 1, urandom(12))

				if checkOxm(oxms, oxm, maxLength):
					oxms.append(oxm)
				else:
					break

			elif oxmField == 4:
				if randint(0, 1):
					oxm = generateOxm(oxmClass, 4 << 1, urandom(6))
				else:
					oxm = generateOxm(oxmClass, 4 << 1 | 1, urandom(12))

				if checkOxm(oxms, oxm, maxLength):
					oxms.append(oxm)
				else:
					break

			elif oxmField == 5:
				oxmPayload = choice([2048, 34525, 2054, 34887, 34888])
				oxm = generateOxm(oxmClass, 5 << 1, Struct('! H').pack(oxmPayload))

				if checkOxm(oxms, oxm, maxLength):
					oxms.append(oxm)
				else:
					break

				if randint(0, 1):
					if oxmPayload == 2048:
						oxmField = choice([8, 9, 10, 11, 12])

						if oxmField == 8:
							oxm = generateOxm(oxmClass, 8 << 1, urandom(1))

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

						elif oxmField == 9:
							oxm = generateOxm(oxmClass, 9 << 1, urandom(1))

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

						elif oxmField == 10:
							oxmPayload = Struct('! B').pack(choice([6, 17, 132, 1, 58]))
							oxm = generateOxm(oxmClass, 10 << 1, oxmPayload)

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

							if randint(0, 1):
								if oxmPayload == '\x06':
									if randint(0, 1):
										oxm = generateOxm(oxmClass, 13 << 1, urandom(2))
									else:
										oxm = generateOxm(oxmClass, 14 << 1, urandom(2))

									if checkOxm(oxms, oxm, maxLength):
										oxms.append(oxm)
									else:
										break

								elif oxmPayload == '\x11':
									if randint(0, 1):
										oxm = generateOxm(oxmClass, 15 << 1, urandom(2))
									else:
										oxm = generateOxm(oxmClass, 16 << 1, urandom(2))

									if checkOxm(oxms, oxm, maxLength):
										oxms.append(oxm)
									else:
										break

								elif oxmPayload == '\x84':
									if randint(0, 1):
										oxm = generateOxm(oxmClass, 17 << 1, urandom(2))
									else:
										oxm = generateOxm(oxmClass, 18 << 1, urandom(2))

									if checkOxm(oxms, oxm, maxLength):
										oxms.append(oxm)
									else:
										break

								elif oxmPayload == '\x01':
									if randint(0, 1):
										oxm = generateOxm(oxmClass, 19 << 1, urandom(1))
									else:
										oxm = generateOxm(oxmClass, 20 << 1, urandom(1))

									if checkOxm(oxms, oxm, maxLength):
										oxms.append(oxm)
									else:
										break

								elif oxmPayload == '\x3a':
									oxmPayload = Struct('! B').pack(randint(135, 136))

									if randint(0, 1):
										oxm = generateOxm(oxmClass, 29 << 1, oxmPayload)
									else:
										oxm = generateOxm(oxmClass, 30 << 1, oxmPayload)

									if checkOxm(oxms, oxm, maxLength):
										oxms.append(oxm)
									else:
										break

									if randint(0, 1):
										if oxmPayload == '\x87':
											if randint(0, 1):
												oxm = generateOxm(oxmClass, 31 << 1, urandom(16))
											else:
												oxm = generateOxm(oxmClass, 32 << 1, urandom(6))

										elif oxmPayload == '\x88':
											if randint(0, 1):
												oxm = generateOxm(oxmClass, 31 << 1, urandom(16))
											else:
												oxm = generateOxm(oxmClass, 33 << 1, urandom(6))

										if checkOxm(oxms, oxm, maxLength):
											oxms.append(oxm)
										else:
											break

						if oxmField == 11:
							if randint(0, 1):
								oxm = generateOxm(oxmClass, 11 << 1, urandom(4))
							else:
								oxm = generateOxm(oxmClass, 11 << 1 | 1, urandom(8))

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

						elif oxmField == 12:
							if randint(0, 1):
								oxm = generateOxm(oxmClass, 12 << 1, urandom(4))
							else:
								oxm = generateOxm(oxmClass, 12 << 1 | 1, urandom(8))

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

					elif oxmPayload == 34525:
						oxmField = choice([8, 9, 10, 26, 27, 28, 39])

						if oxmField == 8:
							oxm = generateOxm(oxmClass, 8 << 1, urandom(1))

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

						elif oxmField == 9:
							oxm = generateOxm(oxmClass, 9 << 1, urandom(1))

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

						elif oxmField == 10:
							oxmPayload = Struct('! B').pack(choice([6, 17, 132, 1, 58]))
							oxm = generateOxm(oxmClass, 10 << 1, oxmPayload)

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

							if randint(0, 1):
								if oxmPayload == '\x06':
									if randint(0, 1):
										oxm = generateOxm(oxmClass, 13 << 1, urandom(2))
									else:
										oxm = generateOxm(oxmClass, 14 << 1, urandom(2))

									if checkOxm(oxms, oxm, maxLength):
										oxms.append(oxm)
									else:
										break

								elif oxmPayload == '\x11':
									if randint(0, 1):
										oxm = generateOxm(oxmClass, 15 << 1, urandom(2))
									else:
										oxm = generateOxm(oxmClass, 16 << 1, urandom(2))

									if checkOxm(oxms, oxm, maxLength):
										oxms.append(oxm)
									else:
										break

								elif oxmPayload == '\x84':
									if randint(0, 1):
										oxm = generateOxm(oxmClass, 17 << 1, urandom(2))
									else:
										oxm = generateOxm(oxmClass, 18 << 1, urandom(2))

									if checkOxm(oxms, oxm, maxLength):
										oxms.append(oxm)
									else:
										break

								elif oxmPayload == '\x01':
									if randint(0, 1):
										oxm = generateOxm(oxmClass, 19 << 1, urandom(1))
									else:
										oxm = generateOxm(oxmClass, 20 << 1, urandom(1))

									if checkOxm(oxms, oxm, maxLength):
										oxms.append(oxm)
									else:
										break

								elif oxmPayload == '\x3a':
									oxmPayload = Struct('! B').pack(randint(135, 136))

									if randint(0, 1):
										oxm = generateOxm(oxmClass, 29 << 1, oxmPayload)
									else:
										oxm = generateOxm(oxmClass, 30 << 1, oxmPayload)

									if checkOxm(oxms, oxm, maxLength):
										oxms.append(oxm)
									else:
										break

									if randint(0, 1):
										if oxmPayload == '\x87':
											if randint(0, 1):
												oxm = generateOxm(oxmClass, 31 << 1, urandom(16))
											else:
												oxm = generateOxm(oxmClass, 32 << 1, urandom(6))

										elif oxmPayload == '\x88':
											if randint(0, 1):
												oxm = generateOxm(oxmClass, 31 << 1, urandom(16))
											else:
												oxm = generateOxm(oxmClass, 33 << 1, urandom(6))

										if checkOxm(oxms, oxm, maxLength):
											oxms.append(oxm)
										else:
											break

						elif oxmField == 26:
							if randint(0, 1):
								oxm = generateOxm(oxmClass, 26 << 1, urandom(16))
							else:
								oxm = generateOxm(oxmClass, 26 << 1 | 1, urandom(32))

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

						elif oxmField == 27:
							if randint(0, 1):
								oxm = generateOxm(oxmClass, 27 << 1, urandom(16))
							else:
								oxm = generateOxm(oxmClass, 27 << 1 | 1, urandom(32))

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

						elif oxmField == 28:
							if randint(0, 1):
								oxm = generateOxm(oxmClass, 28 << 1, urandom(3))
							else:
								oxm = generateOxm(oxmClass, 28 << 1 | 1, urandom(5))

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

						elif oxmField == 39:
							if randint(0, 1):
								oxm = generateOxm(oxmClass, 39 << 1, urandom(2))
							else:
								oxm = generateOxm(oxmClass, 39 << 1 | 1, urandom(3))

							if checkOxm(oxms, oxm, maxLength):
								oxms.append(oxm)
							else:
								break

					elif oxmPayload == 2054:
						oxmField = choice([21, 22, 23, 24, 25])

						if oxmField == 15:
							oxm = generateOxm(oxmClass, 21 << 1, urandom(2))

						elif oxmField == 16:
							if randint(0, 1):
								oxm = generateOxm(oxmClass, 22 << 1, urandom(4))
							else:
								oxm = generateOxm(oxmClass, 22 << 1 | 1, urandom(8))

						elif oxmField == 17:
							if randint(0, 1):
								oxm = generateOxm(oxmClass, 23 << 1, urandom(4))
							else:
								oxm = generateOxm(oxmClass, 23 << 1 | 1, urandom(8))

						elif oxmField == 18:
							if randint(0, 1):
								oxm = generateOxm(oxmClass, 24 << 1, urandom(6))
							else:
								oxm = generateOxm(oxmClass, 24 << 1 | 1, urandom(12))

						elif oxmField == 19:
							if randint(0, 1):
								oxm = generateOxm(oxmClass, 25 << 1, urandom(6))
							else:
								oxm = generateOxm(oxmClass, 25 << 1 | 1, urandom(12))

						if checkOxm(oxms, oxm, maxLength):
							oxms.append(oxm)
						else:
							break

					elif oxmPayload in (34887, 34888):
						oxmField = choice([34, 35, 36])

						if oxmField == 34:
							oxm = generateOxm(oxmClass, 34 << 1, urandom(3))

						elif oxmField == 35:
							oxm = generateOxm(oxmClass, 35 << 1, urandom(1))

						elif oxmField == 36:
							oxm = generateOxm(oxmClass, 36 << 1, urandom(1))

						if checkOxm(oxms, oxm, maxLength):
							oxms.append(oxm)
						else:
							break

			elif oxmField == 6:
				oxmPayload = Struct('! H').pack(randint(0, 8191))

				if randint(0, 1):
					oxm = generateOxm(oxmClass, 6 << 1, oxmPayload)
				else:
					oxm = generateOxm(oxmClass, 6 << 1 | 1, oxmPayload)

				if checkOxm(oxms, oxm, maxLength):
					oxms.append(oxm)
				else:
					break

				if randint(0, 1) and oxmPayload != '\x00\x00':
					oxm = generateOxm(oxmClass, 7 << 1, Struct('! B').pack(randint(0, 7)))

					if checkOxm(oxms, oxm, maxLength):
						oxms.append(oxm)
					else:
						break

			elif oxmField == 38:
				if randint(0, 1):
					oxm = generateOxm(oxmClass, 38 << 1, urandom(8))
				else:
					oxm = generateOxm(oxmClass, 38 << 1 | 1, urandom(16))

				if checkOxm(oxms, oxm, maxLength):
					oxms.append(oxm)
				else:
					break

		elif oxmClass == 65535:
			oxm = generateOxm(oxmClass, randint(0, 255), urandom(4))

			if checkOxm(oxms, oxm, maxLength):
				oxms.append(oxm)
			else:
				break

	oxmsLength = randint(0, len(''.join(oxms)))
	oxms = ''.join(oxms[:oxmsLength])

	oxms = Struct('! H').pack(1) + Struct('! H').pack(4 + len(oxms)) + oxms

	if len(oxms) % 8 != 0:
		oxms += urandom(8 - (len(oxms) % 8))

	return oxms