import socket
import time
router = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
router.bind(("localhost", 8100))

router_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
router_send.bind(("localhost", 8200))

client2_ip = "0x2A" # Change these 4 values
client2_mac = "N2"
client3_ip = "0x2B"
client3_mac = "N3"
router1_ip = "0x21"
router1_mac = "R2"
router_send.listen(100)
client2 = None
client3 = None
router1 = None
while (client2 == None or client3 == None):
    client, address = router_send.accept()
    
    if(client2 == None):
        client2 = client
        print("Client 2 is online")
    else:
        client3 = client
        print("Client 3 is online")

while router1 == None:
    client, address = router_send.accept()
    router1 = client
    print("Router 2 is online")

arp_table_socket = {client2_ip : client2, client3_ip : client3, router1_ip: router1}
print(arp_table_so~cket)

while True:
    data, address = router.recvfrom(4096)
    for client_ip in arp_table_socket:
        destination_socket = arp_table_socket[client_ip]
        destination_socket.send(data)
