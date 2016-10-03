# kemp
Kemp Technologies RESTful API

contentRuleCleanUp.py - fetch all of the content rules that are NOT in use by any virtual service (aka VS or VIP).  It will then ask if you would like to delete them.

disable-restoreVS.py - passing the backup file as an argument will restore only the VS's and disable all virtual services (not sub virtual services).  If no backup file is passed, then it will only disable the virtual services (not sub virtual services)
