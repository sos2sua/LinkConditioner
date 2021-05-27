# LinkConditioner 
# Note only works with python 2.7 - 3.6 !

Allow developers to introduce packet loss in linux network based on the NFQUEUE.


"To understand NFQUEUE, the easiest way is to understand the architecture inside Linux kernel. When a packet reach an NFQUEUE target it is en-queued to the queue corresponding to the number given by the --queue-num option. The packet queue is a implemented as a chained list with element being the packet and metadata (a Linux kernel skb):

1. It is a fixed length queue implemented as a linked-list of packets.
2. Storing packet which are indexed by an integer
3. A packet is released when userspace issue a verdict to the corresponding index integer
4. When queue is full, no packet can be enqueued to it

This has some implication on userspace side:

1. Userspace can read multiple packets and wait for giving a verdict. If the queue is not full there is no impact of this behavior.
2. Packets can be verdict without order. Userspace can read packet 1,2,3,4 and verdict at 4,2,3,1 in that order.
3. Too slow verdict will result in a full queue. Kernel will then drop incoming packets instead of en-queuing them." ref(https://home.regit.org/netfilter-en/using-nfqueue-and-libnetfilter_queue/)

#Dependencies (ref:https://pypi.org/project/NetfilterQueue/)
1. pip intall numpy
2. apt-get install build-essential python-dev libnetfilter-queue-dev
3. netfilterqueue:

   pip install NetfilterQueue
   
    -if the above fails try
 
   pip install -U git+https://github.com/kti/python-netfilterqueue
   (https://stackoverflow.com/questions/61301351/how-do-i-install-netfilterqueue-for-python3)

If installing for Python3 not set as default
1. pip3 install numpy
2. sudo apt-get install build-essential python-dev libnetfilter-queue-dev
3. pip3 install NetfilterQueue

4. sudo python3 main.py 0.1
