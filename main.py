import os
import sys


def readParameters():
    if len(sys.argv) == 3:
        # print ('Argument List:', str(sys.argv[1:]))
        return sys.argv[1],sys.argv[2]
    else:
        print("usage:\n main.py packetloss jitter\n  *packetloss in %\n  *jitter in ms")
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
print(p, j, runCMD('ls'))

print("Starting Link Conditioner")

