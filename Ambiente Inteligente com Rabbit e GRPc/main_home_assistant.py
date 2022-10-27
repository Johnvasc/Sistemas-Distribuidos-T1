from objects.home_assistant import HomeAssistant
#from generated import object_pb2_grpc
#from generated import object_pb2
#import time
import socket

home_assistant = HomeAssistant()
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