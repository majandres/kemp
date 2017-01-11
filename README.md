# kemp
Kemp Technologies RESTful API

contentRuleCleanUp.py - fetch all of the content rules that are NOT in use by any virtual service (aka VS or VIP).  It will then ask if you would like to delete them.

disable-restoreVS.py - passing the backup file as an argument will create a NEW backup with all the VS's disabled and will also ask you if you would like to restore the newly created backup to the LM. If no backup file is passed, then it will only disable the virtual services (not sub virtual services).

mstsToIP.py - tkinter GUI which takes an MSTS cookie and spit out the IP:port value.  The funtion msts_to_ip is doing all the work.
