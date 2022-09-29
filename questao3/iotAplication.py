import socket

PORT = 6789
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg = 'iotAplication'
s.sendall(bytes(msg, 'utf-8'))
while True:
    data = s.recv(1024).decode('utf-8')
    if not data:
        s.close()
        break 
    print(data)