import socket
from datetime import datetime
from timestamp import date_time
import firewall
import json

IP = '0x2B'
MAC = 'N3'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 8033))

local_arp_table = json.loads(open('arp-table-node3.json', 'r').read())

def send_local(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8102))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8002))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8004)) # Packet Sniffer
    
def send_out(packet):
    pass

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

    if dest_ip in local_arp_table:
        destination_mac = local_arp_table[dest_ip] 
    else:
        destination_mac = 'R2'
    
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + protocol + data_length + data
    
    return packet


while True:
    protocol = input("[Node 3] \nPlease select what protocol you would like to use: \n0. Ping Protocol \n1. Log Protocol \n2. Kill Protocol \n3. Simple Messaging \n4. Configure firewall \n5. ARP Poisoning\n")
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
        elif protocol == str(0):
            # print("SEND LOCAL PING")
            send_local(wrap_packet_ip("PING", dest_ip, protocol))
            server.settimeout(10)
            ip_source = ""
            try:
                # print("RECEIVING REPLY")
                received_message, addr = server.recvfrom(1024)
                received_message = received_message.decode("utf-8")
                ip_source = received_message[4:8]
                destination_ip =  received_message[8:12]
                message = received_message[16:]
                if IP == destination_ip:
                    print('Reply from ' + ip_source)
                    print(message[:-1])
                    server.settimeout(None)
            except socket.timeout as e:
                print(e)
                print()

        elif protocol == str(1):
            log_message = input("Please insert the log details: ")
            log_message = str(date_time()) + " " + log_message
            send_local(wrap_packet_ip(log_message, dest_ip, protocol))
        elif protocol == str(5):
            fake_ip = input("Please insert your fake IP: ")
            if " " in fake_ip:
                fake_ip = input("Do not include spaces! Please insert your fake ip: ")
            message = "{} has IP {}".format(MAC, fake_ip)
            send_local(wrap_packet_ip(message, dest_ip, protocol))
        else: 
            message = ''
            send_local(wrap_packet_ip(message, dest_ip, protocol))
    