from os.path import exists
import sys
from sys import argv
import requests
import re
from getpass import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

vs_data = []
vs_index = []
subvs_index = []
login_tries = 3

########################################################################################################################
#check if we can connect successfully & if the API is enabled

try:
    lmip = 'https://' + raw_input("LM IP: ")
except KeyboardInterrupt:
    sys.exit(1)

while login_tries != 0:
    try:
        un = raw_input("Username: ")
        pwd = getpass()

        status = requests.get(lmip+"/access/get?param=version", verify=False, auth=(un,pwd)).status_code
        if status == 200:
            break
        elif status == 401:
            print "Invalid Username or Password"
            login_tries -= 1
            if login_tries == 0:
                print "https://kemptechnologies.com/faq/faq-52-i-cannot-remember-password-my-bal-user-there-way-reset-password/"
                sys.exit(1)
            continue
        elif status == 404:
            print "API Interface NOT enabled... or it's not a LoadMaster"
            sys.exit(1)
    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        print "error: Unable to Connect"
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)

########################################################################################################################
#backup file to disable the VS's on

try:
    lmbackup = argv[1]
    if not exists(lmbackup):
        print "Oops, the backup file does not exists!"
        sys.exit(1)

    data = open(lmbackup, 'rb').read() #open file as binary
    res = requests.post(url=lmip+'/access/restore?type=2', data=data, verify=False, auth=(un, pwd))

    if res.status_code > 399:
        print re.search('<error>(.*)<', res.content, re.IGNORECASE).group(1)
        sys.exit(1)
    elif res.status_code == 200:
        print 'Bakckup successfully restored'

except IndexError:  #no argument is given....user only wants to disable the VS's
    #print "Oops, missing the backup file path/name!"
    pass

########################################################################################################################
#grab VS information and disaalbe them.

content = requests.get(lmip+'/access/listvs', verify=False, auth=(un, pwd)).content

for i in content.split('</VS>'):
    vs_data.append(i)

for i in xrange(re.findall("</vs>", content, flags=re.IGNORECASE).__len__()):  #total number of VS's
    if re.search("<vsaddress>(.*)<", vs_data[i], re.IGNORECASE):  #if there is a VS IP, then it's NOT a sub-vs
        vs_index.append(re.search("<index>(.*)<", vs_data[i], re.IGNORECASE).group(1))
    else:
        subvs_index.append(re.search("<index>(.*)<", vs_data[i], re.IGNORECASE).group(1))

for i in vs_index:  #disable all VS's (not sub-vs's)
    result = requests.get(lmip+'/access/modvs?vs=' + i + '&enable=n', verify=False, auth=(un, pwd))
    if result.status_code == 200:
        print "\tDisabled VS Index: " + i
    else:
        try:
            print re.search('<(error|title)>(.*)<', result.content, re.IGNORECASE).group(2)
        except AttributeError:
            print "Oops, something went wrong..."