import socket
import threading
import sys

#clientes_online = {}
class Servidor():
    def __init__(self, host='localhost', port=12345):

        # Todo servidor criada tem sua propria lista de clientes
        self.clientes_atuais = [] 
        self.nicknames = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((str(host), int(port)))
        self.server.listen(5)
        print('Server is listening...')

        receive_clients = threading.Thread(target=self.receive)
        receive_clients.daemon = True
        receive_clients.start()
        handle_clients = threading.Thread(target=self.handle)
        handle_clients.daemon = True
        handle_clients.start()

        while True:
            message = input('/> ')
            if message == 'close':
                self.server.close()
                sys.exit()
            else:
                pass

    def broadcast(self, message):
        for client in self.clientes_atuais:
            client.send(message)

    def msg_solo(self, msg, client):
        try:
            client.send(msg)
        except:
            self.clientes_atuais.remove(client)

    def leave_chat(self, client):
        index = self.clientes_atuais.index(client)
        self.clientes_atuais.remove(client)
        client.close()
        nickname = self.nicknames[index]
        self.broadcast(f'{nickname} left the chat!'.encode('utf-8'))
        self.nicknames.remove(nickname)

    #Não sei se precisa entrar com client tambem (nem pode kk)
    def handle(self):
        while True:
            if len(self.clientes_atuais) > 0:
                for client in self.clientes_atuais:
                    try:
                        message = client.recv(1024).decode('utf-8')
                        if message:
                            msg_client = message.split('/')
                            if len(msg_client) > 1:
                                if msg_client[1] == 'USUARIOS':
                                    msg_online = 'Mensagem do Servidor!\nUsuarios onlines:\n'
                                    #Depois posso tentar por a parte dos online
                                    for on in self.clientes_atuais:
                                        print(self.clientes_atuais[on])
                                        msg_online += "{} \n".format(str(self.clientes_atuais[on][0]))
                                    print(msg_online)
                                    self.msg_solo(msg_online,client)
                                elif msg_client[1] == 'SAIR':
                                    self.leave_chat(client)
                                else:
                                    wrong_msg = "Comando invalido.\nComandos válidos: /USUARIOS\n/SAIR\n"
                                    print(wrong_msg)
                                    client.send(wrong_msg)
                        else:
                            msg_chat = message.decode('utf-8')
                            self.broadcast(msg_chat)
                        
                    except:
                        index = self.clientes_atuais.index(client)
                        self.clientes_atuais.remove(client)
                        client.close()
                        nickname = self.nicknames[index]
                        self.broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                        self.nicknames.remove(nickname)
                        break

    def receive(self):
        print('Pronto para receber os usuários!')
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')
            #client.send('NICK'.encode('utf-8'))
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clientes_atuais.append(client)

            print(f'Nickname of the client is {nickname}')
            self.broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
            client.send('Connected to the server!'.encode('utf-8'))

server = Servidor()