#!/usr/bin/env python

from ofptHello import ofptHello
from ofptError import ofptError
from ofptEchoReq import ofptEchoReq
from ofptEchoRes import ofptEchoRes
from ofptExperimenter import ofptExperimenter
from ofptFeatureReq import ofptFeatureReq
from ofptFeatureRes import ofptFeatureRes
from ofptGetConfigReq import ofptGetConfigReq
from ofptGetConfigRes import ofptGetConfigRes
from ofptSetConfig import ofptSetConfig
from ofptPacketIn import ofptPacketIn
from ofptFlowRemoved import ofptFlowRemoved
from ofptPortStatus import ofptPortStatus
from ofptPacketOut import ofptPacketOut
from ofptFlowMod import ofptFlowMod
from ofptGroupMod import ofptGroupMod
from ofptPortMod import ofptPortMod
from ofptTableMod import ofptTableMod
from ofptMultipartReq import ofptMultipartReq
from ofptMultipartRes import ofptMultipartRes
from ofptBarrierReq import ofptBarrierReq
from ofptBarrierRes import ofptBarrierRes
from ofptQueueGetConfigReq import ofptQueueGetConfigReq
from ofptQueueGetConfigRes import ofptQueueGetConfigRes
from ofptRoleReq import ofptRoleReq
from ofptRoleRes import ofptRoleRes
from ofptGetAsyncReq import ofptGetAsyncReq
from ofptGetAsyncRes import ofptGetAsyncRes
from ofptSetAsync import ofptSetAsync
from ofptMeterMod import ofptMeterMod

from argparse import ArgumentParser
from csv import writer
from os.path import dirname, realpath
from random import randint
from socket import socket, AF_INET, SOCK_STREAM
from subprocess import check_output
from time import sleep

ipAddress = '127.0.0.1'
port = 6653
packetCount = 100000
maxLength = 1500 - 66
packetsFile = dirname(realpath(__file__)) + '/' + 'packets.txt'
resultsCsv = dirname(realpath(__file__)) + '/' + 'openFlowResults.csv'

parser = ArgumentParser()
parser.add_argument('logFile', help = 'Location of karaf.log log file')
args = parser.parse_args()
logFile = args.logFile

def generatePacket(type):
	global maxLength

	#can be expanded -> http://flowgrammable.org/sdn/openflow/message-layer/hello/
	if type == 0:
		return ofptHello()

	#not sure about data part, may have the structure of a normal openFlow packet
	elif type == 1:
		return ofptError(maxLength)

	elif type == 2:
		return ofptEchoReq(maxLength)

	elif type == 3:
		return ofptEchoRes(maxLength)

	elif type == 4:
		return ofptExperimenter(maxLength)

	elif type == 5:
		return ofptFeatureReq()

	elif type == 6:
		return ofptFeatureRes()

	elif type == 7:
		return ofptGetConfigReq()

	elif type == 8:
		return ofptGetConfigRes()

	elif type == 9:
		return ofptSetConfig()

	elif type == 10:
		return ofptPacketIn(maxLength)

	elif type == 11:
		return ofptFlowRemoved(maxLength)

	elif type == 12:
		return ofptPortStatus()

	elif type == 13:
		return ofptPacketOut(maxLength)

	elif type == 14:
		return ofptFlowMod(maxLength)

	elif type == 15:
		return ofptGroupMod(maxLength)

	elif type == 16:
		return ofptPortMod()

	elif type == 17:
		return ofptTableMod()

	elif type == 18:
		return ofptMultipartReq(maxLength)

	elif type == 19:
		return ofptMultipartRes(maxLength)

	elif type == 20:
		return ofptBarrierReq()

	elif type == 21:
		return ofptBarrierRes()

	elif type == 22:
		return ofptQueueGetConfigReq()

	elif type == 23:
		return ofptQueueGetConfigRes(maxLength)

	elif type == 24:
		return ofptRoleReq()

	elif type == 25:
		return ofptRoleRes()

	elif type == 26:
		return ofptGetAsyncReq()

	elif type == 27:
		return ofptGetAsyncRes()

	elif type == 28:
		return ofptSetAsync()

	elif type == 29:
		return ofptMeterMod(maxLength)

def sendPackets():
	global logFile, resultsCsv, packetCount, packetsFile

	pid = check_output(['pidof', 'java']).strip('\n')

	logLineCount = int(check_output(['wc', '-l', logFile]).split()[0])

	csvfile = open(resultsCsv, 'w')
	csvWriter = writer(csvfile)
	csvWriter.writerow(['Packet Number', 'CPU', 'Mem', 'Log Output'])

	packets = ''

	for i in range(packetCount):
		logOutput = ''

		sock = socket(AF_INET, SOCK_STREAM)
		sock.connect((ipAddress, port))

		sock.send(generatePacket(0))
		sleep(0.05)
		sock.send(generatePacket(6))
		sleep(0.05)

		packet = generatePacket(randint(0, 29))
		sock.send(packet)
		sleep(0.05)
		sock.close()

		usage = check_output(['ps', '-p', pid, '-o', '%cpu,%mem'])

		newLogLineCount = int(check_output(['wc', '-l', logFile]).split()[0])

		if newLogLineCount > logLineCount:
			logOutput += check_output(['tail', '-' + str(newLogLineCount - logLineCount), logFile]).split('|')[-1].strip()
			logLineCount = newLogLineCount

		csvWriter.writerow([i, usage.split()[2], usage.split()[3], logOutput])
		packets += '#packet' + packet

	csvfile.close()

	with open(packetsFile, 'w') as f:
		f.write(packets)

def main():
	sendPackets()

if __name__ == '__main__':
	main()