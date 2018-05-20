#!/usr/bin/python3

# Specific Tests for Arris TM822G

from tm822g import tm822g
from time import sleep

modem = tm822g()

if modem.getPages():
    modem.parse()

    print()
    print("Modem Info:")
    for data in modem.info:
        print("{}: {}".format(data, modem.info[data]))

    print()
    print("Modem RX Info")
    for data in modem.rx:
        print(data)
        for thing in modem.rx[data]:
            print("\t{}: {}".format(thing, modem.rx[data][thing]))

    print()
    print("Modem TX Info")
    for data in modem.tx:
        print(data)
        for thing in modem.tx[data]:
            print("\t{}: {}".format(thing, modem.tx[data][thing]))
