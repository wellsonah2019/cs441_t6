import socket
from datetime import datetime
from timestamp import date_time
import firewall
import json

ip = '0x2C'
mac = 'N4'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

local_arp_table = json.loads(open('arp-table-node4.json', 'r').read())

def send_local(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8102))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8002))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8003))
    
def send_out(packet):
    pass

def wrap_packet_ping(message, dest_ip, protocol, start_time):
    ethernet_header = ""
    ip_header = ""
    source_ip = ip
    ip_header = ip_header + source_ip + dest_ip
    source_mac = mac
    protocol = protocol
    data = message
    data_length = str(len(message))
    ping_type = 'req'
    start_time = start_time

    if len(data_length) == 2:
        data_length = '0' + data_length
    elif len(data_length) == 1:
        data_length = '00' + data_length

    if dest_ip in local_arp_table:
        destination_mac = local_arp_table[dest_ip] 
    else:
        destination_mac = 'R2'
    # print(destination_mac)
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + ip_header + ping_type + protocol + data_length + data + start_time
    
    return packet

def wrap_packet_ip(message, dest_ip, protocol):
    ethernet_header = ""
    ip_header = ""
    source_ip = ip
    ip_header = ip_header + source_ip + dest_ip
    source_mac = mac
    protocol = protocol
    data = message
    data_length = str(len(message))

    if len(data_length) == 2:
        data_length = '0' + data_length
    elif len(data_length) == 1:
        data_length = '00' + data_length

    if dest_ip in local_arp_table:
        destination_mac = local_arp_table[dest_ip] 
    else:
        destination_mac = 'R2'
    
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + ip_header + protocol + data_length + data
    
    return packet


while True:
    protocol = input("[Node 4] \nPlease select what protocol you would like to use: \n1. Log Protocol \n2. Kill Protocol \n3. Simple Messaging \n4. Configure firewall \n5. ARP Poisoning\n")
    ip = input("Enter the fake source IP: ")
    mac = input("Enter the fake source MAC: ")
#   NOTE: firewall config
    if protocol == str(4):
        print("Current firewall configuration: ")
        print("Blocked IPs: {}".format(str(firewall.getfwall())))
        ip_to_block = input("Please enter the IP address to be blocked, or [exit]: ")
        if ip_to_block == "exit":
            print("Exited firewall configuration!")
        elif ip_to_block not in firewall.getfwall():
            firewall.writefwall(ip_to_block)
            print("{} is now blocked!".format(ip_to_block))
        else:
            print("{} is already blocked!".format(ip_to_block))
    else:
        dest_ip = input("Please insert the destination: ")
        if protocol == str(3):
            message = input("Please insert the message you want to send: ")
            while len(message) > 256:
                print()
                print("Message is too long")
                message = input("Please insert the message you want to send: ")
            send_local(wrap_packet_ip(message, dest_ip, protocol))
        
        elif protocol == str(1):
            log_message = input("Please insert the log details: ")
            log_message = str(date_time()) + " " + log_message
            send_local(wrap_packet_ip(log_message, dest_ip, protocol))
        elif protocol == str(5):
            fake_ip = input("Please insert your fake IP: ")
            if " " in fake_ip:
                fake_ip = input("Do not include spaces! Please insert your fake ip: ")
            message = "{} has IP {}".format(mac, fake_ip)
            send_local(wrap_packet_ip(message, dest_ip, protocol))
        elif protocol == str(2): 
            message = ''
            send_local(wrap_packet_ip(message, dest_ip, protocol))
    