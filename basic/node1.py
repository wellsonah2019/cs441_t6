import socket

IP = '0x1A'
MAC = 'N1'

def send_local(packet):
    pass

def send_out(packet):
    pass

def wrap_packet_ip(message, dest_ip):
    pass

while True:
    message = input("Please insert the message you want to send: ")
    dest_ip = input("Please insert the destination: ")
    if dest_ip[2] == '2':
        send_local(wrap_packet_ip(message, dest_ip))
    else:
        send_out(wrap_packet_ip(message, dest_ip))