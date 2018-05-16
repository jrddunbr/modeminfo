#!/usr/bin/python3

from dpc3216 import dpc3216
from time import sleep
import datetime
import sys

DELAY = 15

if len(sys.argv) == 2:
    DELAY = int(sys.argv[1])

modem = dpc3216()

modem.update()

FIELDS = []
FIELDS.append("DATE")
for entry in modem.rx:
    FIELDS.append("\"{} RX Power\"".format(entry))
    FIELDS.append("\"{} SNR\"".format(entry))
for entry in modem.tx:
    FIELDS.append("\"{} TX Power\"".format(entry))

fstr = ""

for field in FIELDS:
    fstr += field + ","
print(fstr[:-1])

while 1:
    modem.update()

    now = datetime.datetime.now()

    strOut = now.isoformat() + ","

    for entry in modem.rx:
        data = modem.rx[entry]
        strOut += str(data[0]) + "," + str(data[1]) + ","

    for entry in modem.tx:
        strOut += str(modem.tx[entry]) + ","

    print(strOut[:-1])

    sleep(DELAY)
