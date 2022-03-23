import socket
import time
from datetime import datetime

IP = '0x2A'
MAC = 'N2'

LOCAL_ARP_TABLE = {
    "0x21": "R2",
    "0x2A": "N2",
    "0x2B": "N3"
}

node2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node2.bind(("localhost", 8002))
def send_ping(packet):
    node2.sendto(bytes(packet, "utf-8"), ("localhost", 8102))
    # node2.sendto(bytes(packet, "utf-8"), ("localhost", 8002))
    node2.sendto(bytes(packet, "utf-8"), ("localhost", 8003))

def wrap_ping_packet(message, dest_ip):
    ethernet_header = ""
    IP_header = ""
    source_ip = IP
    IP_header = IP_header + source_ip + dest_ip
    source_mac = MAC
    ICMP_header = "ICMP"
    
    if dest_ip in LOCAL_ARP_TABLE:
        destination_mac = LOCAL_ARP_TABLE[dest_ip] 
    else:
        destination_mac = 'R2'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + ICMP_header + message
    
    return packet

while True:
    received_message, address = node2.recvfrom(1024)
    if received_message:
        # print("INNN")
        received_message = received_message.decode("utf-8")
        source_mac = received_message[0:2]
        destination_mac = received_message[2:4]
        source_ip = received_message[4:8]
        destination_ip =  received_message[8:12]
        message = received_message[12:16]
        start_time = received_message[16:]
        # print('start')
        print(start_time)
        # print(message)

        # print("*************")
        # print(message)
        if message == "ICMP" and IP == destination_ip:
            # end = time.time()
            # total = end - float(start_time)
            # print(start_time)
            end = datetime.now()
            print(end)
            total = end - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            print('seconds')
            print(total.total_seconds())
            print("Ping successful: ", total.total_seconds())
            msg = "Reply from 0x2A: No lost packet, one way trip time: " + str(total.total_seconds())
            send_ping(wrap_ping_packet(msg, source_ip))
        elif IP == destination_ip and MAC == destination_mac:
            print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
            print("\nMessage: " + message)
        elif IP != destination_ip:
            print("Packet received, but it ain't for u.")