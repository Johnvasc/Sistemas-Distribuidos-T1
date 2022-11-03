
from objects.home_assistant import HomeAssistant
import socket

#Definicao do "objeto" Home assistant
home_assistant = HomeAssistant()

#Estabelecendo conexao via RabbitMQ
connection, channel = home_assistant.connect_rabbit()

#Iniciar a fila principal (home) no RabbitMQ e criar a conexao via gRPC
home_assistant.start_principal_queue()
#Iniciar a fila de objetos que se desconectaram
home_assistant.start_end_queue()

#IP do servidor TCP
ip_server = 'localhost'
#ip_server = socket.gethostbyname(socket.gethostname())
#Porta do servidor TCP
porta_tcp = 12345
#Inicializacao do servidor para comunicacao com a aplicacao
home_assistent_socket = home_assistant.start_tcp(ip_server, porta_tcp)

while True:
    try:
        #Esperando alguma conexao (aplicacao)
        home_assistant.connect_tcp(home_assistent_socket)
    except KeyboardInterrupt:
        print('Conexao TCP finalizada!')
        home_assistent_socket.close()
        break