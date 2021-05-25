import os
import sys
import numpy
import socket
from netfilterqueue import NetfilterQueue

ROUTE_TRAFFIC = "iptables -A INPUT -j NFQUEUE --queue-num 0"
ROUTE_TRAFFIC_DEL = "iptables -D INPUT -j NFQUEUE --queue-num 0"
choices = [True, False]
probs = [1, 0]


def accept_or_not(pkt):
    global choices, probs

    if numpy.random.choice(choices, p=probs):
        pkt.accept()
    else:
        # print("Packet dropped.")
        pkt.drop()


def readParameters():
    if len(sys.argv) >= 2:
        if len(sys.argv) == 2:
            return float(sys.argv[1]), -1
        return float(sys.argv[1]), float(sys.argv[2])
    else:
        print("usage:\n main.py packetloss [jitter]\n  *packetloss in %\n  *jitter in ms")
        exit(1)


def runCMD(cmd):
    cmd = "date >> output.txt; " + cmd
    cmd += " >> output.txt"
    a = os.system(cmd)
    if a != 0:
        print("Failed to execute System Command")
        return False
    return True


print("Initiating Link Conditioner")
p, j = readParameters()

probs = [1-p, p]

res = numpy.random.choice(choices, p=probs)

print("Starting LinkConditioner")
nfqueue = NetfilterQueue()
nfqueue.bind(0, accept_or_not)
s = socket.fromfd(nfqueue.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)
try:
    print("Routing Traffic through the LinkConditioner.")
    runCMD(ROUTE_TRAFFIC)
    nfqueue.run_socket(s)
except KeyboardInterrupt:
    print('')

print("Traffic Route Deleted.")
runCMD(ROUTE_TRAFFIC_DEL)
s.close()
nfqueue.unbind()
print("LinkConditioner Stopped!")

