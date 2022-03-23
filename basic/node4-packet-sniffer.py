import socket
import sys 
import subprocess as sp

node4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node4.bind(("localhost", 8004))

while True:
    received_message, addr = node4.recvfrom(1024)
    received_message = received_message.decode("utf-8")
    source_mac = received_message[0:2]
    destination_mac = received_message[2:4]
    source_ip = received_message[4:8]
    destination_ip =  received_message[8:12]
    protocol = received_message[12:13]
    data_length = received_message[13:16]
    print(data_length)
    message = received_message[16:]
    protocol = int(protocol)
    print("\nThe packet received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
    print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
    print('\nProtocol: ' + str(protocol))
    print("\nData Length: " + data_length)
    print("\nMessage: " + message)
    