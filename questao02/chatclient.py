import socket
import threading

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

print('Conectado ao servidor!')

class Cliente():

    nick = input('Choose a nickname: ')

    # Ja que o usuario chegou até aqui, o host e port podem ser fixos
    def __init__(self, host='localhost', port=12345):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((str(host), int(port)))
        self.nickname = self.nick.encode('utf-8')

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.daemon = True
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.daemon = True
        write_thread.start()

    def receive(self):
        while True:
            try:
                #print('aaa')
                message = self.client.recv(1024).decode('utf-8')
                #print('bbb')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))

                else:
                    print(message)
            except:
                print('And error occurred!')
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            if message:
                if message == '/SAIR':
                    self.client.send(message.encode('utf-8'))
                    print('Sessão encerrada!')
                    self.client.close()
                    exit()    
                else:        
                    self.client.send(message.encode('utf-8'))

client = Cliente()