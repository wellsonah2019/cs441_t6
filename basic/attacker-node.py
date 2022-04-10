import socket
from datetime import datetime
from timestamp import date_time
import json
from post import post_exploit_state
from postexploit import poste

IP = '0x3A'
MAC = 'N9'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 8066))

local_arp_table = json.loads(open('arp-table-node1.json', 'r').read())


def send_local(packet):
  server.sendto(bytes(packet, "utf-8"), ("localhost", 8102)) # router
  server.sendto(bytes(packet, "utf-8"), ("localhost", 8002))
  server.sendto(bytes(packet, "utf-8"), ("localhost", 8003))

def send_rst_syn(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8003))

def wrap_packet_ping(message, dest_ip, protocol, start_time):
    ethernet_header = ""
    IP_header = ""
    source_ip = IP
    IP_header = IP_header + source_ip + dest_ip
    source_mac = MAC
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
        destination_mac = 'R1'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + ping_type + protocol + data_length + data + start_time
    
    return packet

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
        destination_mac = 'R1'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + protocol + data_length + data
    
    return packet

# NOTE creates tcp packets to send
def wrap_packet_tcp(
    dest_ip, protocol, ctl=None, message="", 
    seq = 20, ack = None, special = 1, source_ip=IP, source_mac=MAC
):
    # special is to indicate the step of the attack, starting from 1
    ethernet_header = ""
    IP_header = ""
    source_ip = source_ip
    IP_header = IP_header + source_ip + dest_ip
    source_mac = source_mac
    protocol = protocol
    data = message
    data_length = str(len(message))
    ctl = ctl
    seq = str(seq)
    ack = str(ack)
    window_size = "100"
    special = str(special)

    if len(data_length) == 2:
        data_length = '0' + data_length
    elif len(data_length) == 1:
        data_length = '00' + data_length

    if dest_ip in local_arp_table:
        print("dest ip in local arp table")
        destination_mac = local_arp_table[dest_ip] 
    else:
        destination_mac = 'N2'
    # print(destination_mac)
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = {
        "ethernet_header": ethernet_header,
        "IP_header": IP_header, 
        "ctl": ctl, 
        "protocol": protocol, 
        "data_length": data_length, 
        "data": data, 
        "seq": seq, 
        "ack": ack, 
        "window_size": window_size, 
        "special": special 
    }
    
    # ethernet_header + IP_header + ctl + protocol +\
    #     data_length + data + seq + seq + window_size + special
    
    return json.dumps(packet)

while True:
    protocol = input("[Attacker Node] \n Please select what protocol you would like to use: \n 0. Ping Protocol \n 1. Log Protocol \n 2. Kill Protocol \n 3. Simple Messaging \n5. ARP Poisoning\n6. TCP Connection")
    dest_ip = input("Please insert the destination: ")
    print(type(protocol))
    print(type(dest_ip))
    if protocol == str(3):
        print("IN NODE1 protocol 3 LINE 50")
        message = input("Please insert the message you want to send: ")
        while len(message) > 256:
            print()
            print("Message is too long")
            message = input("Please insert the message you want to send: ")
        send_local(wrap_packet_ip(message, dest_ip, protocol))
    elif protocol == str(0):
        message = input("Please insert the message you want to send: ")
        while len(message) > 256:
            print()
            print("Message is too long")
            message = input("Please insert the message you want to send: ")
        start = datetime.now()
        now = start.strftime("%Y-%m-%d %H:%M:%S.%f")
        # print(now)
        # later = datetime.datetime.now()
        # diff = int(later - now)
        # send_ping(wrap_ping_packet("Ping successful", message[5:], str(now)))
        send_local(wrap_packet_ping(message, dest_ip, protocol, str(now)))
        server.settimeout(10)
        ip_source = ""
        try:
            received_message, addr = server.recvfrom(1024)
            end = datetime.now()
            received_message = received_message.decode("utf-8")
            source_mac = received_message[0:2]
            destination_mac = received_message[2:4]
            ip_source = received_message[4:8]
            destination_ip =  received_message[8:12]
            data_length = int(received_message[16:19])
            end_pos = 19 + data_length
            message = received_message[19:end_pos]
            if IP == destination_ip:
                # print(end)
                total = end - start
                print(total.total_seconds())
                print('Reply from ' + ip_source)
                print("-----------" + date_time() + "-----------")
                print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
                print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
                print("\nProtocol: Ping")
                print("\nData Length: " + str(data_length))
                print("\nMessage: " + message)
                print("\nApproximate round trip in ms: " + str(round(total.total_seconds() * 1000, 2)))
                print("----------------------------------")
                print(message)
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
    # NOTE: tcp stuff
    elif protocol == str(6):
        if post_exploit_state.getstate() != "0":
            msg = input("Enter message please: ")
            seq3 = poste.getseq3()
            ack3 = poste.getack3()
            length = len(msg)
            to_send = wrap_packet_tcp("0x2A", "6", "ACK", message=msg, ack=int(ack3)+length, seq=int(seq3), special=69)
            poste.setack2(seq3)
            poste.setseq2(int(ack3)+length)
            send_local(to_send)
