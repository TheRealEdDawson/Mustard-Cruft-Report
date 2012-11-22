#Importing required libraries
import urllib2
import logging
import re
import datetime
import sys

# Checking that all the arguments were entered on the command line, exiting with a message if not.
if len(sys.argv) != 5:
    argumentsnotset = 'One or more arguments were not passed. \nUsage is like so: \nPython MustardCruftReport.py DOCO-SITE-URL USERNAME PASSWORD MICROTEXT-FILE-PATH'
    print argumentsnotset
    sys.exit(1)	

# Setting command line arguments URL, username and password.
server = sys.argv[1]
site_user = sys.argv[2]
site_pwd = sys.argv[3]
doco_file = sys.argv[4]

# Functions for printing results into the console
def introprint():
    print " "
    print "Scanning begins."
    print " "

def tickprint():
    print "\n Passed test."

def crossprint():
    print "\n Failed test."

# Setting up logging format to set log file AND HTML report filename, time stamping ON
logfilename = "MustardCruftLogFile.log"
logging.basicConfig(filename=logfilename,filemode='w',level=logging.INFO,format='%(asctime)s %(message)s')
htmlreportname = "Mustard_Cruft_Report.html"
introprint() #prints introduction text in ASCII art square

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
    f.write(header)
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

# Setting up the regex strings that will be scanned on each page. 
# These are specific text strings found in Confluence errors, that show up in the source of the page. 
Mustardloginregex = re.compile("<title>Log In")
Mustardlinkregex = re.compile("error\">&#91;")
createlinkregex = re.compile("createlink")
Mustardimageregex = re.compile("Unable to render embedded object")
Mustardmacroregex = re.compile("Unknown macro")
Mustardmacroregex2 = re.compile("Error rendering macro")
Mustardjiraissuesregex = re.compile("error\">jiraissues\:")
Mustardincluderegex = re.compile("The page.*does not exist")
Mustardincluderegex2 = re.compile("The included page could not be found.")

#tuplelist = [(Mustardloginregex,' failed login.',' a login error was returned.'), (Mustardlinkregex,' broken links.',' a broken internal link was found.'), (createlinkregex,' red create links.',' a red create link was found.'), (Mustardimageregex,' broken graphics.',' a broken graphic was found.'), (Mustardmacroregex,' uninstalled macros.',' an uninstalled macro reference was found.'), (Mustardmacroregex2,' general macro errors.',' a general macro error was found.'), (Mustardjiraissuesregex,' JIRA Issues Macro errors.',' a JIRA Issues Macro error was found.'), (Mustardincluderegex,' Mustard excerpt-includes.',' an excerpt-include is Mustard or hidden from the logged-in user.'), (Mustardincluderegex2,' Mustard page includes.',' an included page is Mustard or hidden from the logged-in user.')]

docolist = []
doco_record= []

with open(htmlreportname, 'a') as f:
    f.write("<br><i>Scanning URL:<b> ")
    f.write(server)
    f.write("</b> and SPACE:<b> ")
    f.write(doco_file)
    f.write("</b></i><br>")
    f.write("<br><b>The following Cruft is Mustard.</b> ;-)<br>")

# Processing text file to retrieve api key
doco_data = open(doco_file)
for line in doco_data:
    doco_line = line.rstrip() # Take one line from the file
    doco_record = doco_line.rsplit(' | ') # Split out triple value pairs into list attributes
    print "This is the contents of doco_record: ", doco_record
    #sys.exit(1) #temporary breakpoint
    doco_test_URL = doco_record[0]
    doco_copycopter = doco_record[1]
    doco_microcopy = doco_record[2]
    testloggystring = "This is a line: " + doco_line # Set up logging values
    print testloggystring
    logging.info(testloggystring)
    docolist += doco_line # Write the lines back a list (for debugging check)
    docolist += "Doco Test URL: "
    docolist += doco_test_URL
    docolist += "CopyCopter Code: "
    docolist += doco_copycopter
    docolist += "Microcopy Content: "
    docolist += doco_microcopy
doco_data.close()

#print docolist

"""
def downloadpage(site_address):
    # Conditional block that tries to access the URL and catches HTTP Error codes sent back.
    try: 
        response = urllib2.urlopen(site_address)
        html = response.read()
    #BEGIN HTTP error finder block
    except urllib2.HTTPError, e:
    # e.code is just the numerical HTTP error code from the server. i.e. 404
        print "Error", e.code, "was detected."
	crossprint()
	with open(htmlreportname, 'a') as f:
	    f.write('For page:')
	    f.write('<a href=\"')
	    f.write(site_address)
	    f.write('\" </a>')
            f.write("Error", e.code, "was detected.")
        errorcode = e.code
        errorloggystring = 'Error', errorcode, 'from', 
        logging.info(errorloggystring)
        errorcount = errorcount + 1
    # e.read is the HTML source of the 404 page. Line below prints that to console.
        print e.read() 
    #END HTTP error finder block
    return html

def regexfunction(html, coolregex, testname, errormessage, site_address):
    # Search for Mustard Cruft (error codes in page sources)
    print "Testing for%s" %testname
    errormatch = coolregex.search(html)
    if errormatch: # This shows a list of the characters that matched.
        print 'Error found: ', errormatch.group()
        errorloggystring = 'Error: ', errormatch.group(), 'found.'
        logging.info(errorloggystring)
	with open(htmlreportname, 'a') as f:
	    f.write("<br>For page: ") 
	    f.write("<a href=\"")
	    f.write(site_address)
	    f.write('\">')
	    f.write(site_address)
	    f.write('</a>')
            f.write('%s' %errormessage)
	crossprint()
	return False
    else:
        errorloggystring = 'Passed.'
	print errorloggystring
        logging.info(errorloggystring)
	tickprint()
	return True

# MAIN PROGRAM LOOP

# Loop to print every url in the spaceindex
for page_summary in spaceindex:
    site_address = page_summary['url']
    #Putting in an initial log entry to show that we're trying the given URL.
    initloggystring = "Accessing", site_address
    logging.info(initloggystring)
    print "Accessing", site_address
    linktesttotal += 1
    html = downloadpage(site_address)
    for coolregex, testname, errormessage in tuplelist:
        if not regexfunction(html, coolregex, testname, errormessage, site_address):
		errorcount += 1
    # WINDUP FUNCTION 
    # This records the outcome of the ping to the log, if it seemed successful.
    if html == ".": winduploggystring = "Page content was not retrieved for", site_address
    if html != ".": winduploggystring = "Actions completed on", site_address  
    logging.info(winduploggystring)
    print "Actions completed on", site_address
    html = "."

# (endFOR MAIN PROGRAM)

"""

# This sends summary information to the console and seals off entries in the log file.

print " "
print "Ending Mustard Cruft testing. Thanks for using the Mustard Cruft Report!\n"
scansummary = linktesttotal, "link(s) were tested.", errorcount, "error(s) were found."
print scansummary
print "Mustard Cruft was recorded in the HTML report:", htmlreportname
print "And in the logfile:", logfilename
summarytotal = (linktesttotal, "link(s) were tested.", errorcount, "error(s) were found.")

with open(htmlreportname, 'a') as f:
    docostring = ""
    for d in docolist:
        docostring += d
    f.write(docostring)
    f.write("<br><i>If there's no links above, then no errors were found! See the .log file for a detailed record of the scan.</i>")
    f.write(footer)
