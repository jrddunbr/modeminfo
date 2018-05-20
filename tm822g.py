#!/usr/bin/python3

# Specific Tests for Arris TM822G

from tm822g import tm822g
from time import sleep

modem = tm822g()

PRINT_LOG = False

if modem.getPages():
    modem.parse()

    print()
    print("Modem Info:")
    for data in modem.info:
        print("{}: {}".format(data, modem.info[data]))

    print()
    print("Docsis Info:")
    for data in modem.docsis:
        print("{}: {}".format(data, modem.docsis[data]))

    print()
    print("Modem RX Info:")
    for data in modem.rx:
        print(data)
        for thing in modem.rx[data]:
            print("\t{}: {}".format(thing, modem.rx[data][thing]))

    print()
    print("Modem TX Info:")
    for data in modem.tx:
        print(data)
        for thing in modem.tx[data]:
            print("\t{}: {}".format(thing, modem.tx[data][thing]))

    if PRINT_LOG:
        print()
        print("Modem Log:")
        for label in modem.log["labels"]:
            print("{}\t".format(label), end="")
        print()
        for entry in modem.log["log"]:
            for col in entry:
                print("{}\t".format(col), end="")
            print()
