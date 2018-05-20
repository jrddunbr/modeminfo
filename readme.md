# modem info page parser

This is a project because why not.

It parses the status web page from two supported devices:

* Cisco DPC3216
* Arris TM822G

It queries on the local network (accessible from http://192.168.100.1)

## operation

### Typical Printout

On Linux:

Where `<program name` is either dpc3216.py or tm822g.py (depending on your device)

```/usr/bin/python3 <program name>```

### CSV Output (Cisco Only)

If you run `collect.sh` in bash, it will collect the data and put it into a CSV titled `collect.csv`

This uses the `collect.py` file, which outputs a set of headers, and then data in a compliant CSV format. `collect.py` takes one optional argument - the delay between collection

## Other Information (Cisco Only)

Parsing only requires (as it appears) the `Docsis_system.asp` and the `lang.js` files.

The `Docsis_system.asp` file (located at http://192.168.100.1/Docsis_system.asp) contains all of the status codes and basic printout information. Some of this, designed to be language independent, is javascript functions, which pull in variables from the `lang.js` file, and dump them into the webpage.

The `lang.js` file contains a bunch of variables, and their English translations. This file is really useful to get the names of fields on the status page, and some values are also listed in this table.

## Other Stuff

TODO: make main.py do. This should generically figure out which modem you have, and parse the correct information based on that, in a way that can be printed using the same API from either one.
