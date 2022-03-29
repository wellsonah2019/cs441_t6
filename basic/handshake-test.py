#!/usr/local/bin/python
from scapy.all import *

# VARIABLES
# src = sys.argv[1]
# dst = sys.argv[2]
sport = random.randint(1024,65535)
# dport = int(sys.argv[3])

# SYN
ip=IP(src="0x1A",dst="0x2A")
SYN=TCP(sport=sport,dport=8011,flags='S',seq=1000)
SYNACK=sr1(ip/SYN)

# ACK
ACK=TCP(sport=sport, dport=8011, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
send(ip/ACK)