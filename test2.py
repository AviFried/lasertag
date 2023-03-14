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
            print(data.decode(), self.addr)
            #self.conn.sendall(data)
            self.conn.send(b"Test\n")

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
                    print(client.addr)
                    for player in playerList:
                        if player.ip == client.addr[0]:
                            string = player.getStrings().encode()
                            client.conn.send(f"{string}\n")

            time.sleep(3)

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
