import socket
import sys 
import subprocess as sp
from timestamp import timestamp
from datetime import datetime
import json
# from collections.abc import Mapping
# import pickle

extProc = sp.Popen(['python','attacker-node.py']) # runs myPyScript.py 

status = sp.Popen.poll(extProc) # status should be 'None'
IP = '0x2A'
MAC = 'N2'

local_arp_table = json.loads(open('arp-table-node2.json', 'r').read())

# cable = ("localhost", 8200) 
node2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node2.bind(("localhost", 8006))

def reply_ping(packet):
    node2.sendto(bytes(packet, "utf-8"), ("localhost", 8102))
    node2.sendto(bytes(packet, "utf-8"), ("localhost", 8033))

def log_protocol(source_ip, source_mac, message):
    with open('node2.log', 'a') as file:
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
        data_length = '0' + str(data_length)
    elif len(data_length) == 1:
        data_length = '00' + str(data_length)

    if dest_ip in local_arp_table:
        destination_mac = local_arp_table[dest_ip] 
    else:
        destination_mac = 'R2'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + ping_type + protocol + str(data_length) + data
    
    return packet
print('packet received before while loop')

# NOTE: TCP stuff
def wrap_packet_tcp(message, dest_ip, protocol, start_time):
    # SYN, ACK, SAK (SYN-ACK), RST
    ethernet_header = ""
    IP_header = ""
    source_ip = IP
    IP_header = IP_header + source_ip + dest_ip
    source_mac = MAC
    protocol = protocol
    data = message
    data_length = str(len(message))
    tcp_type = 'something' # TODO: change 
    start_time = start_time

    if len(data_length) == 2:
        data_length = '0' + data_length
    elif len(data_length) == 1:
        data_length = '00' + data_length

    if dest_ip in local_arp_table:
        destination_mac = local_arp_table[dest_ip] 
    else:
        destination_mac = 'R1'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + tcp_type + protocol + data_length + data + start_time
    
    return packet

while True:
    print('packet received')
    received_message, addr = node2.recvfrom(1024)
    received_message = received_message.decode("utf-8")
    source_mac = received_message[0:2]
    destination_mac = received_message[2:4]
    ip_source = received_message[4:8]
    destination_ip =  received_message[8:12]

    # protocols = ["SYN", "ACK", "SAK", "RST"]
    if "{" in received_message and "}" in received_message:
        # tcp_control_flag = received_message[12:15]
        # protocol = received_message[15:16]
        # data_length = received_message[16:19]
        # # print(data_length)
        # end_pos = 19 + int(data_length)
        # message = received_message[19:end_pos]
        # protocol = int(protocol)
        # start_time = received_message[end_pos:]
        # special = received_message[-1]
        received_message = json.loads(received_message)
        tcp_control_flag = received_message["ctl"]
        protocol = received_message["protocol"]
        data_length = received_message["data_length"]
        # print(data_length)
        message = received_message["data"]
        special = received_message["special"]
        ethernet_header = received_message["ethernet_header"]
        source_mac = ethernet_header[0:2]
        ip_header = received_message["IP_header"]
        ip_source = ip_header[0:4]
        destination_ip = ip_header[4:8]
        destination_ip =  ethernet_header[8:12]
        seq = received_message["seq"]
        ack = received_message["ack"]
        window_size = received_message["window_size"]
    else:
      protocol = received_message[12:13]
      data_length = int(received_message[13:16])
      end_pos = 16 + int(data_length)
      message = received_message[16:end_pos]
      protocol = int(protocol)
   
    print("-----------" + timestamp() + "-----------")
    print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
    print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
    print("\nProtocol: TCP")
    print("\nData Length: " + str(data_length))
    if tcp_control_flag:
      if tcp_control_flag == "SAK":
        print("\nTCP Control Flag: SYN-ACK")
      else:
        print("\nTCP Control Flag: " + tcp_control_flag)
    print("\nSeq: " + seq)
    print("\nAck: " + ack)
    print("\nMessage: " + message)    
    print("----------------------------------")