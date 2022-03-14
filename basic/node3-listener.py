import socket
import sys
import subprocess as sp

extProc = sp.Popen(['python','node3.py']) # runs myPyScript.py 

IP = '0x2B'
MAC = 'N3'

cable = ("localhost", 8200) 
node3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node3.bind(("localhost", 8003))

def log_protocol(source_ip, source_mac, message):
    with open('node3.log', 'a') as file:
        file.write("\nSOURCE IP: " + source_ip + '\nSOURCE MAC: ' + source_mac + '\n' + 'MESSAGE: ' + message + '\n\n')
 
while True:
    received_message, address = node3.recvfrom(1024)
    if received_message:
        received_message = received_message.decode("utf-8")
        source_mac = received_message[0:2]
        destination_mac = received_message[2:4]
        source_ip = received_message[4:8]
        destination_ip =  received_message[8:12]
        protocol = received_message[12:13]
        data_length = received_message[13:16]
        message = received_message[16:]
        protocol = int(protocol)
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
                sp.Popen.terminate(extProc)
                sys.exit()
        else:
            print("Packet received, but it ain't for u.")