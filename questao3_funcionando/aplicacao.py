import socket
import threading
import messages_pb2 as messages_pb2
import time

GATEWAY_IP = socket.gethostbyname(socket.gethostname())
GATEWAY_PORT = 37020
GATEWAY_ADDR = (GATEWAY_IP, GATEWAY_PORT)
FORMAT = 'utf-8'

IP_APP = socket.gethostbyname(socket.gethostname())
PORT_APP = 5555
ADDR_APP = (IP_APP, PORT_APP)

def receive(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            message_decoded = messages_pb2.GatewayMessage()
            message_decoded.ParseFromString(message)

            print(message_decoded)
        except Exception as e:
            print(e)
            client_socket.close()
            break

def write(client_socket, message):
    print("### Sending message")
    client_socket.send(message)

def request_list_objects(client_socket):
    command_message = messages_pb2.ApplicationMessage()
    command_message.type = messages_pb2.ApplicationMessage.MessageType.COMMAND
    command_message.command = "list_objects"

    print("### Serializing Message")
    serialized_message = command_message.SerializeToString()

    write(client_socket, serialized_message)
    print("### Message sent!")

    return None

def request_object_status(client_socket, consulted_object):
    command_message = messages_pb2.ApplicationMessage()
    command_message.type = messages_pb2.ApplicationMessage.MessageType.COMMAND
    command_message.command = "request_status"
    command_message.args = consulted_object

    print("### Serializing Message")
    serialized_message = command_message.SerializeToString()

    write(client_socket, serialized_message)
    print("### Message sended!!")

    return None

def set_object_status(client_socket, args):
    command_message = messages_pb2.ApplicationMessage()
    command_message.type = messages_pb2.ApplicationMessage.MessageType.COMMAND
    command_message.command = "set_status"
    command_message.args = args

    print("### Serializing Message")
    serialized_message = command_message.SerializeToString()

    write(client_socket, serialized_message)
    print("### Message sended")

    return None

def set_object_attributes(client_socket, args):
    command_message = messages_pb2.ApplicationMessage()
    command_message.type = messages_pb2.ApplicationMessage.MessageType.COMMAND
    command_message.command = "set_attributes"
    command_message.args = args

    print("### Serializing Message")
    serialized_message = command_message.SerializeToString()

    write(client_socket, serialized_message)
    print("### Message sended")

    return None

def main(client_socket):
    while True: 
        time.sleep(1)
        command = input('\nWrite a command:')
        command_split = command.split()
        try:
            if command_split[0] == 'request_list':
                request_list_objects(client_socket)
            elif command_split[0] == 'request_status':
                request_object_status(client_socket, command_split[1])
            elif command_split[0] == 'set_status':
                set_object_status(client_socket,f"{command_split[1]} {command_split[2]}")
            elif command_split[0] == 'set_attribute':
                set_object_attributes(client_socket,f"{command_split[1]} {command_split[2]} {command_split[3]}")
            else:
                print('Invalid Command!')
        except:
            print('Invalid Command!')

# conecta via tcp com o servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(ADDR_APP)
client_socket.connect(GATEWAY_ADDR)
print("### Connected with Gateway")

# início da thread para fica escutando o server
receive_thread = threading.Thread(target=receive, args=(client_socket,  ))
receive_thread.start()
print("### Listening gateway's answer")

main(client_socket)

# commands:
# request_list_objects(client_socket)
# request_object_status(client_socket, 'Lamp')
# set_object_status(client_socket, 'AC true')
# set_object_attributes(client_socket, 'AC temp 37')
# request_object_status(client_socket, 'Sprinkler')