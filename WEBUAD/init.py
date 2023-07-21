#!/usr/bin/env python
# coding=utf-8

import os
import sys

global vendor, brand, binfile
binfile = ""

def usage():
    print("[*] Function:")
    print("\tUsing binwalk to extract vendor-brand bin files.\n\t[Optional] Using FirmAE to emulate bin files.")
    print("[*] Usage 1:")
    print ("\tpython3 %s vendor brand" % sys.argv[0])
    print("[*] Example 1:")
    print ("\tpython3 %s TPLink 850" % sys.argv[0])
    print("[*] Usage 2:")
    print ("\tpython3 %s vendor brand E" % sys.argv[0])
    print("[*] Example 2:")
    print ("\tpython3 %s TPLink 850 E" % sys.argv[0])

def init():
    #IoTScope Ready
    global vendor, brand, binfile
    suffixes = [".bin", ".chk", ".trx", ".img", ".pck", ".web", ".fmw"]
    vendor = sys.argv[1]
    brand = sys.argv[2]
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
    #os.system("cp %s %s/" % (binfile, vendor))
    os.system("binwalk -Me %s" % (binfile))
    os.system("mkdir %s/%s" % (vendor, brand))
    #maybe not squashfs-root dir
    #search "-root" dir
    p = "_%s.extracted" % (binfile)
    print (p)
    cnt = 0
    if (os.path.exists(p)):
        for root, dirs, files in os.walk(p):
            #print (root, dirs)
            if ("-root" in root and root[-5:] == "-root"):
                os.system("cp -R %s/* %s/%s" % (root, vendor, brand))
                os.system("mkdir %s/%s/firmware" % (vendor, brand))
                os.system("cp -R %s/* %s/%s/firmware" % (root, vendor, brand))
                cnt += 1
    os.system("rm -rf _%s.extracted/" % (binfile))
    if (cnt >= 1):
        print ("[+] Extracting Bin files Succeeds ... \n[+] DIR: %s/%s" % (vendor, brand))
        #FirmAE copy files
        os.system("cp %s /home/iot/tools/FirmAE/firmwares/" % (binfile))
        return 0
    else:
        print ("[!] Extracting Bin files Fails ... Can not find root directory.")
        return 1

def Emulating():
    global vendor, brand, binfile
    #Step 2: FirmAE Emulating
    os.chdir("/home/iot/tools/FirmAE/")
    os.system("echo iot | sudo -S ./run.sh -r %s ./firmwares/%s" % (brand, binfile))

if __name__ == "__main__":
    if (len(sys.argv) == 3):
        init()
    elif (len(sys.argv) == 4 and sys.argv[3] == "E"):
        ret = init()
        if (ret == 0):
            Emulating()
    else:
        usage()
