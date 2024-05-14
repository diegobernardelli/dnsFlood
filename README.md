This script has been created to perform stress tests on DNS servers or DNS inspection devices.
The script takes a file list of domain names (check domainlist.txt for the format) loops the requests to the target DNS server

    USAGE:

    ./dnsFlood.py [domain list file] <arg1, arg2, ...>

    ARGUMENTS:

     -h | --help        print help
    -hl | --high-load   enable high load mode -> in this mode only the first 8 domains are looped at cpu speed with 8 threads
    -sm | --src-mac     set source mac address -> fromat 00:00:00:00:00:00
    -dm | --dst-mac     set destination mac address -> fromat 00:00:00:00:00:00
    -si | --src-ip      set source ip addess
    -di | --dst-ip      set destination ip address
