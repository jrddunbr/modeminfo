#!/usr/bin/python3

# Specific Tests for Arris TM822G

from tm822g import tm822g
from time import sleep

modem = tm822g()

modem.getPages()
modem.parse()
