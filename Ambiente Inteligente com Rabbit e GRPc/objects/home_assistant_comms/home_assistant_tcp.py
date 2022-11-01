#Arquivo referente a conexao com a aplicacao, desde inicializacao do servidor ate troca de mensagens

import socket
import threading
from generated import object_pb2

FORMAT = 'UTF-8'
class HomeAssistantTCP():
    #Inicializacao do servidor TCP
    def start_tcp(self, ip_server, port):
        ADDR = (ip_server, port)
        #Conexao TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Evitar erro por multiplas execucoes em pouco tempo
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(ADDR)
        server_socket.listen()

        print("Server On!")
        print("IP's Server: ", ADDR)

        return server_socket
    
    #Estabelecendo conexao via TCP
    def connect_tcp(self, server_socket):
        #Fica em espera ate uma conexao ser estabelecida
        client, address = server_socket.accept()
        print("Connected with {}".format(str(address)))
        client.send('Connected to server!'.encode(FORMAT))
        #Cria uma thread para cuidar dessa nova conexao
        thread = threading.Thread(target = self.handle, args = (client,), daemon = True)
        thread.start()
    
    #Funcao (em uma thread) para cuidar das requisicoes da aplicacao
    def handle(self, client):
        while True:
            #Recebimento de uma mensagem (requisicao)
            message = client.recv(1024)
            message_decoded = message.decode(FORMAT)
            #Dividir o conteudo da mensagem por informacao se possivel
            command = message_decoded.split()
            try:
                #Envia a lista com todos os objetos conectados ao home assistant
                if command[0] == 'request_list':
                    response_msg = f'{list(self.objects.keys())}'
                    client.send(response_msg.encode(FORMAT))
                #Comando para desconectar a aplicacao do home assistant
                elif command[0] == 'exit':
                    print("Desconectando aplicação....")
                    client.close()
                    print("Aplicação desconectada!")
                    del client  #Nao sei se precisa, testar depois
                    break

                #Abaixo sao os comandos para se comunicar via gRPC com os objetos para
                #obter o requisitado pela aplicacao

                #Mudar o status para ligado de algum objeto
                elif command[1] == 'set_status_on':
                    selected_object = self.objects[command[0]]
                    response_msg = selected_object.On(object_pb2.Empty())
                    client.send(f'Objeto com status definido para {response_msg}'.encode(FORMAT))
                #Mudar o status para desligado de algum objeto
                elif command[1] == 'set_status_off':
                    selected_object = self.objects[command[0]]
                    response_msg = selected_object.Off(object_pb2.Empty())
                    client.send(f'Objeto com status definido para False'.encode(FORMAT))
                #Mudar o valor de algum atributo (se existir) do objeto desejado
                elif command[1] == 'set_attribute':
                    selected_object = self.objects[command[0]]
                    response_msg = selected_object.SetAttribute(object_pb2.NewAttribute(value = float(command[2])))
                    client.send(f'Objeto com atributo definido para {response_msg}'.encode(FORMAT))
                #Retornar todo o status do objeto desejado
                elif command[1] == 'request_status':
                    object_data = self.objects_data[command[0]]
                    client.send(object_data.encode(FORMAT))
            #Se o comando recebido nao for nenhum dos validos
            except:
                response_msg = 'Comando Inválido... Tente novamente! =D'
                client.send(response_msg.encode(FORMAT))