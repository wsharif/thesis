#!/usr/bin/env python

from string import letters, digits, punctuation
from re import compile
from os.path import dirname, realpath
from random import choice, randint, shuffle
from subprocess import check_output
from csv import writer
from requests import get, delete, post, put
from requests.auth import HTTPBasicAuth

ipAddress = '127.0.0.1'
port = '8181'
username = 'admin'
password = 'admin'
maxUrlLength = 5908 - len('/restconf')
maxPayloadLength = 65536 - 66 - 6145
requestsCount = 100000
requestsFile = dirname(realpath(__file__)) + '/' + 'requests.txt'
modifiedRequestsFile = dirname(realpath(__file__)) + '/' + 'modifiedRequests.txt'
resultsCsv = dirname(realpath(__file__)) + '/' + 'restconfResults.csv'
logFile = '../distribution-karaf-0.5.2-Boron-SR2/data/log/karaf.log'
urlCharacters = [i for i in letters + digits + punctuation] + ['%' + hex(i)[2:].zfill(2) for i in range(256)]

for i in ['%', '[', ']']:
	urlCharacters.remove(i)

def modifyUrl(url):
	global maxUrlLength, urlCharacters

	regex = compile('{.+?}')
	reserve = (len(regex.split(url)) - 1) * 3
	urlPartsLength = randint(reserve, maxUrlLength - len(''.join(regex.split(url))))
	urlParts = []

	for i in range(len(regex.split(url)) - 1):
		reserve -= 3
		urlPartLength = randint(3, urlPartsLength - reserve)
		urlPart = ''

		while True:
			urlPart += choice(urlCharacters)

			if len(urlPart) + 3 > urlPartLength:
				break

		urlPartsLength -= len(urlPart)
		urlPart = urlPart.replace('\\', '\\\\')
		urlParts.append(urlPart)

	shuffle(urlParts)

	for i in urlParts:
		url = regex.sub(i, url, 1)

	return url

def generateString(maxValueLength):
	valueLength = randint(6, maxValueLength)
	count = valueLength / 6
	value = ''

	for i in range(count):
		value += '\u' + hex(randint(0, 65535))[2:].zfill(4)

	return value

def generateInteger(maxValueLength):
	if randint(0, 1):
		valueLength = randint(1, min(19, (maxValueLength - 1)))
		value = '-'

	else:
		valueLength = randint(1, min(19, maxValueLength))
		value = ''

	for i in range(valueLength):
		if i == 0:
			value += str(randint(1, 9))

		else:
			value += str(randint(0, 9))

	return value

def generateNumber(maxValueLength):
	if randint(0, 1):
		value = generateInteger(maxValueLength)

	else:
		if randint(0, 1):
			valueLength = randint(2, maxValueLength - 2)
			value = '-'

		else:
			valueLength = randint(2, maxValueLength - 1)
			value = ''
						
		for i in range(valueLength):
			if i == 0 or i == valueLength - 1:
				value += str(randint(1, 9))

			else:
				value += str(randint(0, 9))

		decimalPointIndex = randint(1, len(value) - 1)
		value = value[:decimalPointIndex] + '.' + value[decimalPointIndex:]

	return value

def generateBoolean():
	if randint(0, 1):
		value = 'True'

	else:
		value = 'False'

	return value

def generateObject(maxValueLength):
	objectLength = randint(20, maxValueLength)
	keys = []
	values = []

	while True:
		if randint(0, 1):
			keyLength = randint(6, objectLength - 2  - len(keys) * 2 - len(''.join(keys)) - len(''.join(values)) - 1 - 2 - 1 - 2 - 6)
			valueLength = randint(6, objectLength - 2  - len(keys) * 2 - len(''.join(keys)) - len(''.join(values)) - 1 - 2 - keyLength - 1 - 2)

		else:
			valueLength = randint(6, objectLength - 2  - len(keys) * 2 - len(''.join(keys)) - len(''.join(values)) - 1 - 2 - 1 - 2 - 6)
			keyLength = randint(6, objectLength - 2  - len(keys) * 2 - len(''.join(keys)) - len(''.join(values)) - 1 - 2 - valueLength - 1 - 2)

		key = '"%s"' %generateString(keyLength)

		valueType = choice(['string', 'integer', 'number', 'boolean'])
		if valueType == 'string':
			value = '"%s"' %generateString(valueLength)

		elif valueType == 'integer':
			value = generateInteger(valueLength)

		elif valueType == 'number':
			value = generateNumber(valueLength)

		elif valueType == 'boolean':
			value = generateBoolean()

		if 2 + len(keys) * 2 + len(''.join(keys)) + len(''.join(values)) + 1 + len(key) + 1 + len(value) <= objectLength:
			keys.append(key)
			values.append(value)

			if 2 + len(keys) * 2 + len(''.join(keys)) + len(''.join(values)) + 18 > objectLength:
				break

		else:
			break

	shuffle(keys)

	for i, j in enumerate(keys):
		if i == 0:
			object = '{' + j + ':' + values[i] + '}'

		else:
			object = object[:-1] + ',' + j + ':' + values[i] + '}'

	return object

def modifyPayload(payload):
	global maxPayloadLength

	valueTypes = {}
	values = {}

	if payload.count('string'):
		valueTypes['string'] = payload.count('string')
		values['string'] = []

	if payload.count('\"integer\"'):
		valueTypes['\"integer\"'] = payload.count('\"integer\"')
		values['\"integer\"'] = []

	if payload.count('\"number\"'):
		valueTypes['\"number\"'] = payload.count('\"number\"')
		values['\"number\"'] = []

	if payload.count('\"boolean\"'):
		valueTypes['\"boolean\"'] = payload.count('\"boolean\"')
		values['\"boolean\"'] = []

	if payload.count('\"object\"'):
		valueTypes['\"object\"'] = payload.count('\"object\"')
		values['\"object\"'] = []

	tempPayload = ''.join(payload.split('string'))
	tempPayload = ''.join(tempPayload.split('\"integer\"'))
	tempPayload = ''.join(tempPayload.split('\"number\"'))
	tempPayload = ''.join(tempPayload.split('\"boolean\"'))
	tempPayload = ''.join(tempPayload.split('\"object\"'))
	payloadLength = len(tempPayload)

	reserve = payload.count('string') * 6 + payload.count('\"integer\"') * 2 + payload.count('\"number\"') * 4 + payload.count('\"boolean\"') * 5 + payload.count('\"object\"') * 20

	while valueTypes:
		valueType = choice(valueTypes.keys())

		if valueType == 'string':
			reserve -= 6
			maxValueLength = maxPayloadLength - payloadLength - reserve
			value = generateString(maxValueLength)

		elif valueType == '\"integer\"':
			reserve -= 2
			maxValueLength = maxPayloadLength - payloadLength - reserve
			value = generateInteger(maxValueLength)

		elif valueType == '\"number\"':
			reserve -= 4
			maxValueLength = maxPayloadLength - payloadLength - reserve
			value = generateNumber(maxValueLength)

		elif valueType == '\"boolean\"':
			reserve -= 5
			maxValueLength = maxPayloadLength - payloadLength - reserve
			value = generateBoolean()

		elif valueType == '\"object\"':
			reserve -= 20
			maxValueLength = maxPayloadLength - payloadLength - reserve
			value = generateObject(maxValueLength)

		valueTypes[valueType] -= 1
		if not valueTypes[valueType]:
			del valueTypes[valueType]

		payloadLength += len(value)
		values[valueType].append(value)

	for valueType, valueList in values.iteritems():
		shuffle(valueList)

		for i in valueList:
			payload = payload.replace(valueType, i, 1)

	return payload

def modifyRequests():
	global requestsFile, modifiedRequestsFile, maxUrlLength

	with open(requestsFile, 'r') as f:
		requests = f.read()

	modifiedRequests = ''

	for i in requests.split('#httpRequest')[1:]:
		request = i
		method = request.split('\n')[1]
		url = request.split('\n')[2]
		payload = '\n'.join(request.split('\n')[3:])

		if '{' in url:
			url = modifyUrl(url)
			if len(url) > maxUrlLength:
				print 'Error'

		payload = modifyPayload(payload)

		modifiedRequests += '#httpRequest' + '\n' + method + '\n' + url + '\n' + payload

	with open(modifiedRequestsFile, 'w') as f:
		f.write(modifiedRequests)

	return modifiedRequests

def sendRequests(requests):
	global resultsCsv, requestsCount, ipAddress, port, username, password, logfile

	pid = check_output(['pidof', 'java']).strip('\n')

	logLineCount = int(check_output(['wc', '-l', logFile]).split()[0])

	csvfile = open(resultsCsv, 'w')
	csvWriter = writer(csvfile)
	csvWriter.writerow(['Request Number', 'Method', 'URL', 'Status Code', 'CPU', 'Mem', 'Requests Error', 'Log Output'])

	for i in range(requestsCount):
		request = choice(requests.split('#httpRequest')[1:])
		method = request.split()[0]
		url = request.split()[1]
		url = ('http://%s:%s/restconf' %(ipAddress, port)) + url
		payload = ''.join(request.split()[2:])
		requestsError = ''
		statusCode = ''
		logOutput = ''

		if method == 'post':
			try:
				response = post(url, auth = HTTPBasicAuth(username, password), headers = {'Content-Type': 'application/json'}, data = payload)
				statusCode += str(response.status_code)
			except Exception as e:
				requestsError += str(e)

		elif method == 'get':
			try:
				response = get(url, auth = HTTPBasicAuth(username, password))
				statusCode += str(response.status_code)
			except Exception as e:
				requestsError += str(e)

		elif method == 'put':
			try:
				response = put(url, auth = HTTPBasicAuth(username, password), headers = {'Content-Type': 'application/json'}, data = payload)
				statusCode += str(response.status_code)
			except Exception as e:
				requestsError += str(e)

		elif method == 'delete':
			try:
				response = delete(url, auth = HTTPBasicAuth(username, password))
				statusCode += str(response.status_code)
			except Exception as e:
				requestsError += str(e)

		usage = check_output(['ps', '-p', pid, '-o', '%cpu,%mem'])

		newLogLineCount = int(check_output(['wc', '-l', logFile]).split()[0])

		if newLogLineCount > logLineCount:
			logOutput += check_output(['tail', '-' + str(newLogLineCount - logLineCount), logFile]).split('|')[-1].strip()
			logLineCount = newLogLineCount

		csvWriter.writerow([i, method, url, statusCode, usage.split()[2], usage.split()[3], requestsError, logOutput])

	csvfile.close()

def main():
	sendRequests(modifyRequests())

if __name__ == '__main__':
	main()