from ctypes import addressof
import socket

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
    message = received_message[12:]
    if IP == destination_ip and MAC == destination_mac:
        print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
        print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
        print("\nMessage: " + message)
    elif destination_ip in connected_to_me:
        print("Packet received for node 1")
        if source_ip[2] != '1':
            print('received from outside network -- will pass to cable')
            send_local(received_message)
        else:
            print("But received locally -- therefore will not send")
    elif destination_ip[2] == '2':
        print("Packet received for destination outside network... \n Forwarding to router-nic2...")
        server.sendto(bytes(received_message, "utf-8"), ("localhost", 8102))
    else:
        print("Packet received but it aint for you")
        
    

