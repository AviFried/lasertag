# ref:
# https://wiki.python.org/moin/UdpCommunication
import socket

#UDP_IP = "127.0.0.1"
#UDP_PORT = 5005
import time

UDP_IP = "192.168.7.249"
UDP_PORT = 2390
MESSAGE = b"ID Request"

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
recived = True
while recived:
    data = sock.recv(2390)
    print(data.decode("utf-8"))
    gunOneID = data.decode("utf-8")
    if type(data.decode("utf-8")) == str:
        recived = False

gunOneHealth = 100
gunOnePoints = 0
gunOneAmmo = 20
print("readyt")
while True:

    MESSAGE = b'Health: 55 Ammo: 27 Health: 55 Ammo: 27 Health: 55 Ammo: 27 Health: 55 Ammo: 27 Health: 55 Ammo: 27 Health: 55 Ammo: 27'
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    print("sent")
    time.sleep(1)




