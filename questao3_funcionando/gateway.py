import socket
import time
import threading
import messages_pb2 as messages_pb2

from multicast.send_group import send_multicast 

IP = socket.gethostbyname(socket.gethostname())
PORT = 37020
ADDR = (IP, PORT)
FORMAT = "utf-8"

ADDR_APP = ('192.168.1.103', 5555)
socket_app = []

clients_types = []
clients = []
ac_info = ''

def start_server():
    server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_tcp_socket.bind(ADDR)
    server_tcp_socket.listen()
    print("Gateway On!\n")
    return server_tcp_socket

def send_gateway_address():
    message = f"{IP} {PORT}"
    send_multicast(message)

def send_command_to_object(client_index, message):
    clients[client_index].send(message.encode(FORMAT))

def handle(client):    
    while True:
        try:
            answer = messages_pb2.GatewayMessage()
            answer.response_type = messages_pb2.GatewayMessage.MessageType.GET

            message = client.recv(1024)
            message_decoded = message.decode(FORMAT)

            if message_decoded.split()[0] == 'acinfo':
                global ac_info 
                ac_info = f"AC {message_decoded.split()[1]} {message_decoded.split()[2]}"
                print(ac_info)

            elif message_decoded.split()[0] == 'lampinfo' or message_decoded.split()[0] == 'sprinklerinfo':
                info = message_decoded
                print(info)
                
                iobject = answer.object.add()
                iobject.type = message_decoded.split()[0]
                iobject.status = info.split()[1]

                answer_serialized = answer.SerializeToString()
                socket_app[0].send(answer_serialized)

            else:
                answer = 'Return of gateway: You are connected by TCP\n'
                client.send(answer.encode(FORMAT))

        except Exception as e:
            print(e)
            client.close()
            break

def return_sensors(client, request_object):
    answer = messages_pb2.GatewayMessage()
    answer.response_type = messages_pb2.GatewayMessage.MessageType.GET

    if request_object == "AC":
        info = ac_info

    iobject = answer.object.add()
    iobject.type = info.split()[0]
    iobject.temp = int(info.split()[1])
    iobject.status = info.split()[2]

    answer_serialized = answer.SerializeToString()
    socket_app[0].send(answer_serialized)

def return_list_object(client):
    answer = messages_pb2.GatewayMessage()
    answer.response_type = messages_pb2.GatewayMessage.MessageType.LIST
    
    for o in clients_types:
        iobject = answer.object.add()
        iobject.type = o

    answer_serialized = answer.SerializeToString()

    client.send(answer_serialized)

def request_object_status(client, consulted_object):

    iobject = consulted_object
    for i in range(0, len(clients_types)):
        if clients_types[i] == iobject:
            if iobject == "AC":
                return_sensors(client, iobject)
            else:
                send_command_to_object(i , f"request_status")

def set_object_status(client, args):
    iobject, new_status = args.split()[0], args.split()[1]

    for i in range(0, len(clients_types)):
        if clients_types[i] == iobject:
            send_command_to_object(i , f"set_status {new_status}")

def set_object_attributes(client, args):
    iobject, changed_attribute, new_value = args.split()[0], args.split()[1], args.split()[2]

    for i in range(0, len(clients_types)):
        if clients_types[i] == iobject:
            send_command_to_object(i , f"set_{changed_attribute} {new_value}")

def application_handle(client):
    while True:
        try:
            print("Waiting application's messages")
            message = client.recv(1024)
            message_decoded = messages_pb2.ApplicationMessage()
            message_decoded.ParseFromString(message)
            
            if message_decoded.type == 1:
                if message_decoded.command == 'list_objects':
                    return_list_object(client)
                elif message_decoded.command == 'request_status':
                    request_object_status(client, message_decoded.args)
                elif message_decoded.command == 'set_status':
                    set_object_status(client, message_decoded.args)
                elif message_decoded.command == 'set_attributes':
                    set_object_attributes(client, message_decoded.args)
                else:
                    pass
        except Exception as e:
            print(e)
            client.close()
            break
                    
def connect_client_by_tcp(server_tcp_socket):
    print("Waiting TCP's connections...\n")
    
    while True:
        try:
            client, address = server_tcp_socket.accept()
            #print(address)

            # encaminhamento para a thread que irá lidar com as requisições da applicação ou para a thread dos objetos
            if address == ADDR_APP: 
                socket_app.append(client)
                application_thread = threading.Thread(target=application_handle, args=(client,))
                application_thread.start()
            else:
                # registra os clientes antes de iniciar a thread
                client_type = client.recv(1024).decode(FORMAT)
                
                clients_types.append(client_type)
                clients.append(client)
            
                print("Connected to {}\n".format(str(address)))

                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
        except Exception as e:
            print(e)

server_tcp_socket = start_server()
send_gateway_address()
connect_client_by_tcp(server_tcp_socket)