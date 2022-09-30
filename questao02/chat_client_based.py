from asyncio.windows_events import NULL
from pydoc import cli
import socket
import threading
import sys

command_join = input('Bem-vindo!\nSe quiser participar do chat, digite o comando /ENTRAR.\nComando: ')

while command_join != '/ENTRAR':
    print(f'{command_join} não é um comando válido, tente novamente!')
    command_join = input('Se quiser participar do chat, digite o comando /ENTRAR.\nComando: \n')

print('Ok, estamos quase lá...')

server_ip = input('Informe o ip do servidor: ')
server_port = input('Informe a porta do servidor: ')

while True:
    if (server_ip == 'localhost' or server_ip == '127.0.0.1') and int(server_port) == 12345:
        print(f'Servidor: {server_ip} na porta: {server_port} encontrado!')
        break
    else:
        if (server_ip != 'localhost' or server_ip != '127.0.0.1') and int(server_port) == 12345:
            print(f'Servidor não encontrado!\nFalha ao se conectar ao ip informado!\n')
            connect_resp = input('Usuário ainda quer tentar se conectar? S para sim N para não\nResposta: ')
            connect_resp = connect_resp.lower()
            if connect_resp == 's':
                server_ip = input('Informe o ip do servidor: ')
                server_port = input('Informe a porta do servidor: ')
            elif connect_resp == 'n':
                print('Entendo, até mais!')
                exit()
            else:
                print('Valor inválido, tente novamente!')
                connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                print(connect_resp)
                connect_resp = connect_resp.lower()
                print(connect_resp)
                while connect_resp != 's' and connect_resp != 'n':
                    print('Valor inválido, tente novamente!')
                    connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                    print(connect_resp)
                    connect_resp = connect_resp.lower()
                    print(connect_resp)
                if connect_resp == 's':
                    server_ip = input('Informe o ip do servidor: ')
                    server_port = input('Informe a porta do servidor: ')
                else:
                    print('Entendo, até mais!')
                    exit()
        elif (server_ip == 'localhost' or server_ip == '127.0.0.1') and int(server_port) != 12345:
            print(f'Servidor não encontrado!\nFalha ao se conectar pela porta informada!\n')
            connect_resp = input('Usuário ainda quer tentar se conectar? S para sim N para não\nResposta: ')
            connect_resp = connect_resp.lower()
            if connect_resp == 's':
                server_ip = input('Informe o ip do servidor: ')
                server_port = input('Informe a porta do servidor: ')
            elif connect_resp == 'n':
                print('Entendo, até mais!')
                exit()
            else:
                print('Valor inválido, tente novamente!')
                connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                connect_resp = connect_resp.lower()
                while connect_resp != 's' and connect_resp != 'n':
                    print('Valor inválido, tente novamente!')
                    connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                    connect_resp = connect_resp.lower()
                if connect_resp == 's':
                    server_ip = input('Informe o ip do servidor: ')
                    server_port = input('Informe a porta do servidor: ')
                else:
                    print('Entendo, até mais!')
                    exit()
        else:
            print(f'Servidor não encontrado!\nip e porta inválidos!\n')
            connect_resp = input('Usuário ainda quer tentar se conectar? S para sim N para não\nResposta: ')
            connect_resp = connect_resp.lower()
            if connect_resp == 's':
                server_ip = input('Informe o ip do servidor: ')
                server_port = input('Informe a porta do servidor: ')
            elif connect_resp == 'n':
                print('Entendo, até mais!')
                exit()
            else:
                print('Valor inválido, tente novamente!')
                connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                connect_resp = connect_resp.lower()
                while connect_resp != 's' and connect_resp != 'n':
                    print('Valor inválido, tente novamente!')
                    connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                    connect_resp = connect_resp.lower()
                if connect_resp == 's':
                    server_ip = input('Informe o ip do servidor: ')
                    server_port = input('Informe a porta do servidor: ')
                else:
                    print('Entendo, até mais!')
                    exit()

print('Conectado ao servidor!\n')

nickname = input('Choose a nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((str(server_ip), int(server_port)))

stop_thread = 0

def receive():
    global stop_thread
    while True:
        if stop_thread == 1:
            break
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            elif message == 'Desconectado!':
                print(message)
                stop_thread = 1
                client.close()
                break
            else:
                print(message)
        except:
            print('Houve um erro no recebimento de mensagens!') #NAO DA CERTO
            stop_thread = 1
            client.close()
            break

def write():
    global stop_thread
    while True:
    #PODE COLOCAR UM TRY EXCEPT AQUI COM UM BREAK NO EXCEPT
        if stop_thread == 1:
            break
        #message = input('~> ')
        #msg_format = f'~> {nickname}: {message}'
        #if message[0] == '/':
        #    client.send(message.encode('utf-8'))
        #else:
        #    print(msg_format)    
        #    client.send(msg_format.encode('utf-8'))
        text = input('')
        if text[0] == '/':
            client.send(text.encode('utf-8'))
        else:
            message = '{}: {}'.format(nickname, text)
            client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
#receive_thread.daemon = True
receive_thread.start()
write_thread = threading.Thread(target=write)
#write_thread.daemon = True
write_thread.start()
