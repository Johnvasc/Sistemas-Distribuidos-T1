import socket

IP = "127.0.0.1"
PORT = 5000

print('Bem-vindo(a) à calculadora UDP! \n - Aperte X se quer sair \n - Insira os valores de A e B e a operação a ser realizada.')

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:

    print('Insira o 1o valor')
    a = input()

    print('Insira o 2o valor')
    b = input()

    print('Insira o operador, + para soma, - para subtração, * para multiplicação e / para divisão:')
    operator = input()



    message = a +', '+b+', '+operator
    print('Mensagem recebida do servidor: ' + message + "\n")

    socket.sendto(message.encode('utf-8'), (IP, PORT))
    if a == 'X' or b == 'X' or operator == 'X':
        break

    data, address = socket.recvfrom(2048)
    text = data.decode('utf-8')
    print('RESULTADO DA OPERAÇÃO %s : %s ' % (address, text) + "\n")

print('Connection Closed')
socket.close()