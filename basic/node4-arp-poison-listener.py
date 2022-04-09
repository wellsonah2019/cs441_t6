import socket
import sys
import subprocess as sp
from timestamp import timestamp
import firewall
from datetime import datetime
import json

extProc = sp.Popen(['python','node4-arp-poison.py']) # runs myPyScript.py 

IP = '0x2C'
MAC = 'N4'

local_arp_table = json.loads(open('arp-table-node4.json', 'r').read())

# FIREWALL_RULE_N3 = {
#     "allow": [],
#     "deny": []
# }

cable = ("localhost", 8200) 
node3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node3.bind(("localhost", 8004))


def reply_ping(packet):
    node3.sendto(bytes(packet, "utf-8"), ("localhost", 8102))
    node3.sendto(bytes(packet, "utf-8"), ("localhost", 8022))

def log_protocol(source_ip, source_mac, message):
    with open('node4.log', 'a') as file:
        file.write("\nSOURCE IP: " + source_ip + '\nSOURCE MAC: ' + source_mac + '\n' + 'MESSAGE: ' + message + '\n\n')
    print("Successfully written to log file!")

def wrap_packet_ip(message, dest_ip, protocol):
    ethernet_header = ""
    IP_header = ""
    source_ip = IP
    IP_header = IP_header + source_ip + dest_ip
    source_mac = MAC
    protocol = protocol
    data = message
    data_length = str(len(message))
    ping_type = 'rep'

    if len(data_length) == 2:
        data_length = '0' + data_length
    elif len(data_length) == 1:
        data_length = '00' + data_length

    if dest_ip in local_arp_table:
        destination_mac = local_arp_table[dest_ip] 
    else:
        destination_mac = 'R2'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + ping_type + protocol + data_length + data
    
    return packet
 
 
while True:
    received_message, address = node3.recvfrom(1024)
    if received_message:
        received_message = received_message.decode("utf-8")
        print(received_message)
        source_mac = received_message[0:2]
        destination_mac = received_message[2:4]
        ip_source = received_message[4:8]
        destination_ip =  received_message[8:12]
        ping_type = ''
        protocol = ''
        data_length = ''
        message = ''
        start_time = ''
        protocol = received_message[12:13]
        data_length = int(received_message[13:16])
        # print(data_length)
        end_pos = 16 + int(data_length)
        message = received_message[16:end_pos]
        protocol = int(protocol)
        print("ARP-POISONED PACKET RECEIVED...")
        print("-----------" + timestamp() + "-----------")
        print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
        print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
        print("\nProtocol: " + str(protocol))
        print("\nData Length: " + str(data_length))
        print("\nMessage: " + message)    
        print()
        print("PACKET FOR 'ME'. DOING MITM ATTACK...")
        print("----------------------------------")