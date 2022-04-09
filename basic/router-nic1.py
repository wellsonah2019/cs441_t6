from ctypes import addressof
import socket
import sys
from timestamp import timestamp
from datetime import datetime

IP = '0x11'
MAC = 'R1'

connected_to_me = {
    "0x1A": "N1",
}

other_router_nic = {
    "0x21": "R2"
}

def send_local(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8001))

def reply_ping(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8011))

def log_protocol(source_ip, source_mac, message):
    with open('router-nic1.log', 'a') as file:
        file.write("SOURCE IP: " + source_ip + '\nSOURCE MAC: ' + source_mac + '\n' + 'MESSAGE: ' + message + '\n\n')

router1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
router1.bind(("localhost", 8101))

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('yes here')


def wrap_packet_ping(message, dest_ip, protocol):
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

    if dest_ip in connected_to_me:
        destination_mac = connected_to_me[dest_ip] 
    else:
        destination_mac = 'R2'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + ping_type + protocol + str(data_length) + data
    
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

    if dest_ip in connected_to_me:
        destination_mac = connected_to_me[dest_ip] 
    else:
        destination_mac = 'R2'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + protocol + data_length + data
    
    return packet

while True:
    received_message, addr = router1.recvfrom(1024)
    received_message = received_message.decode("utf-8")
    source_mac = received_message[0:2]
    destination_mac = received_message[2:4]
    source_ip = received_message[4:8]
    destination_ip =  received_message[8:12]
    ping_type = ''
    protocol = ''
    data_length = ''
    message = ''
    start_time = ''
    if received_message[12] == 'r':
        ping_type = received_message[12:15]
        protocol = received_message[15:16]
        data_length = int(received_message[16:19])
        # print(data_length)
        end_pos = 19 + data_length
        message = received_message[19:end_pos]
        protocol = int(protocol)
        start_time = received_message[end_pos:]
    else:
        protocol = received_message[12:13]
        data_length = int(received_message[13:16])
        # print(data_length)
        end_pos = 16 + data_length
        message = received_message[16:end_pos]
        protocol = int(protocol)
    # protocol = received_message[12:13]
    # data_length = received_message[13:16]
    # protocol = int(protocol)
    # message = received_message[16:]
    print(destination_mac)
    print(destination_ip)
    if IP != destination_ip or MAC != destination_mac:
        print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
        print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=source_ip, destination_ip=destination_ip))
        print("\nProtocl: " + str(protocol))
        print("\nData Length: " + str(data_length))
        print("\nMessage: " + message)    
        print()
        print("PACKET NOT FOR ME. ROUTING NOW...")
    if IP == destination_ip and MAC == destination_mac:
        if protocol == 3:
            print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
            print("\nData Length: " + str(data_length))
            print("\nMessage: " + message)
        elif protocol == 0:
            print("RECEIVED PING REQUEST...")
            end = datetime.now()
            print(end)
            print("-----------" + timestamp() + "-----------")
            print("\nThe packet received:\nSource MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
            print("\nProtocol: Ping")
            print("\nData Length: " + str(data_length))
            print("\nMessage: " + message)
            print("----------------------------------")
            total = end - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            print("Ping successful: " + str(round(total.total_seconds() * 1000, 2)) + "ms")
            print("REPLYING NOW...")
            if source_ip[2] == '1':
                reply_ping(wrap_packet_ping(message, source_ip, str(protocol)))
            else:
                server.sendto(bytes(wrap_packet_ping(message, source_ip, str(protocol)), "utf-8"), ("localhost", 8102))
        elif protocol == 1:
            print("-----------" + timestamp() + "-----------")
            print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=source_ip, destination_ip=destination_ip))
            print("\nProtocol: Log")
            print("\nData Length: " + str(data_length))
            print("\nMessage: " + message)
            print("----------------------------------")
            log_protocol(source_ip, source_mac, message)
        elif protocol == 2:
            print("Kill protocol has been given. Will exit now...")
            sys.exit()
        elif protocol == 5:
            print("ARP Request has been made...")
            message = message.split(' ')
            my_mac = message[0]
            fake_ip = message[-1]
            print("Registering IP {} with MAC {}".format(fake_ip, my_mac))
            connected_to_me[fake_ip] = my_mac
            print("Current ARP Table:")
            print(connected_to_me)
    elif destination_ip in connected_to_me:
        print("Packet received for destination current network... \nForwading to current network...")
        print("CURRENT SOURCE MAC ADDRESS:", source_mac)
        print("CURRENT DESTINATION MAC ADDRESS:", destination_mac)
        print("CHANGING SOURCE MAC ADDRESS TO {}...".format(MAC))
        print("CHANGING MAC ADDRESS TO {}...".format(connected_to_me[destination_ip]))
        received_message = MAC + str(connected_to_me[destination_ip]) + received_message[4:]
        if source_ip[2] != '1':
            if protocol == 0:
                if ping_type == 'rep':
                    reply_ping(received_message)
                else:
                    send_local(received_message)
            else:
                print('received from outside network -- will pass to cable')
                send_local(received_message)
            # print('received from outside network -- will pass to cable')
            # send_local(received_message)
        else:
            print("But received locally -- therefore will not send")
    elif destination_ip[2] == '2':
        print("Packet received for destination outside network... \nForwarding to router-nic2...")
        print("CURRENT SOURCE MAC ADDRESS:", source_mac)
        print("CURRENT DESTINATION MAC ADDRESS:", destination_mac)
        print("CHANGING SOURCE MAC ADDRESS TO {}...".format(MAC))
        print("CHANGING MAC ADDRESS TO R2...")
        received_message = [char for char in received_message]
        received_message[0] = 'R'
        received_message[1] = '1'
        received_message[2:4] = [char for char in other_router_nic['0x21']]
        received_message = ''.join(received_message)
        destination_mac = received_message[2:4]
        server.sendto(bytes(received_message, "utf-8"), ("localhost", 8102))

