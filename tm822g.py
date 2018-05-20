#!/usr/bin/python3

# Specific Tests for Arris TM822G

from tm822g import tm822g
from time import sleep

modem = tm822g()

if modem.getPages():
    modem.parse()

    for data in modem.rx:
        print(data)
        print(modem.rx[data])

    for data in modem.tx:
        print(data)
        print(modem.tx[data])

    print("Uptime: {}".format(modem.info["uptime"]))
