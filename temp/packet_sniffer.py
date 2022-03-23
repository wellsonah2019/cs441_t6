import socket

# the public network interface
# HOST = socket.gethostbyname(socket.gethostname())
# host = socket.socket(socket.AF_CAN, socket.SOCK_DGRAM)
# HOST = socket.gethostbyname(socket.gethostname())

# s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# s.bind((HOST, 0))


while True:
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    packet = s.recvfrom(65565)
    print(packet)

    # s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # print(s.recvfrom(65565))

    # s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
# HOST = socket.gethostbyname(socket.gethostname())

# # create a raw socket and bind it to the public interface
# s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
# s.bind((HOST, 0))

# # Include IP headers
# s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# # receive all packages
# s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# # receive a package
# print(s.recvfrom(65565))

# # disabled promiscuous mode
# s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)