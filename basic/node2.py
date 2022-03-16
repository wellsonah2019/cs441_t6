import socket
from datetime import datetime

IP = '0x2A'
MAC = 'N2'
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


LOCAL_ARP_TABLE = {
    "0x21": "R2",
    "0x2A": "N2",
    "0x2B": "N3"
}
def send_local(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8102))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8002))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8003))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8004)) # Packet Sniffer

def wrap_packet_ip(message, dest_ip, protocol):
    ethernet_header = ""
    IP_header = ""
    source_ip = IP
    IP_header = IP_header + source_ip + dest_ip
    source_mac = MAC
    protocol = protocol
    data = message
    data_length = str(len(message))

    if len(data_length) == 2:
        data_length = '0' + data_length
    elif len(data_length) == 1:
        data_length = '00' + data_length

    if dest_ip in LOCAL_ARP_TABLE:
        destination_mac = LOCAL_ARP_TABLE[dest_ip] 
    else:
        destination_mac = 'R2'
    print(destination_mac)
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + protocol + data_length + data
    
    return packet


while True:
    protocol = input("Please select what protocol you would like to use: \n 0. Ping Protocol \n 1. Log Protocol \n 2. Kill Protocol \n 3. Simple Messaging \n")
    dest_ip = input("Please insert the destination: ")
    if protocol == str(3):
        message = input("Please insert the message you want to send: ")
        while len(message) > 256:
            print()
            print("Message is too long")
            message = input("Please insert the message you want to send: ")
        send_local(wrap_packet_ip(message, dest_ip, protocol))
    elif protocol == str(0):
        pass # send ping here

    elif protocol == str(1):
        log_message = input("Please insert the log details: ")
        log_message = str(datetime.now()) + " " + log_message
        send_local(wrap_packet_ip(log_message, dest_ip, protocol))

    else: 
        message = ''
        send_local(wrap_packet_ip(message, dest_ip, protocol))
    
    
    
    