import socket
import re

IP = "127.0.0.1"
PORT = 5000

print('Bem-vindo(a) à calculadora UDP! \n - Aperte X se quer sair \n - Insira os valores de A e B e a operação a ser realizada.')

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:

    print('Insira o 1o valor')
    a = input()

    if(a == 'X' or a == 'x'):
        message = 'sair'
        socket.sendto(message.encode('utf-8'), (IP, PORT))
        break

    while True:
        try:
            float(a)
        
        except ValueError:
            # Not a valid number
            print("\nO valor deve ser um número!\n")
            a = input("Insira o 1o valor: ")
        else:
            break
    
    if(a == 'X' or a == 'x'):
        message = 'sair'
        socket.sendto(message.encode('utf-8'), (IP, PORT))
        break


    print('Insira o 2o valor')
    b = input()

    if(b == 'X' or b == 'x'):
        message = 'sair'
        socket.sendto(message.encode('utf-8'), (IP, PORT))
        break

    while True:
        try:
            float(b)
        
        except ValueError:
            # Not a valid number
            print("\nO valor deve ser um número!\n")
            b = input("Insira o 2o valor: ")
        else:
            break
    
    if(b == 'X' or b == 'x'):
        message = 'sair'
        socket.sendto(message.encode('utf-8'), (IP, PORT))
        break

    print('Insira o operador, + para soma, - para subtração, * para multiplicação e / para divisão:')
    operator = input()

    if(operator == 'X' or operator == 'x'):
        message = 'sair'
        socket.sendto(message.encode('utf-8'), (IP, PORT))
        break

    while(operator!='+' and operator!='-' and operator!='*' and operator!='/'):
        operator = input('\n O operador digitado não é valido. \n Insira o operador, + para soma, - para subtração, * para multiplicação e / para divisão:')

    if(operator == 'X' or operator == 'x'):
        message = 'sair'
        socket.sendto(message.encode('utf-8'), (IP, PORT))
        break

    message = a +', '+b+', '+operator
    print('Mensagem recebida do servidor: ' + message + "\n")

    socket.sendto(message.encode('utf-8'), (IP, PORT))
   

    data, address = socket.recvfrom(2048)
    text = data.decode('utf-8')
    print('RESULTADO DA OPERAÇÃO %s : %s ' % (address, text) + "\n")

print('Connection Closed')
socket.close()