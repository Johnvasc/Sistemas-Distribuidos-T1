
from objects.home_assistant import HomeAssistant
import socket

#Definicao do "objeto" Home assistant
home_assistant = HomeAssistant()

#Estabelecendo conexao via RabbitMQ
connection, channel = home_assistant.connect_rabbit()

home_assistant.start_principal_queue()
home_assistant.start_end_queue()

ip_server = socket.gethostbyname(socket.gethostname())
home_assistent_socket = home_assistant.start_tcp(ip_server, 12356)

while True:
    try:
        home_assistant.connect_tcp(home_assistent_socket)
    except KeyboardInterrupt:
        home_assistent_socket.close()
        break