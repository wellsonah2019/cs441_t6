import socket
from datetime import datetime
from timestamp import date_time

IP = '0x1A'
MAC = 'N1'
TCP_PORT = 8011 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", TCP_PORT))

#limit of the queue, i.e., how many pending connections can be stored in the queue.
# If the queue is full, further connection requests will be dropped
server.listen(5)

conn, addr = server.accept()
from_client = ''

data = conn.recv(30)
print(type(data))

data = data.decode('utf-8')

from_client += data
print(from_client)

msg = "Hello from server"
conn.send(msg.encode('utf-8'))
print("[INFO] Data sent successfully to Client")

conn.close()
print('client disconnected')
server.close()
print('socket disconnected')
