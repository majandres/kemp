import sys
import requests
import re
from getpass import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

rule_list = []
rules_active = []
remove_these_rules = []
login_tries = 3

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


######################################################################################################
#grab all of the content rules

for i in requests.get(lmip+'/access/showrule', verify=False, auth=(un, pwd)).content.split('\n'):
    try:
        rule_list.append(re.search("<name>(.*)<", i, re.IGNORECASE).group(1))  #put rule_name in a list
    except AttributeError: #if no match is found
        continue

######################################################################################################
#grab all of the rules that are actually in use

for i in requests.get(lmip+'/access/listvs', verify=False, auth=(un, pwd)).content.split('\n'):
    try:
        rule = re.search("<name>(.*)<", i, re.IGNORECASE).group(1)  #all of the rules that are active....beware, sub-vs are also under <Name> !
        #check if it's actually a rule!
        if rule in rule_list:
            if rule not in rules_active:  #check for duplicates...some rules are in more than one place!
                rules_active.append(rule)
        else:
            continue
    except AttributeError:  #if no match is found
        continue

print "\ntotal rules: ", rule_list.__len__()
print "rules in use: ", rules_active.__len__()

######################################################################################################
#compare rule_list[] to rules_active[]
#check if rule_list[0] exists in rules_active[]...if not, add rule to a new list of rules to be removed from the system.

for val in rule_list:
    if val in rules_active:
        continue
    else:
        remove_these_rules.append(val)

######################################################################################################
#remove the rules that were found not to be "active"

print "rules to delete: ", remove_these_rules.__len__()

for i in remove_these_rules:
    print "\t", i

#ask the user if they woul like to delete the previously listed rules
while True:
    try:
        answer = raw_input('\nContinue to delete [Y/N]: ').lower()
        if answer == 'y':
            for i in remove_these_rules:
                if str(requests.get(lmip+'/access/delrule?name='+i, verify=False, auth=(un, pwd)).status_code) == '200':
                    print "Deleted rule: ", i
                else:
                    print "Oops, something went wrong!"
            break
        elif answer == 'n':
            sys.exit(1)
    except KeyboardInterrupt:
        print '\n'
        sys.exit(1)