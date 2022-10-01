import socket
import random
import time

PORT = 6789
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# mensagem de identificação do gadget ao servidor
s.connect((HOST, PORT))
msg = 'iotGadget'
s.sendall(bytes(msg, 'utf-8'))
#funcionamento do gadget de sensor contínuo, da temperaturas entre 30 e 40º ceusius e dorme por 5s
while True:
    temp = random.randrange(30, 40)
    msg = f"temperatura: {temp}º ceusius"
    print(msg)
    s.sendall(bytes(msg, 'utf-8'))
    time.sleep(5)
