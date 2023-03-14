import socket
import time
import socket
import threading
import time

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

class ClientThread(threading.Thread):
    clients = []
    lock = threading.Lock()

    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        print(f"Connected by {self.addr}")

    def run(self):
        with ClientThread.lock:
            ClientThread.clients.append(self)

        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            recieved = data.decode()
            print(recieved)
            for player in playerList:
                #print(player.ip, self.addr[0])
                if player.ip == self.addr[0]:
                    for recieve in recieved.split():
                        print(recieve)
                        if recieve == "fire":
                            #print("Shot")
                            player.shot()
                            print(player.getStrings())
            #self.conn.sendall(data)
            #self.conn.send(b"Test\n")

        with ClientThread.lock:
            ClientThread.clients.remove(self)

        print(f"Disconnected from {self.addr}")
        self.conn.close()
        del self

class BroadcastThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            with ClientThread.lock:
                for client in ClientThread.clients:
                    #print(client.addr)
                    for player in playerList:
                        #print(player.ip, client.addr[0])
                        if player.ip == client.addr[0]:
                            string = player.getStrings() + "\n"
                            #print(string)
                            client.conn.send(string.encode())

            time.sleep(3)

class Player:
    def __init__(self, ip, team, lives, ammo):
        self.team = team
        self.lives = lives
        self.ammo = ammo
        self.score = 0
        self.ip = ip

    def killed(self):
        self.lives -= 1
        self.score -= 5

    def shot(self):
        self.ammo -= 1

    def kill(self):
        self.score += 10

    def getStrings(self):
        one = f"Health: {self.lives} Ammo:{self.ammo},Points: {self.score}"
        return one

    def sendData(self, sock, UDP1):
        one = self.getStrings()
        sock.sendto(one.encode(), (self.ip, UDP1))
        return sock

    def recive(self, sock, UDP, timeout=0.1):
        sock.settimeout(timeout)
        try:
            data, address = sock.recvfrom(UDP)
            if address[0] == self.ip:
                data = data.decode("utf-8")
                print(address)
            else:
                data = ''
        except socket.timeout:
            data = ""
        return data

player1 = Player("10.2.94.142", "Blue", 5, 20)
player2 = Player("10.2.94.205", "Red", 5, 20)
playerList = [player1, player2]

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        client_thread = ClientThread(conn, addr)
        client_thread.start()

    # Start broadcast thread after accepting first client
    if len(ClientThread.clients) == 1:
        broadcast_thread = BroadcastThread()
        broadcast_thread.start()

