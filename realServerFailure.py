import socket
import re
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# this will only work with LM version 7.1.35 and above.
# before running this, take a sample capture to see what kind of traffic to expect....
# note that, if you have SOR, server side traffic will used the source IP of the interface...
# health checks use the interface IP when checking RS's....also, HA. (if you don't understand, then don't use this)
# also, don't forget to set the Syslog IP on the LM to point towards the host that is running this script.

# used for API access (management IP address)
lmip = "https://10.10.10.11"
un = "bal"
pw = "1fourall"

# IP address of the failing RS. Don't care about the port.
RSAddress = "10.10.10.100"

# interface that the RS is located on...take note of non-local RS's and the LM's DG.
interface = "eth0"

# only capture traffic between the local interface and the RS. (health check traffic) beware of SOR and HA.
tcpOptions = "host 10.10.10.11 and 10.10.10.100"  # host 10.10.10.11 and 10.10.10.100 or host 10.10.10.12 and 10.10.10.100

# stop TCP dump after this many seconds
maxTime = "30"

tcpdumpURL = lmip + "/access/tcpdump?maxpackets=200000&maxtime=" + maxTime + "&interface=" + interface + "&tcpoptions=" + tcpOptions


fileCount=1
# http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def download_file(url, reason):
    global fileCount
    local_filename = str(fileCount) + " RSFail - " + RSAddress + " - " + reason + ".pcap"
    r = requests.get(url, auth=(un, pw), verify=False) # <----- Money Maker!
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    fileCount += 1
    return local_filename

# https://wiki.python.org/moin/UdpCommunication
UDP_IP = "0.0.0.0"
UDP_PORT = 514
sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

print "%s %d" % ("I'm listening now on UDP port", UDP_PORT)

# this is basically acting as a Syslog server looking for the RS to fail.....when it does, tcpdump is run on the LM.
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "%s - Connected by %s - %s" % (time.strftime("%c"), addr, data)
    #"<11>l4d: Removing RS 10.10.10.100:80 from VS 10.10.10.62:443(IIS Secured) - Timeout waiting for data"
    if re.search("Removing RS "+RSAddress, data):
        reason = re.search("Removing RS.* - (.*)", data).groups()
        print "%s - !!!!!!!!!!!!!!!!!Staring tcpDump!!!!!!!!!!!!!!!!!" % (time.strftime("%c"))
        download_file(tcpdumpURL, reason[0])  #start TCP dump
