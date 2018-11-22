# kemp
Kemp Technologies RESTful API

ruleCleanUp.py - fetch all of the content rules that are NOT in use by any virtual service (aka VS or VIP).  It will then ask if you would like to delete them.

mstsToIP.py - tkinter GUI which takes an MSTS cookie and spit out the IP:port value.  The function msts_to_ip is doing all the work.

realServerFailure.py - automatically take a tcpdump of a real servrer after it fails a health check.  It's likely that if the RS fails one health check, it will fail again the second time it is checked....but now we have the tcpdump running. It's recommended that you fine tune your tcp options in order to only capture health check traffic.

removeVS.py - remove all virtual services that are in use by the LM.  removeVS in combination with ruleCleanup will clean up your LM.
