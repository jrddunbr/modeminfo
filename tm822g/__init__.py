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
        self.modemInfo = {}
        self.docsisInfo = {}
        self.lan = {}
        print("Arris TM822G Parsing Library Initialized")

    def getPages(self):
        self.statusPageData = ""
        self.versionPageData = ""
        self.eventLogPageData = ""
        self.modemStatePageData = ""
        PAGE_LIST = [STATUS_PAGE, VERSION_PAGE, EVENT_LOG_PAGE, MODEM_STATE_PAGE]
        for page in PAGE_LIST:
            try:
                response = urllib.request.urlopen("http://{}/{}".format(DEFAULT_IP, page))
                pageData = response.read().decode("utf-8")
                if response.status != 200:
                    print("There was a problem with fetching {}".format(page))
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
        print("Finished fetching pages")

    def tableParser(self, table):
        #print(table)
        rows = table.count("<tr>") - 1
        labels = []
        data = []
        if rows <= -1:
            return ([], [])
        # if we're this far, there's at least a row of table labels
        labelStart = table.find("<tr>") + len("<tr>")
        labelEnd = table.find("</tr>", labelStart)
        rowData = table[labelStart:labelEnd].replace("\r", "").split("<td>")
        [labels.append(r.replace("</td>", "").strip()) for r in rowData if "</td>" in r]
        #print(labels)
        if rows == 0:
            return labels
        # if we're this far, we have some rows to work with
        rest = table[labelEnd + len("</tr>"):]
        lastRowEnd = 0
        for row in range(0, rows):
            #print("row: {}".format(row))
            rowStart = rest.find("<tr>", lastRowEnd) + len("<tr>")
            rowEnd = rest.find("</tr>", rowStart)
            lastRowEnd = rowEnd
            rowData = rest[rowStart:rowEnd].replace("\r", "").split("<td>")
            cleanData = [r.replace("</td>", "").strip() for r in rowData if "</td>" in r]
            data.append(cleanData)
        return (labels, data)

    def parseDownstreamTable(self, downstreamData):
        table = downstreamData.split("\n",1)[1]
        labels, data = self.tableParser(table)
        labels[0] = "Channel"
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
                self.tx[channel]["modulation"] = str(row[6])
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

    def parse(self):
        self.parseStatusPageData()
