import socket
import operator

# 'Converts' the string operator into a real operator

IP = "127.0.0.1"
PORT = 5000

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((IP, PORT))

print('Server Listening At {}'.format(socket.getsockname()))

def valorinteiro(v):
  n = int(v)
  m = v * 10
  s = n * 10
  if m == s:
    return True
  else:
    return False

while True:
    messageBytes, address = socket.recvfrom(2048)
    messageString = messageBytes.decode('utf-8')
    print('Recebido do cliente {} : {}'.format(address, messageString))

    k = messageString
    if k=='sair':
        break
    messageString = messageString.split(", ")
    
    a = messageString[0]
    b = messageString[1]
    operator = messageString[2]

    if a == 'X' or b == 'X' or operator == 'X':
        break

    if operator == '+':
        print("soma")
        result = float(a) + float(b)
        if (valorinteiro(result) == True):
            result = int(result)
        print("Resultado:", result)

    elif operator == '-':
        print("subtração")
        result = float(a) - float(b)
        if (valorinteiro(result) == True):
            result = int(result)
        print("Resultado:", result)
    
    elif operator == '*':
        print("multiplicação")
        result = float(a) * float(b)
        if (valorinteiro(result) == True):
            result = int(result)
        print("Resultado:", result)
    
    elif operator == '/':
        print("divisão")
        result = float(a) / float(b)
        if (valorinteiro(result) == True):
            result = int(result)
        print("Resultado:", result)


    socket.sendto(str(result).encode(), address)
    
print('Conexão Fechada')
socket.close()