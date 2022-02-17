import socket
import time

router = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
router.bind(("localhost", 8100))

router_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
router_send.bind(("localhost", 8200))

router_mac = "05:10:0A:CB:24:EF"

node2 = ("localhost", 8000)
node3 = ("localhost", 8001)
r2 = ("localhost", 8002)

client2_ip = "0x2A" # Change these 4 values
client2_mac = "N2"
client3_ip = "0x2B"
client3_mac = "N3"
router_send.listen(4)
client2 = None
client3 = None
while (client2 == None or client3 == None):
    client, address = router_send.accept()
    
    if(client2 == None):
        client2 = client
        print("Client 2 is online")
    else:
        client3 = client
        print("Client 3 is online")
arp_table_socket = {client2_ip : client2, client3_ip : client3}
arp_table_mac = {client2_ip : client2_mac, client3_ip : client3_mac}
router.listen(5)
while True:
    conn, addr = router.accept()
    print(conn)
    print(addr)
    packet = conn.recv(1024)
    for client_ip in arp_table_socket:
        destination_socket = arp_table_socket[client_ip]
        destination_socket.send(packet)
