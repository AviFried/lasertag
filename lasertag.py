import socket

#UDP_IP = "127.0.0.1"
#UDP_PORT = 5005
import time

UDP_IP1 = "192.168.7.249"
UDP_IP2 ="192.168.7.249"
UDP_PORT = 2390
UDP_PORT2 = 2380
UDP_PORT3 = 2370
unit1_1 = b"Health:200Ammo:10"
unit1_3 = b"Points:   200"
unit2_1 = b"Health:300Ammo:10"
unit2_3 = b"Points:   500"
unit1_2 = b"setup"
unit2_2 = b"setup"
unit1_Ammmo = 15
print("UDP target IP: %s" % UDP_IP1)
print("UDP target port: %s" % UDP_PORT)
print("unit1_1: %s" % unit1_1)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(unit1_1, (UDP_IP1, UDP_PORT))
sock.sendto(unit2_1, (UDP_IP2, UDP_PORT))
data = sock.recv(UDP_PORT)
print(data.decode("utf-8"))
time.sleep(1)
sock.sendto(unit1_3, (UDP_IP1, UDP_PORT3))
sock.sendto(unit2_3, (UDP_IP2, UDP_PORT3))
data = sock.recv(UDP_PORT3)
print(data.decode("utf-8"))
time.sleep(1)
sock.sendto(unit1_2, (UDP_IP1, UDP_PORT2))
sock.sendto(unit2_2, (UDP_IP2, UDP_PORT2))
data = sock.recv(UDP_PORT3)
print(data.decode("utf-8"))
time.sleep(1)

while True:
    data = sock.recv(UDP_PORT2)
    recieved = data.decode("utf-8")
    print(recieved)
    if recieved == "fire":
        unit1_Ammmo-= 1
        unit1_1 = f'Health:200Ammo:{unit1_Ammmo}'
        sock.sendto(unit1_1.encode(), (UDP_IP1, UDP_PORT))
