import socket

IP = '0x2B'
MAC = 'N3'
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


LOCAL_ARP_TABLE = {
    "0x21": "R2",
    "0x2A": "N2"
}
def send_local(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8100))

def send_out(packet):
    pass

def wrap_packet_ip(message, dest_ip):
    ethernet_header = ""
    IP_header = ""
    source_ip = IP
    IP_header = IP_header + source_ip + dest_ip
    source_mac = MAC
    print(dest_ip in LOCAL_ARP_TABLE)
    destination_mac = LOCAL_ARP_TABLE[dest_ip] 
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + message
    
    return packet


while True:
    message = input("Please insert the message you want to send: ")
    dest_ip = input("Please insert the destination: ")
    
    if dest_ip[2] == '2':
        send_local(wrap_packet_ip(message, dest_ip))
    else:
        send_out()
    