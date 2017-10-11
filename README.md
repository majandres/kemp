# kemp
Kemp Technologies RESTful API

contentRuleCleanUp.py - fetch all of the content rules that are NOT in use by any virtual service (aka VS or VIP).  It will then ask if you would like to delete them.

disable-restoreVS.py - passing the backup file as an argument will create a NEW backup with all the VS's disabled and will also ask you if you would like to restore the newly created backup to the LM. If no backup file is passed, then it will only disable the virtual services (not sub virtual services).

mstsToIP.py - tkinter GUI which takes an MSTS cookie and spit out the IP:port value.  The funtion msts_to_ip is doing all the work.

realServerFailure.py - automatically take a tcpdump of a real servrer after it fails a health check.  It's likely that if the RS fails one health check, it will fail again the second time it is checked....but now we have the tcpdump running. It's recommended that you fine tune your tcp options in order to only capture health check traffic.

removeVS.py - remove all virtual services that are in use by the LM.  removeVS in combination with contentRuleCleanup will clean up your LM.
