# import socket
# from datetime import datetime

# server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# global FIREWALL_RULE_N3 
# FIREWALL_RULE_N3 = {
#     "allow": [],
#     "deny": []
# }

def resetfwall():
  open('firewall.txt', 'w').close()

def writefwall(ip):
  with open("firewall.txt", "a+") as f:
    f.write(ip + "\n")
  
def getfwall():
  data = [line.strip() for line in open("firewall.txt", 'r')]
  return data
