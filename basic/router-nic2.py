from ctypes import addressof
import socket
import sys

IP = '0x21'
MAC = 'R2'

connected_to_me = {
    "0x2A": "N2",
    "0x2B": "N3"
}

other_router = {
    "0x11": "R1"
}

def send_local(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8002))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8003))

router1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
router1.bind(("localhost", 8102))

def log_protocol(source_ip, source_mac, message):
    with open('node2.log', 'a') as file:
        file.write("SOURCE IP: " + source_ip + '\nSOURCE MAC: ' + source_mac + '\n' + 'MESSAGE: ' + message + '\n\n')

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('yes here')
while True:
    received_message, addr = router1.recvfrom(1024)
    received_message = received_message.decode("utf-8")
    source_mac = received_message[0:2]
    destination_mac = received_message[2:4]
    source_ip = received_message[4:8]
    destination_ip =  received_message[8:12]
    protocol = received_message[12:13]
    data_length = received_message[13:16]
    protocol = int(protocol)
    message = received_message[16:]
    if IP == destination_ip and MAC == destination_mac:
        if protocol == 3:
            print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
            print("\nData Length: " + data_length)
            print("\nMessage: " + message)
        elif protocol == 0:
            pass # insert ping function here
        elif protocol == 1:
            log_protocol(source_ip, source_mac, message)
        elif protocol == 2:
            print("Kill protocol has been given. Will exit now...")
            sys.exit()
    elif destination_ip in connected_to_me:
        received_message = received_message[0:2] + str(connected_to_me[destination_ip]) + received_message[4:]
        print("Packet received for a node in my network")
        if source_ip[2] != '2':
            print('received from outside network -- will pass to cable')
            send_local(received_message)
        else:
            print("But received locally -- therefore will not send")
    elif destination_ip[2] == '1':
        print("Packet received for destination outside network... \n Forwarding to router-nic1...")
        server.sendto(bytes(received_message, "utf-8"), ("localhost", 8101))
    else:
        print("Packet received but it ain't for you")
        
    

