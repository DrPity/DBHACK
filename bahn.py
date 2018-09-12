import psutil
import time
import math
import subprocess
import sys

newMac = False
sessionTraffic = 0

def checkTraffic(size_bytes):
   if size_bytes == 0:
       return "0B"
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 0) % 200
   return s

oldTrafficVolume = checkTraffic(psutil.net_io_counters(pernic=True)['en0'].bytes_recv)

while True:
    net = psutil.net_io_counters(pernic=True)
    trafficVolume = float(checkTraffic(net['en0'].bytes_recv))

    if trafficVolume != oldTrafficVolume:
        sessionTraffic = abs(trafficVolume - oldTrafficVolume)

    if sessionTraffic <= 1.0 and not newMac:
        print "traffic Volume reached"
        try:
            subprocess.check_call(['spoof-mac', 'randomize', 'Wi-Fi'])
            subprocess.check_call(['networksetup', '-setairportpower', 'en0', 'off'])
            subprocess.check_call(['networksetup', '-setairportpower', 'en0', 'on'])
            newMac = True
        except:
            print "[Installation Error] "
            sys.exit(0)
    elif sessionTraffic > 1.0 and newMac:
        newMac = False  
        print "Reset"
    else: 
        print sessionTraffic
    time.sleep(1)


