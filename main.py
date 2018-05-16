#!/usr/bin/python3

from dpc3216 import dpc3216
from pprint import pprint

modem = dpc3216()
modem.getPageData()
modem.getLangData()
#modem.printPageData()
if len(modem.pageData) > 10:
    print("modem data recieved")
if len(modem.pageData) > 10:
    print("modem lang recieved")
modem.parseLang()
modem.parse()

print()

print("Modem Information:")
for entry in modem.modemInfo:
    print("\t{}: {}".format(entry, modem.modemInfo[entry]))

print("Docsis Information:")
for entry in modem.docsisInfo:
    print("\t{}: {}".format(entry, modem.docsisInfo[entry]))

print("RX Information:")
for entry in modem.rx:
    data = modem.rx[entry]
    print("\t{}: Power: {}dBmV\tSignal To Noise Ratio: {}dB".format(entry, data[0], data[1]))

print("TX Information:")
for entry in modem.tx:
    data = modem.tx[entry]
    print("\t{}: Power: {}dBmV".format(entry, data))
