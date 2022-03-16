from ctypes import addressof
import socket
import sys

IP = '0x11'
MAC = 'R1'

connected_to_me = {
    "0x1A": "N1"
}

other_router = {
    "0x21": "R2"
}

def send_local(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8001))

def log_protocol(source_ip, source_mac, message):
    with open('node2.log', 'a') as file:
        file.write("SOURCE IP: " + source_ip + '\nSOURCE MAC: ' + source_mac + '\n' + 'MESSAGE: ' + message + '\n\n')

router1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
router1.bind(("localhost", 8101))

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
    print(destination_mac)
    print(destination_ip)
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
        if source_ip[2] != '1':
            print('received from outside network -- will pass to cable')
            send_local(received_message)
        else:
            print("But received locally -- therefore will not send")
    elif destination_ip[2] == '2':
        print("Packet received for destination outside network... \n Forwarding to router-nic2...")
        received_message = [char for char in received_message]
        received_message[2] = 'R'
        received_message[3] = '2'
        received_message = ''.join(received_message)
        print(received_message)
        server.sendto(bytes(received_message, "utf-8"), ("localhost", 8102))
    else:
        print("Packet received but it aint for you")
        
    

