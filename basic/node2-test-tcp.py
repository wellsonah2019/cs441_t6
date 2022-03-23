import socket
from datetime import datetime
from timestamp import date_time

IP = '0x2A'
MAC = 'N2'
TCP_PORT = 8011

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect the client to the TCP port on which our server is running
client.connect(("localhost",TCP_PORT))

msg = "Hello from client"
msg = msg.encode('utf-8')

print("[INFO] Sending data to Server...")
client.send(msg)
print("[INFO] Data sent successfully to Server")

print("[INFO] Receiving Data from server")
data = client.recv(30)
data = data.decode('utf-8')

print('[INFO] Data received from Server : ',data)

client.close()