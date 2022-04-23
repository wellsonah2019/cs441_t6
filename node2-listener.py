import socket
import sys 
import subprocess as sp
from timestamp import timestamp
from datetime import datetime
import json
from time import sleep
# from collections.abc import Mapping
# import pickle
from post import post_exploit_state
from postexploit import poste


extProc = sp.Popen(['python','node2.py']) # runs myPyScript.py 

status = sp.Popen.poll(extProc) # status should be 'None'
IP = '0x2A'
MAC = 'N2'

local_arp_table = json.loads(open('arp-table-node2.json', 'r').read())

cable = ("localhost", 8200) 
node2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node2.bind(("localhost", 8002))

def reply_ping(packet):
    node2.sendto(bytes(packet, "utf-8"), ("localhost", 8102))
    node2.sendto(bytes(packet, "utf-8"), ("localhost", 8033))

def send_local(packet):
    node2.sendto(bytes(packet, "utf-8"), ("localhost", 8003))
    node2.sendto(bytes(packet, "utf-8"), ("localhost", 8004)) # Packet Sniffer
    node2.sendto(bytes(packet, "utf-8"), ("localhost", 8006)) # attacker



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

    print(dest_ip)
    if dest_ip in local_arp_table:
        print("dest ip in local arp table")
        destination_mac = local_arp_table[dest_ip] 
    else:
        destination_mac = 'R2'
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



while True:
    print('packet received')
    received_message, addr = node2.recvfrom(1024)
    received_message = received_message.decode("utf-8")
    source_mac = received_message[0:2]
    destination_mac = received_message[2:4]
    ip_source = received_message[4:8]
    destination_ip =  received_message[8:12]
    ping_type = ''
    protocol = ''
    data_length = ''
    message = ''
    start_time = ''
    # protocols = ["SYN", "ACK", "SAK", "RST"]
    # check if it is a dictionary
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
        destination_mac = ethernet_header[2:4]
        ip_header = received_message["IP_header"]
        ip_source = ip_header[0:4]
        destination_ip = ip_header[4:8]
        seq = received_message["seq"]
        ack = received_message["ack"]
        window_size = received_message["window_size"]
    # not a dictionary
    else:
        if received_message[12] == 'r':
            ping_type = received_message[12:15]
            protocol = received_message[15:16]
            data_length = received_message[16:19]
            # print(data_length)
            end_pos = 19 + int(data_length)
            message = received_message[19:end_pos]
            protocol = int(protocol)
            start_time = received_message[end_pos:]
            print("HERE", start_time)
        else:
            protocol = received_message[12:13]
            data_length = int(received_message[13:16])
            # print(data_length)
            end_pos = 16 + int(data_length)
            message = received_message[16:end_pos]
            protocol = int(protocol)
    # NOTE: for testing only
    # print("IP", IP)
    # print("dest ip", destination_ip)
    # print("MAC", MAC)
    # print("dest mac", destination_mac)

    if IP == destination_ip and MAC == destination_mac:
        if protocol == 3 or protocol == 7:
            print("-----------" + timestamp() + "-----------")
            print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
            print("\nProtocol: Simple Messaging")
            print("\nData Length: " + str(data_length))
            print("\nMessage: " + message)
            print("----------------------------------")
        elif protocol == 0:
            end = datetime.now()
            print(end)
            print("-----------" + timestamp() + "-----------")
            print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
            print("\nProtocol: Ping")
            print("\nData Length: " + str(data_length))
            print("\nMessage: " + message)
            print("----------------------------------")
            print(start_time)
            total = end - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            print("Ping successful: ", total.total_seconds() * 1000)
            # msg = "Reply from 0x2A: No lost packet, one way trip time: " + str(total.total_seconds() * 1000)
            if ip_source not in local_arp_table:
                node2.sendto(bytes(wrap_packet_ip(message, ip_source, str(protocol)), "utf-8"), ("localhost", 8003))
                node2.sendto(bytes(wrap_packet_ip(message, ip_source, str(protocol)), "utf-8"), ("localhost", 8102))
            else:
                reply_ping(wrap_packet_ip(message, ip_source, str(protocol)))

                
            # print(message)
        elif protocol == 1:
            print("-----------" + timestamp() + "-----------")
            print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
            print("\nProtocol: Log")
            print("\nData Length: " + str(data_length))
            print("\nMessage: " + message)
            print("----------------------------------")
            log_protocol(ip_source, source_mac, message)
        elif protocol == 2:
            print("-----------" + timestamp() + "-----------")
            print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
            print("\nProtocol: Kill")
            print("\nData Length: " + str(data_length))
            print("\nMessage: " + message)
            print("----------------------------------")
            print("Kill protocol has been given. Will exit now...")
            sp.Popen.terminate(extProc)
            sys.exit()
        elif protocol == 5:
            # POISON ARP HERE
            message = message.split(' ')
            my_mac = message[0]
            fake_ip = message[-1]
            local_arp_table[fake_ip] = my_mac
            with open('arp-table-node2.json', 'w') as f:
                f.write(json.dumps(local_arp_table))
            local_arp_table = json.loads(open('arp-table-node2.json', 'r').read()) 
            print("Noticed ARP table change. Restarting sender node...")
            sp.Popen.terminate(extProc)
            try:
                extProc = sp.Popen(['python','node2.py']) # runs myPyScript.py
                print("Sender node restarted.")
            except:
                print("Failed to restart sender node...")
                print("Please restart manually")
                print()
        elif str(protocol) == "6":
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

            # NOTE step 5 of TCP connection
            # print("special is ", special)
            if str(special).strip() == "2": 
                sleep(0.1) # gimmick way of making this appear later. probably need to change this
                to_send = wrap_packet_tcp("0x2B", "6", "ACK", seq=21, ack=51, special=5)
                # print("sending " + to_send)
                # input("Press Enter to continue...")
                node2.sendto(bytes(to_send, "utf-8"), ("localhost", 8003))
                node2.sendto(bytes(to_send, "utf-8"), ("localhost", 8006))
                # print("Step 5 of TCP handshake done!")
            # NOTE step 3 of attack
            elif str(special).strip() == "3":
                pass

            if post_exploit_state.getstate() != "0":
                # ack2 = poste.getack2()
                # ack2 = int(ack2) + data_length
                # # update seq 2 and ack 2
                # seq2 = poste.getseq2()
                # poste.setseq2(int(seq2)+data_length)
                if str(special).strip() == '69':
                    # attacker send back ACK here
                    to_send = wrap_packet_tcp("0x2B", "6", "ACK", seq=ack, ack=int(seq) + len(message), special=420, source_ip="0x2A", source_mac="N2")
                    send_local(to_send)
                    poste.setseq2((int(poste.getseq2()) + 1))
                pass

    elif destination_ip != IP and MAC == destination_mac:
        print("ARP-POISONED PACKET RECEIVED...")
        print("-----------" + timestamp() + "-----------")
        print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
        print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
        print("\nProtocol: " + str(protocol))
        print("\nData Length: " + str(data_length))
        print("\nMessage: " + message)    
        print()
        print("PACKET FOR 'ME'.")
        print("----------------------------------")
        print("WILL ACT NORMALLY FOR NOW...")
        print()
        print()

        if protocol == 3 or protocol == 7:
            print("-----------" + timestamp() + "-----------")
            print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
            print("\nProtocol: Simple Messaging")
            print("\nData Length: " + str(data_length))
            print("\nMessage: " + message)
            print("----------------------------------")
        elif protocol == 0:
            end = datetime.now()
            print(end)
            print("-----------" + timestamp() + "-----------")
            print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
            print("\nProtocol: Ping")
            print("\nData Length: " + str(data_length))
            print("\nMessage: " + message)
            print("----------------------------------")
            print(start_time)
            total = end - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            print("Ping successful: ", total.total_seconds() * 1000)
            # msg = "Reply from 0x2A: No lost packet, one way trip time: " + str(total.total_seconds() * 1000)
            if ip_source not in local_arp_table:
                node2.sendto(bytes(wrap_packet_ip(message, ip_source, str(protocol)), "utf-8"), ("localhost", 8003))
                node2.sendto(bytes(wrap_packet_ip(message, ip_source, str(protocol)), "utf-8"), ("localhost", 8102))
            else:
                reply_ping(wrap_packet_ip(message, ip_source, str(protocol)))

                
            # print(message)
        elif protocol == 1:
            print("-----------" + timestamp() + "-----------")
            print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
            print("\nProtocol: Log")
            print("\nData Length: " + str(data_length))
            print("\nMessage: " + message)
            print("----------------------------------")
            log_protocol(ip_source, source_mac, message)
        elif protocol == 2:
            print("-----------" + timestamp() + "-----------")
            print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
            print("\nProtocol: Kill")
            print("\nData Length: " + str(data_length))
            print("\nMessage: " + message)
            print("----------------------------------")
            print("Kill protocol has been given. Will exit now...")
            sp.Popen.terminate(extProc)
            sys.exit()
        elif protocol == 5:
            # POISON ARP HERE
            message = message.split(' ')
            my_mac = message[0]
            fake_ip = message[-1]
            local_arp_table[fake_ip] = my_mac
            with open('arp-table-node2.json', 'w') as f:
                f.write(json.dumps(local_arp_table))
            local_arp_table = json.loads(open('arp-table-node2.json', 'r').read()) 
            print("Noticed ARP table change. Restarting sender node...")
            sp.Popen.terminate(extProc)
            try:
                extProc = sp.Popen(['python','node2.py']) # runs myPyScript.py
                print("Sender node restarted.")
            except:
                print("Failed to restart sender node...")
                print("Please restart manually")
                print()
        elif str(protocol) == "6":
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

            # NOTE step 5 of TCP connection
            # print("special is ", special)
            if str(special).strip() == "2": 
                sleep(0.1) # gimmick way of making this appear later. probably need to change this
                to_send = wrap_packet_tcp("0x2B", "6", "ACK", seq=21, ack=51, special=5)
                # print("sending " + to_send)
                # input("Press Enter to continue...")
                node2.sendto(bytes(to_send, "utf-8"), ("localhost", 8003))
                node2.sendto(bytes(to_send, "utf-8"), ("localhost", 8006))
                # print("Step 5 of TCP handshake done!")
            # NOTE step 3 of attack
            elif str(special).strip() == "3":
                pass

            if post_exploit_state.getstate() != "0":
                # ack2 = poste.getack2()
                # ack2 = int(ack2) + data_length
                # # update seq 2 and ack 2
                # seq2 = poste.getseq2()
                # poste.setseq2(int(seq2)+data_length)
                if str(special).strip() == '69':
                    # attacker send back ACK here
                    to_send = wrap_packet_tcp("0x2B", "6", "ACK", seq=ack, ack=int(seq) + len(message), special=420, source_ip="0x2A", source_mac="N2")
                    send_local(to_send)
                    poste.setseq2((int(poste.getseq2()) + 1))
                pass

        # change message, source ip, etc. into a real packet to actual destination

    else:
        # NOTE debug
        print()

        print("-----------" + timestamp() + "-----------")
        print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
        print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
        print("\nProtocol: " + str(protocol))
        print("\nData Length: " + str(data_length))
        print("\nMessage: " + message)    
        print()
        print("PACKET NOT FOR ME. DROPPING NOW...")
        print("----------------------------------")