import datetime
import os
import requests
import sys
import time

# parse arguments

if len(sys.argv) is not 5:
    print "Error: Invalid command line arguments.\n"
    print "Usage: python umaurora.py COURSE_IDENTIFIER COURSE_CODE COURSE_CRN SESSID"
    print "   Ex: python umaurora.py MKT 2210 10009 abcde12345"
    sys.exit()

course_identifier = sys.argv[1]
course_code = sys.argv[2]
course_crn = sys.argv[3]
sessid = sys.argv[4]


# print welcome message and prepare script

print "======================================================"
print "|                                                    |"
print "|       UNIVERSITY OF MANITOBA AURORA CHECKER        |"
print "|                                                    |"
print "======================================================"
print "Testing {0} {1} CRN: {2}".format(course_identifier, course_code, course_crn)
print ""

wait_time = 60
interval = wait_time
last_check_time = None

space = 0


def check_space():

    # check the available space

    global space
    space = int(fetch_space_count())

    if space > 0:
        os.system("say \"space is available\"")
        print "SPACE IS AVAILABLE!!!!!!#!#!@!@!!!@!@!!!111"
    elif space == -9999:
        print "Error checking space.  Please make sure the CRN and course match up."

    # update the time

    global last_check_time
    last_check_time = datetime.datetime.now().strftime('%H:%M:%S')


def fetch_space_count():

    # run the request

    cookies = dict(SESSID=sessid)
    data = "term_in=201490&sel_subj=dummy&sel_subj={0}&SEL_CRSE={1}&SEL_TITLE=&BEGIN_HH=0&BEGIN_MI=0&BEGIN_AP=a&SEL_DAY=dummy&SEL_PTRM=dummy&END_HH=0&END_MI=0&END_AP=a&SEL_CAMP=dummy&SEL_SCHD=dummy&SEL_SESS=dummy&SEL_INSTR=dummy&SEL_INSTR=%25&SEL_ATTR=dummy&SEL_ATTR=%25&SEL_LEVL=dummy&SEL_LEVL=%25&SEL_INSM=dummy&sel_dunt_code=&sel_dunt_unit=&call_value_in=&rsts=dummy&crn=dummy&path=1&SUB_BTN=View+Sections".format(course_identifier, course_code)
    result = requests.post("https://aurora.umanitoba.ca/banprod/bwskfcls.P_GetCrse", cookies=cookies, data=data)

    # parse the response

    text = result.text

    # isolate the desired table

    array = text.split("Sections Found</CAPTION>")
    text = array[1]

    # split the table rows

    array = text.split("<TD COLSPAN=\"20\" CLASS=\"dddefault\"><hr></TD>")

    # iterate through the table rows

    for row in array:

        row = parse_aurora_row(row)
        if row:
            if row["crn"] == course_crn:
                return row["spaces"]

    return -9999


def parse_aurora_row(row):

    row = row.split("<TD CLASS=\"dddefault\">")

    if len(row) < 2:
        return None # invalid row

    # parse the CRN

    crn = parse_aurora_column(row[2])
    crn = crn.split("return true\">")
    crn = crn[1].split("</A>")
    crn = crn[0]

    # parse the spaces

    spaces = parse_aurora_column(row[13])

    # return the results

    result = dict(crn=crn, spaces=spaces)
    return result


def parse_aurora_column(col):

    col = col.split('</TD>')
    return col[0]


def print_status():

    sys.stdout.write("\r")
    sys.stdout.write("Available spaces: {0} | ".format(space))
    sys.stdout.write("Refreshed at {0} | ".format(last_check_time))

    sys.stdout.write("Refreshing in {0}".format((wait_time - interval)))

    sys.stdout.write("                 ") # extra input to clear multiple lines
    sys.stdout.flush()


while True:

    if interval == wait_time:
        check_space()
        interval = 0

    print_status()

    wait_interval = 1
    time.sleep(wait_interval)
    interval += wait_interval
