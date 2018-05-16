#!/usr/bin/python3

from dpc3216 import dpc3216
from time import sleep

modem = dpc3216()

while 1:
    modem.update()

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

    #sleep(0.1)
