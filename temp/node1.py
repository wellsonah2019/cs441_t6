import socket
# from threading import Timer
import time
from datetime import datetime

IP = '0x1A'
MAC = 'N1'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


LOCAL_ARP_TABLE = {
    "0x11": "R1",
    "0x1A": "N1"
}
def send_local(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8001))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8101))

def send_ping(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8001))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8101))

def send_out(packet):
    pass

def wrap_packet_ip(message, dest_ip):
    ethernet_header = ""
    IP_header = ""
    source_ip = IP
    IP_header = IP_header + source_ip + dest_ip
    source_mac = MAC
    
    if dest_ip in LOCAL_ARP_TABLE:
        destination_mac = LOCAL_ARP_TABLE[dest_ip] 
    else:
        destination_mac = 'R1'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + message
    
    return packet

def wrap_ping_packet(message, dest_ip, start_time):
    ethernet_header = ""
    IP_header = ""
    source_ip = IP
    IP_header = IP_header + source_ip + dest_ip
    source_mac = MAC
    protocol = "0"
    data = message
    data_length = str(len(message))
    print('dest')
    print(start_time)
    
    if dest_ip in LOCAL_ARP_TABLE:
        destination_mac = LOCAL_ARP_TABLE[dest_ip] 
    else:
        destination_mac = 'R1'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + protocol + data_length + data
    
    return packet


while True:
    options = input("1. Send Message\n2. Send Ping\n")
    if options == '1':
        message = input("Please insert the message you want to send: ")
        dest_ip = input("Please insert the destination: ")
        send_local(wrap_packet_ip(message, dest_ip))
    elif options == '2':
        message = input("Which node do you want to ping?\n")
        # server.settimeout(20)
        # server.connect(tuple(message[5:]))
        # server.settimeout(None)
        # start = time.time()
        # print(start)
        # now = datetime.datetime.now()
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        print(now)
        # later = datetime.datetime.now()
        # diff = int(later - now)
        send_ping(wrap_ping_packet("Ping successful", message[5:], str(now)))
        # s = Timer(2.0, nArgs, ("OWLS","OWLS","OWLS"))
        # s.start()
        # end = time.time()
        # print(end - start)
    
    
    
    