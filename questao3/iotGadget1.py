import socket
import random
import time

PORT = 6789
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg = 'iotGadget'
s.sendall(bytes(msg, 'utf-8'))
print("teste")
while True:
    temp = random.randrange(30, 40)
    msg = f"temperatura: {temp}º ceusius"
    print(msg)
    s.sendall(bytes(msg, 'utf-8'))
    time.sleep(5)
