# __init__.py
# Cisco DPC3216 Status Page Parser

import urllib.request

DEFAULT_IP = "192.168.100.1"
DEFAULT_PAGE = "Docsis_system.asp"
DEFAULT_LANG = "lang.js"

class dpc3216:
    def __init__(self, pageData="", langData=""):
        self.pageData = pageData
        self.langData = langData
        self.STATIC = len(pageData) > 0
        self.lang = {}
        self.modemInfo = {}
        self.docsisInfo = {}
        self.lang["venabled"] = "Enabled"
        print("Cisco DPC3216 Parsing Library Initialized")


    def getPageData(self):
        self.pageData = ""
        try:
            response = urllib.request.urlopen("http://{}/{}".format(DEFAULT_IP, DEFAULT_PAGE))
            self.pageData = response.read().decode("utf-8")
            if response.status != 200:
                print("There was a problem with fetching {}".format(DEFAULT_PAGE))
        except Exception as e:
            print("Error fetching file: {}".format(e))


    def getLangData(self):
        self.langData = ""
        try:
            response = urllib.request.urlopen("http://{}/{}".format(DEFAULT_IP, DEFAULT_LANG))
            self.langData = response.read().decode("utf-8")
            if response.status != 200:
                print("There was a problem with fetching {}".format(DEFAULT_LANG))
        except Exception as e:
            print("Error fetching file: {}".format(e))


    def parseLang(self):
        for line in self.langData.split("\n"):
            try:
                if line[0:3] == "var":
                    #print(line[4:-1])
                    name, rval = line[4:].split(";",1)[0].split("=",1)
                    if "\"" in rval:
                        val = rval.replace("\"","").strip()
                        self.lang[name] = val
                    else:
                        val = rval.strip()
                        self.lang[name] = val
                    #print("#Val: {} #Name: {}".format(val, name))
            except Exception as e:
                print("Error with line: {}\nLine: {}".format(e, line))
        #print(self.lang)


    def scriptToName(self, var):
        start = var.find("dw(") + 3
        end = var.find(");")
        #print("start: {} end: {}".format(start, end))
        if start != -1 and end != -1:
            name = var[start:end]
            try:
                return self.lang[name]
            except:
                return name[1:] + " << NAME RESOLVER FAIL"


    def parseTable(self, tableName, tableData):
        tableLines = tableData.split("\n")
        if tableName == "Modem Information" or tableName == "Docsis Information":
            name = ""
            for x in range(0, len(tableLines)):

                if "td id=" in tableLines[x]:
                    #print(tableLines[x].strip())
                    #print(tableLines[x+1].strip())
                    if "script" in tableLines[x+1]:
                        #print(self.scriptToName(tableLines[x+1]))
                        name = self.scriptToName(tableLines[x+1]).replace(":","")
                    else:
                        pass
                        #print(tableLines[x+1].strip())

                if "td headers=" in tableLines[x]:
                    #print(tableLines[x].strip())
                    #print(tableLines[x+1].strip())
                    val = ""
                    if "script" in tableLines[x+1]:
                        #print(self.scriptToName(tableLines[x+1]))
                        val = self.scriptToName(tableLines[x+1])
                    else:
                        #print(tableLines[x+1].strip())
                        val = tableLines[x+1].strip()

                    if tableName == "Modem Information":
                        self.modemInfo[name] = val
                    if tableName == "Docsis Information":
                        self.docsisInfo[name] = val
                #print ("x: {} line: {}".format(x, tableLines[x]))
        else:
            for x in range(0, len(tableLines)):
                #print ("x: {} line: {}".format(x, tableLines[x]))
                pass


    def parse(self):
        TABLE_NAMES = ["Modem Information", "Docsis Information", "Downstream Channel Information", "Upstream Channel Information"]
        VERBS = ["Start", "End"]
        strings = {}
        for tname in TABLE_NAMES:
            data = self.pageData
            startVerb = "{} {}".format(tname, VERBS[0])
            endVerb = "{} {}".format(tname, VERBS[1])
            start = data.find(startVerb)
            end = data.find(endVerb) + len(endVerb)
            if start != 0 and end != 0:
                #print("Start: {} End: {}".format(start, end))
                #print(data[start:end])
                self.parseTable(tname, data[start:end])
            else:
                print("Error, Start: {} End: {}".format(start, end))


    def printPageData(self):
        print()
        print(self.pageData)
        print()


    def update(self):
        if not self.STATIC:
            self.getPageData()
            self.getLangData()
            self.parseLang()
            self.parse()
        else:
            self.parseLang()
            self.parse()
