import socket



HOST = "10.2.94.207"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b"Hello, WOrld")
    data = s.recv(1024)

print(f"Recieved: {data!r}")