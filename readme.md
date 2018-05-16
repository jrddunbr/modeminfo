# modem info page parser for Cisco DPC3216

This is a project because why not.

It parses the status webpage from a Cisco DPC3216 on the local network (accessible from http://192.168.100.1) and reads everything in.

## operation

### Typical Printout

On Linux:

```/usr/bin/python3 main.py```

### CSV Output

If you run `collect.sh` in bash, it will collect the data and put it into a CSV titled `collect.csv`

This uses the `collect.py` file, which outputs a set of headers, and then data in a compliant CSV format. `collect.py` takes one optional argument - the delay between collection

## Other Information

Parsing only requires (as it appears) the `Docsis_system.asp` and the `lang.js` files.

The `Docsis_system.asp` file (located at http://192.168.100.1/Docsis_system.asp) contains all of the status codes and basic printout information. Some of this, designed to be language independent, is javascript functions, which pull in variables from the `lang.js` file, and dump them into the webpage.

The `lang.js` file contains a bunch of variables, and their English translations. This file is really useful to get the names of fields on the status page, and some values are also listed in this table.

## Licensing

Since none of the Cisco configuration data, binaries, or webpages/variables are stored in this repository (and are generated/parsed/fetched on the fly when the program is in normal operation), I don't have to worry about licensing terms for their software/firmware. See `license.txt` for the license for this repository
