import os
import shutil
import tarfile
from os.path import exists
import sys
from sys import argv
import requests
import re
from getpass import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# check if we can connect successfully & if the API is enabled
def lm_connect():
    login_tries = 3
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
    return lmip, un, pwd


# create backup file with all VS's disabled
def disable_all_vs_config(backup):
    try:
        lmbackup = backup
        if not exists(lmbackup):
            print "Oops, the backup file does not exists!"
            sys.exit(1)

        tar = tarfile.open(lmbackup)
        tar.extractall()  # extract all to the current directory
        config_files = tar.getnames()  # store backup file names in list
        tar.close()

        # modify the config file to DISABLE all of the VS's
        bahd = open("bahd.conf", "r")
        data = bahd.readlines()
        bahd.close()
        bahd = open("bahd.conf", 'w')

        for s in data:
            bahd.write(s.replace("ENABLE:1", "ENABLE:0"))
        bahd.close()

        # targz everything back up ready to upload to the LM
        tar2 = tarfile.open(lmbackup + "_DISABLED", "w:gz")
        for name in config_files:
            tar2.add(name)
        tar2.close()

        # remove all the files that were extracted
        for i in config_files:
            if exists(i):
                if os.path.isdir(i):
                    shutil.rmtree(i)
                elif os.path.isfile(i):
                    os.remove(i)
        shutil.rmtree('tmp')
        shutil.rmtree('waf')
    except tarfile.ReadError:
        print "Oops, failed to read that file...sure it's a LM Backup?"
        sys.exit(1)


# grab VS information and disable via API
def disable_all_vs_api(lmip, un, pwd):
    vs_data = []
    vs_index = []
    subvs_index = []

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


# upload backup to the LM
def restore_backup(backup, lmip, un, pwd):
    data = open(backup, 'rb').read() #open file as binary
    res = requests.post(url=lmip+'/access/restore?type=2', data=data, verify=False, auth=(un, pwd))

    if res.status_code > 399:
        print re.search('<error>(.*)<', res.content, re.IGNORECASE).group(1)
        sys.exit(1)
    elif res.status_code == 200:
        print 'Bakckup successfully restored'


# ask user if they want to disable AND restore the backup
try:
    argv[1]
    try:
        answer = raw_input("Disable VS's and restore backup? [Y/N]: ")
    except KeyboardInterrupt:
        sys.exit(1)
    while answer not in ['Y', 'N', 'y', 'n']:
        try:
            answer = raw_input("Disable VS's and restore backup? [Y/N]: ")
        except KeyboardInterrupt:
            sys.exit(1)
    if answer in ['Y', 'y']:
        disable_all_vs_config(argv[1])
        lmip, un, pwd = lm_connect()
        restore_backup(argv[1], lmip, un, pwd)
    else:
        disable_all_vs_config(argv[1])

# user only wants to disable VS's on the LM.
except IndexError:
    lmip, un, pwd = lm_connect()
    disable_all_vs_api(lmip, un, pwd)
