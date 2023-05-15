#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time
from datetime import datetime

def usage():
    print("[*] Usage:")
    print ("\tpython3 %s vendor brand IP" % sys.argv[0])
    print("[*] Example:")
    print ("\tpython3 %s D-Link DIR816L 192.168.1.1" % sys.argv[0])

def scope():
    binfile = ""
    suffixes = [".bin", ".chk", ".trx", ".img", ".pck", ".web"]
    vendor = sys.argv[1]
    brand = sys.argv[2]
    IP = sys.argv[3]
    for suffix in suffixes:
        if (os.path.exists(brand + suffix)):
            binfile = brand + suffix
            break
    if binfile == "":
        print ("[!] No Such <%s> BIN Files" % (brand))
        return 1
    if not os.path.exists(vendor):
        print ("[!] vendor <%s> paths is not exist" % vendor)
        return 1
    #Step 1: Emulating
    os.system("python3 enumerating.py %s %s" % (vendor,brand))
    #Step 2: Delivering
    os.system("python3 delivering.py %s %s %s" % (vendor, brand, IP))
    #Step 3: Identifying Unprotected
    os.system("echo root | sudo -S python3 identifyingUnprotected.py %s %s" % (vendor, brand))
    #Step 4: Setting Database
    os.system("echo root | sudo -S python3 dbAssistant.py %s %s %s" % (vendor, brand, IP))
    #Step 5: Identifying Hidden
    os.system("echo root | sudo -S python3 identifyingHidden.py %s %s %s" % (vendor, brand, IP))

if __name__ == "__main__":
    if (len(sys.argv) != 4):
        usage()
    else:
        StartTime = datetime.now()
        print ("[*] Start Time =", StartTime)
        scope()
        EndTime = datetime.now()
        print ("[*] End Time =", EndTime)
        print ("[*] Time =", (EndTime - StartTime))
        print ("[*] Seconds =", (EndTime - StartTime).seconds)
