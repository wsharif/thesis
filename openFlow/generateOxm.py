from struct import Struct

def generateOxm(oxmClass, oxmField, oxmPayload = ''):
	oxmClass = Struct('! H').pack(oxmClass)
	oxmField = Struct('! B').pack(oxmField)
	oxmLength = Struct('! B').pack(len(oxmPayload))
	oxm = oxmClass + oxmField + oxmLength + oxmPayload

	return oxm