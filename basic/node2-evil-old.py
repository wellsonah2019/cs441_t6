import socket

IP = '0x2A'
MAC = 'N2'
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


LOCAL_ARP_TABLE = {
    "0x21": "R2",
    "0x2A": "N2",
    "0x2B": "N3"
}
def send_local(packet):
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8102))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8002))
    server.sendto(bytes(packet, "utf-8"), ("localhost", 8003))


def wrap_packet_ip(message, dest_ip, source_ip = IP):
    ethernet_header = ""
    IP_header = ""
    source_ip = source_ip
    IP_header = IP_header + source_ip + dest_ip
    source_mac = MAC
    if dest_ip in LOCAL_ARP_TABLE:
        destination_mac = LOCAL_ARP_TABLE[dest_ip] 
    else:
        destination_mac = 'N1'
    print(destination_mac)
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + message
    
    return packet


while True:
    message = input("Please insert the message you want to send: ")
    dest_ip = input("Please insert the destination: ")
    source_ip = input("[Evil mode] Please insert the source IP to spoof: ")
    
    
    send_local(wrap_packet_ip(message, dest_ip, source_ip))
    
    
    
    