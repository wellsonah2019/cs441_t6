import socket
import sys
import subprocess as sp
from timestamp import timestamp
from datetime import datetime
import json

extProc = sp.Popen(['python','node1.py']) # runs myPyScript.py 

status = sp.Popen.poll(extProc) # status should be 'None'

print(status)
# sp.Popen.terminate(extProc) # closes the process

# status = sp.Popen.poll(extProc) # status should now be something other than 'None' ('1' in my testing)
IP = '0x1A'
MAC = 'N1'

local_arp_table = json.loads(open('arp-table-node1.json', 'r').read())

node1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node1.bind(("localhost", 8001))

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
        data_length = '0' + str(data_length)
    elif len(data_length) == 1:
        data_length = '00' + str(data_length)

    if dest_ip in local_arp_table:
        destination_mac = local_arp_table[dest_ip] 
    else:
        destination_mac = 'R1'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + ping_type + protocol + str(data_length) + data
    
    return packet
 
while True:
    received_message, addr = node1.recvfrom(1024)
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
    if received_message[12] == 'r':
        ping_type = received_message[12:15]
        protocol = received_message[15:16]
        data_length = received_message[16:19]
        # print(data_length)
        end_pos = 19 + int(data_length)
        message = received_message[19:end_pos]
        protocol = int(protocol)
        start_time = received_message[end_pos:]
    else:
        protocol = received_message[12:13]
        data_length = received_message[13:16]
        # print(data_length)
        end_pos = 16 + int(data_length)
        message = received_message[16:end_pos]
        protocol = int(protocol)
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
            total = end - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            print("Ping successful: " + str(round(total.total_seconds() * 1000, 2)) + "ms")
            # msg = "Reply from 0x2A: No lost packet, one way trip time: " + str(total.total_seconds() * 1000)
            reply_ping(wrap_packet_ip(message, ip_source, str(protocol)))
            print(message)
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
            with open('arp-table-node1.json', 'w') as f:
                f.write(json.dumps(local_arp_table))
            local_arp_table = json.loads(open('arp-table-node1.json', 'r').read()) 
            print("Noticed ARP table change. Restarting sender node...")
            sp.Popen.terminate(extProc)
            try:
                extProc = sp.Popen(['python','node1.py']) # runs myPyScript.py
                print("Sender node restarted.")
            except:
                print("Failed to restart sender node...")
                print("Please restart manually")
                print()
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
            total = end - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            print("Ping successful: " + str(round(total.total_seconds() * 1000, 2)) + "ms")
            # msg = "Reply from 0x2A: No lost packet, one way trip time: " + str(total.total_seconds() * 1000)
            reply_ping(wrap_packet_ip(message, ip_source, str(protocol)))
            print(message)
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
            with open('arp-table-node1.json', 'w') as f:
                f.write(json.dumps(local_arp_table))
            local_arp_table = json.loads(open('arp-table-node1.json', 'r').read()) 
            print("Noticed ARP table change. Restarting sender node...")
            sp.Popen.terminate(extProc)
            try:
                extProc = sp.Popen(['python','node1.py']) # runs myPyScript.py
                print("Sender node restarted.")
            except:
                print("Failed to restart sender node...")
                print("Please restart manually")
                print()
    else:
        print("-----------" + timestamp() + "-----------")
        print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
        print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
        print("\nProtocol: " + str(protocol))
        print("\nData Length: " + str(data_length))
        print("\nMessage: " + message)    
        print()
        print("PACKET NOT FOR ME. DROPPING NOW...")
        print("---------------------------------")