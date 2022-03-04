import socket

IP = '0x1A'
MAC = 'N1'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


LOCAL_ARP_TABLE = {
    "0x11": "R1",
    "0x1A": "N1"
}
def send_local(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8001))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8101))

def send_out(packet):
    pass

def wrap_packet_ip(message, dest_ip):
    ethernet_header = ""
    IP_header = ""
    source_ip = IP
    IP_header = IP_header + source_ip + dest_ip
    source_mac = MAC
    
    if dest_ip in LOCAL_ARP_TABLE:
        destination_mac = LOCAL_ARP_TABLE[dest_ip] 
    else:
        destination_mac = 'R1'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + message
    
    return packet


while True:
    message = input("Please insert the message you want to send: ")
    dest_ip = input("Please insert the destination: ")
    
    send_local(wrap_packet_ip(message, dest_ip))
    
    