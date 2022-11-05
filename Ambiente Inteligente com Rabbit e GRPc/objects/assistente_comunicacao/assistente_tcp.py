#Arquivo referente a conexao com a aplicacao, desde inicializacao do servidor ate troca de mensagens

import socket
import threading
from generated import object_pb2

FORMAT = 'UTF-8'
class HomeAssistantTCP():
    #Inicializacao do servidor TCP
    def start_tcp(self, ip_server, port):
        endereco = (ip_server, port)
        #Conexao TCP
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Evitar erro por multiplas execucoes em pouco tempo
        servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor_socket.bind(endereco)
        servidor_socket.listen()

        print("Servidor On!")
        print("IP do Servidor: ", endereco)

        return servidor_socket
    
    #Estabelecendo conexao via TCP
    def connect_tcp(self, servidor_socket):
        #Fica em espera ate uma conexao ser estabelecida
        client, address = servidor_socket.accept()
        print("Conectado com {}".format(str(address)))
        client.send('Conectado ao servidor!'.encode(FORMAT))
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
            comando = message_decoded.split()
            try:
                #Envia a lista com todos os objetos conectados ao home assistant
                if comando[0] == 'request_list':
                    mensagem_resposta = f'{list(self.objects.keys())}'
                    client.send(mensagem_resposta.encode(FORMAT))
                #Comando para desconectar a aplicacao do home assistant
                elif comando[0] == 'exit':
                    print("Desconectando da aplicação....")
                    client.close()
                    print("A aplicação foi desconectada!")
                    del client  #Nao sei se precisa, testar depois
                    break

                #Abaixo sao os comandos para se comunicar via gRPC com os objetos para
                #obter o requisitado pela aplicacao

                #Mudar o status para ligado de algum objeto
                elif comando[1] == 'set_status_on':
                    objeto_selecionado = self.objects[comando[0]]
                    mensagem_resposta = objeto_selecionado.On(object_pb2.Empty())
                    client.send(f'Objeto com status definido para {mensagem_resposta}'.encode(FORMAT))
                #Mudar o status para desligado de algum objeto
                elif comando[1] == 'set_status_off':
                    objeto_selecionado = self.objects[comando[0]]
                    mensagem_resposta = objeto_selecionado.Off(object_pb2.Empty())
                    client.send(f'Objeto com status definido para False'.encode(FORMAT))
                #Mudar o valor de algum atributo (se existir) do objeto desejado
                elif comando[1] == 'set_attribute':
                    objeto_selecionado = self.objects[comando[0]]
                    mensagem_resposta = objeto_selecionado.SetAttribute(object_pb2.NewAttribute(value = float(comando[2])))
                    client.send(f'Objeto com atributo definido para {mensagem_resposta}'.encode(FORMAT))
                #Retornar todo o status do objeto desejado
                elif comando[1] == 'request_status':
                    object_data = self.objects_data[comando[0]]
                    client.send(object_data.encode(FORMAT))
            #Se o comando recebido nao for nenhum dos validos
            except:
                mensagem_resposta = 'Comando Inválido... Tente novamente! =D'
                client.send(mensagem_resposta.encode(FORMAT))