import socket
import sys
import subprocess as sp
from timestamp import timestamp

extProc = sp.Popen(['python','node1.py']) # runs myPyScript.py 

status = sp.Popen.poll(extProc) # status should be 'None'

print(status)
# sp.Popen.terminate(extProc) # closes the process

# status = sp.Popen.poll(extProc) # status should now be something other than 'None' ('1' in my testing)
IP = '0x1A'
MAC = 'N1'

LOCAL_ARP_TABLE = {
    "0x11": "R1",
    "0x1A": "N1"
}

node1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node1.bind(("localhost", 8001))

def reply_ping(packet):
    node1.sendto(bytes(packet, "utf-8"), ("localhost", 8101))

def log_protocol(source_ip, source_mac, message):
    with open('node1.log', 'a') as file:
        file.write("\nSOURCE IP: " + source_ip + '\nSOURCE MAC: ' + source_mac + '\n' + 'MESSAGE: ' + message + '\n\n')

def wrap_packet_ip(message, dest_ip, protocol):
    ethernet_header = ""
    IP_header = ""
    source_ip = IP
    IP_header = IP_header + source_ip + dest_ip
    source_mac = MAC
    protocol = protocol
    data = message + 'r'
    data_length = str(len(message))

    if len(data_length) == 2:
        data_length = '0' + data_length
    elif len(data_length) == 1:
        data_length = '00' + data_length

    if dest_ip in LOCAL_ARP_TABLE:
        destination_mac = LOCAL_ARP_TABLE[dest_ip] 
    else:
        destination_mac = 'R1'
    ethernet_header = ethernet_header + source_mac + destination_mac
    packet = ethernet_header + IP_header + protocol + data_length + data
    
    return packet
 
while True:
    received_message, addr = node1.recvfrom(1024)
    received_message = received_message.decode("utf-8")
    source_mac = received_message[0:2]
    destination_mac = received_message[2:4]
    ip_source = received_message[4:8]
    destination_ip =  received_message[8:12]
    protocol = received_message[12:13]
    data_length = received_message[13:16]
    message = received_message[16:]
    protocol = int(protocol)
    if IP == destination_ip and MAC == destination_mac:
        if protocol == 3:
            print("-----------" + timestamp() + "-----------")
            print("\nThe packet received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
            print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
            print("\nData Length: " + data_length)
            print("\nMessage: " + message)
            print("----------------------------------")
        elif protocol == 0:
            reply_ping(wrap_packet_ip(message, ip_source, str(protocol)))
            print(message)
        elif protocol == 1:
            log_protocol(ip_source, source_mac, message)
        elif protocol == 2:
            print("Kill protocol has been given. Will exit now...")
            sp.Popen.terminate(extProc)
            sys.exit()
    else:
        print("-----------" + timestamp() + "-----------")
        print("\nThe packet received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
        print("\nSource IP address: {ip_source}, Destination IP address: {destination_ip}".format(ip_source=ip_source, destination_ip=destination_ip))
        print("\nProtocol: " + str(protocol))
        print("\nData Length: " + data_length)
        print("\nMessage: " + message)    
        print()
        print("PACKET NOT FOR ME. DROPPING NOW...")
        print("---------------------------------")