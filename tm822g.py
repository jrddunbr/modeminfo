#!/usr/bin/python3

# Specific Tests for Arris TM822G

from tm822g import tm822g
from time import sleep

f = open("data/tm822g/cgi-bin/status_cgi")

full = ""

for line in f:
    full += line

f.close()

#modem = tm822g(statusPageData=full)
#modem.parse()

modem = tm822g()

modem.getPages()
modem.parse()

for data in modem.rx:
    print(data)
    print(modem.rx[data])

for data in modem.tx:
    print(data)
    print(modem.tx[data])

print("Uptime: {}".format(modem.info["uptime"]))
