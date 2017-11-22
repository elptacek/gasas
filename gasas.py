#!/usr/bin/python

import json
import urllib
import sys
import os.path

from datetime import datetime
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
from optparse import OptionParser

# in case there is no last run time, use this
leNow = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

gsHost = 'https://www.googleapis.com/admin/reports/v1/activity/users/all/applications/'

def saveLastRunTime(lrt, which):
    fileName = "%s/%s" % (dataDir, which)
    file = open(fileName, "w+")
    file.write(lrt)
    file.close()

def getLastRunTime(which, where):
    fileName = "%s/%s" % (dataDir, which)
    if os.path.exists(fileName):
        file = open(fileName, "r")
        lrt = file.read().rstrip()
        file.close()
        return urllib.quote(lrt)
    else:
        return urllib.quote(leNow)

def fetchStuff(session, which):
    #uri =  "%s%s?startTime=%s" % (gsHost, which, getLastRunTime(which, dataDir))
    uri =  "%s%s" % (gsHost, which)
    print("Fetching {0}".format(uri))
    res = session.get(uri)
    return json.loads(res.content)
        

def main(argv):

    parser = OptionParser()
    parser.add_option("-d", "--data", dest="dataDir", help="specify directory path for data")
    parser.add_option("-c", "--creds", dest="gsCredsFile", help="specify path to GSuite credentials file", metavar="FILE")
    parser.add_option("-r", "--report", dest="reportType", help="specify a report type to run, e.g. [login|admin|all]")
    opts, args = parser.parse_args(argv)
    
    gsCredsFile = opts.gsCredsFile

    dataDir = opts.dataDir or '/tmp'
    logFile = open(dataDir + "/log", "a")
    sys.stdout = logFile

    reportType = [opts.reportType]
    # Dunno why or works above and not here. 
    if reportType[0] == None:
        reportType = ["admin", "calendar", "drive", "login", "mobile", "token", "groups", "saml", "chat", "gplus", "rules"]
    
    creds = service_account.Credentials.from_service_account_file(gsCredsFile,
                                                                        scopes=['https://www.googleapis.com/auth/admin.reports.audit.readonly',
                                                                                'https://www.googleapis.com/auth/admin.reports.usage.readonly'])
    dcreds = creds.with_subject("yoursuperadminaccount@yourdomain.com")
    
    authdSession = AuthorizedSession(dcreds)

    for action in reportType:
        results = fetchStuff(authdSession, action)
        # this will go to the logfile
        print(results)
        
        #if "items" in results.keys():
            #saveLastRunTime(results['items'][0]['id']['time'], action)

        
    logFile.close()

            
if __name__ == "__main__":
    main(sys.argv)
