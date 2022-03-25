import socket
import sys
import subprocess as sp
from timestamp import timestamp
from datetime import datetime
import json

extProc = sp.Popen(['python','attacker-node.py']) # runs myPyScript.py 

status = sp.Popen.poll(extProc) # status should be 'None'

print(status)
# sp.Popen.terminate(extProc) # closes the process

# status = sp.Popen.poll(extProc) # status should now be something other than 'None' ('1' in my testing)
IP = '0x3A'
MAC = 'E1'

local_arp_table = json.loads(open('arp-table-node1.json', 'r').read())

node1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node1.bind(("localhost", 8006))

def reply_ping(packet):
    node1.sendto(bytes(packet, "utf-8"), ("localhost", 8101))

def log_protocol(source_ip, source_mac, message):
    with open('node1.log', 'a') as file:
        file.write("\nSOURCE IP: " + source_ip + '\nSOURCE MAC: ' + source_mac + '\n' + 'MESSAGE: ' + message + '\n\n')

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
        destination_mac = 'R1'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + ping_type + protocol + data_length + data
    
    return packet
 
while True:
    received_message, addr = node1.recvfrom(1024)
    received_message = received_message.decode("utf-8")
    source_mac = received_message[0:2]
    destination_mac = received_message[2:4]
    ip_source = received_message[4:8]
    destination_ip =  received_message[8:12]

    protocol = received_message[12:13]
    data_length = received_message[13:16]
    # print(data_length)
    end_pos = 16 + int(data_length)
    message = received_message[16:end_pos]
    protocol = int(protocol)

    print("-----------" + timestamp() + "-----------")
    print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
    print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
    print("\nProtocol: Simple Messaging")
    print("\nData Length: " + data_length)
    print("\nMessage: " + message)
    print("----------------------------------")
    