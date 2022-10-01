import socket

PORT = 6789
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg = 'iotAplication'
s.sendall(bytes(msg, 'utf-8'))
i = 0
while True:
    data = s.recv(1024).decode('utf-8')
    if not data:
        s.close()
        break 
    print(data)
    i += 1
    if i == 10:
        print('deseja cortar alguma conexao?')
        escolha = input("1 - Sim\n2 - Nao")
        if escolha == 'Sim':
            end = input('insira o endereco da aplicacao')
            msg = f'des_{end}'
            s.sendall(bytes(msg, 'utf-8'))