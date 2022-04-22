import socket
import time
import math


router_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
router_send.bind(("localhost", 8201))

client1_ip = "0x1A" # Change these 4 values
client1_mac = "N1"

router1_ip = "0x11"
router1_mac = "R1"

router_send.listen(100)
client1 = None
router1 = None
while (client1 == None):
    client, address = router_send.accept()
    print('yes')
    client1 = client
    print("Client 1 is online")
    
while router1 == None:
    client, address = router_send.accept()
    router1 = client
    print("Router 1 is online")

arp_table_socket = {client1_ip : client1, router1_ip: router1}
print(arp_table_socket)
router = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
router.bind(("localhost", 8101))
while True:
    data, address = router.recvfrom(4096)
    for client_ip in arp_table_socket:
        destination_socket = arp_table_socket[client_ip]
        destination_socket.send(data)
