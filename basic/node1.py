import socket
from datetime import datetime

IP = '0x1A'
MAC = 'N1'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 8011))


LOCAL_ARP_TABLE = {
    "0x11": "R1",
    "0x1A": "N1"
}
def send_local(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8001))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8101))

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

    if dest_ip in LOCAL_ARP_TABLE:
        destination_mac = LOCAL_ARP_TABLE[dest_ip] 
    else:
        destination_mac = 'R1'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + protocol + data_length + data
    
    return packet


while True:
    protocol = input("Please select what protocol you would like to use: \n 0. Ping Protocol \n 1. Log Protocol \n 2. Kill Protocol \n 3. Simple Messaging \n")
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
        send_local(wrap_packet_ip("PING", dest_ip, protocol))
        server.settimeout(10)
        ip_source = ""
        try:
            received_message, addr = server.recvfrom(1024)
            received_message = received_message.decode("utf-8")
            ip_source = received_message[4:8]
            destination_ip =  received_message[8:12]
            message = received_message[16:]
            if IP == destination_ip:
                print('Reply from ' + ip_source)
                print(message[:-1])
        except socket.timeout as e:
            print(e)

    elif protocol == str(1):
        log_message = input("Please insert the log details: ")
        log_message = str(datetime.now()) + " " + log_message
        send_local(wrap_packet_ip(log_message, dest_ip, protocol))

    else: 
        message = ''
        send_local(wrap_packet_ip(message, dest_ip, protocol))