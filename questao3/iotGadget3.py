import socket

PORT = 6789
HOST = 'localhost'
isOn = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# mensagem de identificação do gadget ao servidor
s.connect((HOST, PORT))
msgS = s.recv(1024).decode('utf-8')
print(msgS)
msg = 'iotGadget_ID:4567_TY:Actv_NA:LampadaInteligente'
s.sendall(bytes(msg, 'utf-8'))
#funcionamento do gadget de sensor contínuo, da umidade entre 60 e 70% e dorme por 8s
while True:
    print(f'status atual: {isOn}')
    data = s.recv(1024).decode('utf-8')
    if data[0:3] == 'gon':
        isOn = True
        msg = 'actv_4567_True'
    elif data[0:3] == 'gof':
        isOn = False
        msg = 'actv_4567_False'
    s.sendall(bytes(msg, 'utf-8'))