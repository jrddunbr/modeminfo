#__init__.py
# Arris TM822G Status Page(s) Parser

import urllib.request

DEFAULT_IP = "192.168.100.1"

STATUS_PAGE = "/cgi-bin/status_cgi"
VERSION_PAGE = "/cgi-bin/vers_cgi"
EVENT_LOG_PAGE = "/cgi-bin/vers_cgi"
MODEM_STATE_PAGE = "/cgi-bin/cm_state_cgi"

class tm822g:
    def __init__(self, statusPageData="", versionPageData="", eventLogPageData="", modemStatePageData=""):
        self.statusPageData = statusPageData
        self.versionPageData = versionPageData
        self.eventLogPageData = eventLogPageData
        self.modemStatePageData = modemStatePageData
        self.STATIC = self.statusPageData != ""
        self.rx = {}
        self.tx = {}
        self.info = {}
        self.docsis = {}
        self.interfaces = {}
        print("Arris TM822G Parsing Library Initialized")

    def getPages(self):
        good = True
        self.statusPageData = ""
        self.versionPageData = ""
        self.eventLogPageData = ""
        self.modemStatePageData = ""
        PAGE_LIST = [STATUS_PAGE, VERSION_PAGE, EVENT_LOG_PAGE, MODEM_STATE_PAGE]
        print("Starting Fetching Pages")
        for page in PAGE_LIST:
            try:
                response = urllib.request.urlopen("http://{}/{}".format(DEFAULT_IP, page))
                pageData = response.read().decode("utf-8")
                if response.status != 200:
                    print("There was a problem with fetching {}".format(page))
                    good = False
                else:
                    if page == STATUS_PAGE:
                        self.statusPageData = pageData
                    elif page == VERSION_PAGE:
                        self.versionPageData = pageData
                    elif page == EVENT_LOG_PAGE:
                        self.eventLogPageData = pageData
                    elif page == MODEM_STATE_PAGE:
                        self.eventLogPageData = pageData
                    else:
                        print("Uhhh.. We're not sure what to do with `{}`'s' data.".format(page))
            except Exception as e:
                print("Error fetching file: {}".format(e))
                good = False
        print("Done Fetching Pages")
        return good

    def tableParser(self, table):
        data = self.basicTableParser(table)
        if len(data) == 0:
            return ([], [])
        # If we get this far, we have a table with at least 1 row (which is a label at least)
        if len(data) == 1:
            return (data, [])
        # if we get this far, we totally have some rows
        labels = data.pop(0)
        return (labels, data)

    def basicTableParser(self, table):
        rows = table.count("<tr")
        if rows == 0:
            return []
        # now, if we're this far, we have rows
        data = []
        lastRowEnd = 0
        for row in range(0, rows):
            #print(row)
            trStart = table.find("<tr", lastRowEnd) + len("<tr")
            rowStart = table.find(">", trStart) + len(">")
            rowEnd = table.find("</tr>", rowStart) - len("</tr>")
            lastRowEnd = rowEnd
            rowData = table[rowStart:rowEnd]
            datums = rowData.count("<td")
            lastDatumEnd = rowStart
            cleanData = []
            for datum in range(0, datums):
                tdStart = table.find("<td", lastDatumEnd) + len("<td")
                datumStart = table.find(">", tdStart) + len(">")
                datumEnd = table.find("</td>", datumStart)
                lastDatumEnd = datumEnd
                datumData = table[datumStart:datumEnd]
                #print(datumData.strip())
                cleanData.append(datumData.strip())
            data.append(cleanData)
        return data

    def parseDownstreamTable(self, downstreamData):
        table = downstreamData.split("\n",1)[1]
        labels, data = self.tableParser(table)
        labels[0] = "Channel"
        #print(labels)
        for row in data:
            channel = "Channel " + row[0].replace("Downstream", "").strip()
            missing = False
            for datum in row:
                if "--" in datum:
                    missing = True
            self.rx[channel] = {}
            if "--" not in row[1]:
                self.rx[channel]["dcid"] = int(row[1])
            if "--" not in row[2]:
                self.rx[channel]["freq"] = float(row[2].strip("MHz")) #MHz is unit
            if "--" not in row[3]:
                self.rx[channel]["power"] = float(row[3].strip("dBmV")) # dBmV is unit
            if "--" not in row[4]:
                self.rx[channel]["snr"] = float(row[4].strip("dB")) # dB is unit
            if "--" not in row[5]:
                self.rx[channel]["modulation"] = str(row[5])
            if "--" not in row[6]:
                self.rx[channel]["octets"] = int(row[6])
            if "--" not in row[7]:
                self.rx[channel]["corrected"] = int(row[7])
            if "--" not in row[8]:
                self.rx[channel]["uncorrectable"] = int(row[8])
            self.rx[channel]["missing"] = missing

    def parseUpstreamTable(self, upstreamData):
        table = upstreamData.split("\n",1)[1]
        labels, data = self.tableParser(table)
        labels[0] = "Channel"
        #print(labels)
        for row in data:
            channel = "Channel " + row[0].replace("Upstream", "").strip()
            missing = False
            for datum in row:
                if "--" in datum:
                    missing = True
            self.tx[channel] = {}
            if "--" not in row[1]:
                self.tx[channel]["ucid"] = int(row[1])
            if "--" not in row[2]:
                self.tx[channel]["freq"] = float(row[2].strip("MHz")) #MHz is unit
            if "--" not in row[3]:
                self.tx[channel]["power"] = float(row[3].strip("dBmV")) # dBmV is unit
            if "--" not in row[4]:
                self.tx[channel]["channel_type"] = str(row[4])
            if "--" not in row[5]:
                self.tx[channel]["symbol_rate"] = str(row[5])
            if "--" not in row[6]:
                self.tx[channel]["modulation"] = str(row[6].split("\n")[0])
            self.tx[channel]["missing"] = missing

    def parseStatusPageData(self):
        data = self.statusPageData
        startVerb = "<h4> Downstream </h4>"
        endVerb = "</table>"
        dstart = data.find(startVerb)
        dend = data.find(endVerb, dstart) + len(endVerb)
        if dstart != 0 and dend != 0:
            #print("Start: {} End: {}".format(dstart, dend))
            downstreamData = data[dstart:dend]
            #print(downstreamData)
            self.parseDownstreamTable(downstreamData)
        #print(self.statusPageData)
        startVerb = "<h4> Upstream </h4>"
        endVerb = "</table>"
        ustart = data.find(startVerb, dend)
        uend = data.find(endVerb, ustart) + len(endVerb)
        if ustart != 0 and uend != 0:
            #print("Start: {} End: {}".format(ustart, uend))
            upstreamData = data[ustart:uend]
            #print(upstreamData)
            self.parseUpstreamTable(upstreamData)
        startVerb = "System Uptime:"
        endVerb = "</td>"
        sustart = data.find(startVerb, uend)
        sumid = data.find(endVerb, sustart) + len(endVerb)
        suend = data.find(endVerb, sumid)
        if sustart !=0 and suend != 0:
            #print("Start: {} End: {}".format(sustart, suend))
            #print(data[sumid:suend])
            uptime = data[sumid:suend].replace("<td>", "").strip()
            #print(uptime)
            self.info["uptime"] = uptime

    def parseVersionPageData(self):
        data = self.versionPageData
        headerVerb = "INSERT ARRIS PAGE CONTENT HERE"
        tableVerb = "<table"
        closeTableVerb = "</table>"
        iapch = data.find(headerVerb)
        uselessTable = data.find(tableVerb, iapch) + len(tableVerb)
        systemTableStart = data.find(tableVerb, uselessTable)
        systemTableEnd = data.find(closeTableVerb, systemTableStart)
        systemTable = data[systemTableStart:systemTableEnd]
        systemTableData = self.basicTableParser(systemTable)
        systemSplitData = systemTableData[1][1].split("<br>")

        systemString = systemSplitData[0].strip()
        hw_rev = systemSplitData[1].split(":",1)[1].strip()
        vendor = systemSplitData[2].split(":",1)[1].strip()
        bootloader = systemSplitData[3].split(":",1)[1].strip()
        software = systemSplitData[4].split(":",1)[1].strip()
        model = systemSplitData[5].split(":",1)[1].strip()
        serial = systemTableData[7][1]
        battery_fw = systemTableData[8][1]

        self.info["system_name"] = systemString
        self.info["hw_rev"] = hw_rev
        self.info["vendor"] = vendor
        self.info["boot_rev"] = bootloader
        self.info["sw_rev"] = software
        self.info["model"] = model
        self.info["serial"] = serial
        self.info["batt_fw"] = battery_fw

        rest = data[systemTableEnd:]

        startVerb = "Firmware Name:"
        midVerb = "<td"
        endVerb = "</td></tr>"

        fwNamePre = rest.find(startVerb) + len(startVerb)
        fwNameMid = rest.find(midVerb, fwNamePre) + len(midVerb)
        fwNameStart = rest.find(">", fwNameMid) + 1
        fwNameEnd = rest.find(endVerb, fwNameStart)

        fw_name = rest[fwNameStart:fwNameEnd]

        startVerb = "Firmware Build Time:"

        btPre = rest.find(startVerb) + len(startVerb)
        btMid = rest.find(midVerb, btPre) + len(midVerb)
        btStart = rest.find(">", btMid) + 1
        btEnd = rest.find(endVerb, btStart)

        bt = rest[btStart:btEnd]

        self.info["fw_name"] = fw_name
        self.info["build_time"] = bt

    def parse(self):
        self.parseStatusPageData()
        self.parseVersionPageData()
        print("Done Parsing")
