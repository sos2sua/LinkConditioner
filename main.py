import os
import sys
import numpy
import socket
from netfilterqueue import NetfilterQueue

ROUTE_TRAFFIC = "iptables -I OUTPUT -j NFQUEUE --queue-num 1;iptables -I INPUT -j NFQUEUE --queue-num 1"
ROUTE_TRAFFIC_IN_DEL = "iptables -D INPUT -j NFQUEUE --queue-num 1"
ROUTE_TRAFFIC_OUT_DEL = "iptables -D OUTPUT -j NFQUEUE --queue-num 1"
STATISTICS = "cat /proc/net/netfilter/nfnetlink_queue"
USAGE = "usage:\n main.py packetloss [jitter]\n  *packetloss in %\n  *jitter in ms"
choices = [True, False]
probs = [1, 0]

dropCount = 0
running = 0

def accept_or_not(pkt):
    global choices, probs, dropCount

    if numpy.random.choice(choices, p=probs):
        pkt.accept()
    else:
        dropCount += 1
        if dropCount == 400:
            print("")
            dropCount = 0
            runCMD(STATISTICS)
        if dropCount % 10 == 0:
            print("d")
        pkt.drop()


def readParameters():
    global USAGE
    if len(sys.argv) >= 2:
        if len(sys.argv) == 2:
            return float(sys.argv[1]), -1
        ploss = float(sys.argv[1])
        jbuff = float(sys.argv[2])
        if ploss < 1 or jbuff < 1:
            print(USAGE)
            exit(1)
        return ploss, jbuff
    else:
        print(USAGE)
        exit(1)


def runCMD(cmd, ignoreResponse=False):
    global running
    if running == 0:
        running = 1
        print("queue_number peer_portid queue_total copy_mode copy_range queue_dropped user_dropped id_sequence")
        cmd = "date >> output.txt;echo 'queue_number peer_portid queue_total copy_mode copy_range queue_dropped user_dropped id_sequence' >> output.txt; " + cmd

    if not ignoreResponse:
        cmd += " 2>> output.txt >> output.txt"
    else:
        cmd += " 2> /dev/null > /dev/null"
    a = os.system(cmd)
    if a != 0:
        if not ignoreResponse:
            print("Failed to execute System Command")
        return False
    return True


print("Initiating Link Conditioner")
p, j = readParameters()

probs = [1-p, p]

res = numpy.random.choice(choices, p=probs)

print("Starting LinkConditioner")
nfqueue = NetfilterQueue()
nfqueue.bind(1, accept_or_not)
s = socket.fromfd(nfqueue.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)

# Delete all old routes that may exist
while runCMD(ROUTE_TRAFFIC_IN_DEL, True):
    pass
while runCMD(ROUTE_TRAFFIC_OUT_DEL, True):
    pass
try:
    print("Routing Traffic through the LinkConditioner.")
    runCMD(ROUTE_TRAFFIC)
    nfqueue.run_socket(s)
except KeyboardInterrupt:
    print('')

print("Traffic Route Deleted.")

runCMD(ROUTE_TRAFFIC_IN_DEL)
runCMD(ROUTE_TRAFFIC_OUT_DEL)
s.close()
nfqueue.unbind()
print("LinkConditioner Stopped!")

