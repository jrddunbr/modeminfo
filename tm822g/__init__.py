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

    def parseStatusPageData(self):
        print(self.statusPageData)

    def parse(self):
        self.parseStatusPageData()
