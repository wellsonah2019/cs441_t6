import socket

IP = '0x1A'
MAC = 'N1'

node1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node1.bind(("localhost", 8001))
while True:
    received_message, addr = node1.recvfrom(1024)
    received_message = received_message.decode("utf-8")
    source_mac = received_message[0:2]
    destination_mac = received_message[2:4]
    source_ip = received_message[4:8]
    destination_ip =  received_message[8:12]
    message = received_message[12:]
    if IP == destination_ip and MAC == destination_mac:
        print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
        print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
        print("\nMessage: " + message)
    else:
        print("Packet received, but it ain't for u.")