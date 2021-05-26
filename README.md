# LinkConditioner 
# Note only works with python 2.7 - 3.6 !

Allow developers to introduce packet loss in linux network.

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
