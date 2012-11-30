#Importing required libraries
import logging
import datetime
import sys
import requests
import ast
import string

# Checking that all the arguments were entered on the command line, exiting with a message if not.
if len(sys.argv) != 6:
    argumentsnotset = 'One or more arguments were not passed. \nUsage is like so: \nPython MustardCruftReport.py DOCO-SITE-URL USERNAME PASSWORD MICROTEXT-GITHUB-URL NINEFOLD-SERVER-ID'
    print argumentsnotset
    sys.exit(1)	

# Setting command line arguments URL, username and password.
siteURL = sys.argv[1]
siteUserName = sys.argv[2]
sitePassWord = sys.argv[3]
githubPage = sys.argv[4] #deprecated
server_id = sys.argv[5]

# Overriding location of context-help file in Github and Ninefold server id
githubPage = "https://api.github.com/repos/TheRealEdDawson/testable-microtext/contents/Testable-Microtext.txt"
server_id = "020bcc5f-2a2b-417d-a6bc-44c61bcc0e78"

# Setting up logging format to set log file AND HTML report filename, time stamping ON
logfilename = "MustardCruftLogFile.log"
logging.basicConfig(filename=logfilename,filemode='w',level=logging.INFO,format='%(asctime)s %(message)s')
htmlreportname = "Mustard_Cruft_Report.html"
print " "
print "Scanning begins."
print " "

# Setting up HTML report header and footer
# HTML header content:
header = """
<html>
<head><title>Mustard Cruft Report</title></head>
<body>
<h1>Mustard Cruft Report</h1>
<i>Compiled on: """

# Setting up timestamp for HTML report
datestamp = datetime.date.today().strftime("%A %d. %B %Y")
timestamp = datetime.datetime.now().strftime("%I:%M%p")

# Writing HTML header to file:
with open(htmlreportname, 'w') as f:
    #f.write(header)
    f.write(datestamp)
    f.write(", at ")
    f.write(timestamp)
    f.write(""" UTC</i>""")

# HTML footer content:
footer = """<br><br><b>Ending Mustard Cruft testing. 
<br><br>Thanks for using the Mustard Cruft Report!</b></body></html>"""

# List of general varables in use
# e is a variable that catches HTTP error codes that come back
response = "A string to catch the HTML data from the URL location"
html = "."
sessionduration = 0
linktesttotal = 0
errorcount = 0
siteText = "blank"

# presetting some doco variables
docolist = ""
doco_record= []
testCounter = 0

# Site Login: establishing session keys and values
session = requests.session(config={'verbose': sys.stderr})
#This is the form data that the page sends when logging in
login_data = {
'session[username]': siteUserName,
'session[password]': sitePassWord,
'commit': 'Login',
'utf8': True,
}

# Authenticate the user on the site and actually login, creating a session
r = session.post(siteURL + '/sessions', data=login_data)
print r.status_code
logging.info(r.status_code)
#logging.info(r.headers)
#print r.encoding
#logging.info(r.encoding)
#logging.info(r.text)
#logging.info(r.json)

def siteGet(securePage):
    # Try accessing a page that requires you to be logged in
    accessloggystring = "\n\n\n*** NEXT CASE *** #" + str(testCounter) + "\n\nAttempting to access secure page:\n" + securePage + "\n"
    print accessloggystring
    logging.info(accessloggystring) 
    r = session.get(securePage) # Actually access the page
    siteText = r.text
    return (siteText)
    print r.status_code

# Opening the HTML report file
with open(htmlreportname, 'a') as f:
    f.write("<br><i>Scanning URL:<b> ")
    f.write(siteURL)
    f.write("</b> and source file:<b> ")
    f.write(githubPage)
    f.write("</b></i><br>")

# Accessing Github to retrieve microcopy content, and decode from base64 
r = session.get(githubPage) # Get the context-help file information from Github
print r.status_code #Show whether your request to Github worked
githubDict = ast.literal_eval(r.text) # Pull the Github string into a dictionary
stringy = githubDict['content']; # pull out just the file contents from what Github returns

# Processing Microcopy to retrieve lines of content
doco_data = stringy.decode('base64','strict') #decode the file contents from base64 & put into string
for line in doco_data.split('\n'):
    doco_line = line
    doco_record = doco_line.rsplit(' | ') # Split out triple value pairs into list attributes
    doco_test_URL = doco_record[0]
    doco_copycopter = doco_record[1]
    doco_microcopy = doco_record[2]
    # Checking if the page URL contains "SERVERNAME" and replacing it with server_id if so
    if "SERVERNAME" in doco_test_URL:
        tempURL = doco_test_URL.replace("SERVERNAME", server_id)
        #print "This is the assembled URL for SERVERNAME: ", tempURL
        doco_test_URL = tempURL
        #sys.exit(1)
    # Here, we want to assemble a URL from the base URL, appending the doco_test_URL
    securePage = siteURL + doco_test_URL
    siteText2 = siteGet(securePage) # Call the function to retrieve a new page's source
    testCounter += 1
    # Check if the microcopy text is found inside the tested site copy and return
    precheckloggystring = "\nChecking for occurrence of: " + doco_microcopy + "\n\nCopycopter Code: " + doco_copycopter
    print precheckloggystring
    logging.info(precheckloggystring)
    checkResult = doco_microcopy in siteText2
    if checkResult == False: errorcount += 1
    checkloggystring = "\nCheck result was: " + str(checkResult) #bunch of logging
    print checkloggystring
    logging.info(checkloggystring)
    docolist += "</p><br/><br/><p>Doco Test URL: "
    docolist += str(doco_test_URL)
    docolist += "</p><p>CopyCopter Code: "
    docolist += str(doco_copycopter)
    docolist += "</p><p>Microcopy Content: "
    docolist += str(doco_microcopy)
    docolist += str(checkloggystring)

# This sends summary information to the console and seals off entries in the log file.
print " "
print "Ending Mustard Cruft testing. Thanks for using the Mustard Cruft Report!\n"
scansummary = testCounter, "case(s) were tested.", errorcount, "error(s) were found."
print scansummary
print "Mustard Cruft was recorded in the HTML report:", htmlreportname
print "And in the logfile:", logfilename
summarytotal = str(testCounter) + " case(s) were tested. " + str(errorcount) + " error(s) were found."
logging.info(summarytotal)

with open(htmlreportname, 'a') as f:
    f.write(docolist)
    f.write("<br/><br/>")
    f.write(summarytotal)
    f.write("<br><i>If there's no links above, then no errors were found! See the .log file for a detailed record of the scan.</i>")
    f.write(footer)
    f.close()
