import socket
import threading

from generated import object_pb2_grpc
from generated import object_pb2

FORMAT = 'UTF-8'
class HomeAssistantTCP():
    def start_tcp(self, ip_server, port):
        ADDR = (ip_server, port)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(ADDR)
        server_socket.listen()

        print("Server On!")
        print("IP's Server: ", ADDR)

        return server_socket
    
    def connect_tcp(self, server_socket):
            client, address = server_socket.accept()
            print("Connected with {}".format(str(address)))
            client.send('Connected to server!'.encode(FORMAT))
            thread = threading.Thread(target = self.handle, args = (client,), daemon = True)
            thread.start()
    
    def handle(self, client):
        while True:
            message = client.recv(1024)
            message_decoded = message.decode(FORMAT)
            command = message_decoded.split()
            try:
                if command[0] == 'request_list':
                    response_msg = f'{list(self.objects.keys())}'
                    client.send(response_msg.encode(FORMAT))
                elif command[0] == 'exit':
                    print("Desconectando aplicação....")
                    client.close()
                    print("Aplicação desconectada!")
                    del client
                    break
                elif command[1] == 'set_status_on':
                    selected_object = self.objects[command[0]]
                    response_msg = selected_object.On(object_pb2.Empty())
                    client.send(f'Objeto com status definido para {response_msg}'.encode(FORMAT))
                elif command[1] == 'set_status_off':
                    selected_object = self.objects[command[0]]
                    response_msg = selected_object.Off(object_pb2.Empty())
                    client.send(f'Objeto com status definido para False'.encode(FORMAT))
                elif command[1] == 'set_attribute':
                    selected_object = self.objects[command[0]]
                    response_msg = selected_object.SetAttribute(object_pb2.NewAttribute(value = float(command[2])))
                    client.send(f'Objeto com atributo definido para {response_msg}'.encode(FORMAT))
                elif command[1] == 'request_status':
                    object_data = self.objects_data[command[0]]
                    client.send(object_data.encode(FORMAT))
            except:
                response_msg = 'Comando Inválido... Tente novamente! =D'
                client.send(response_msg.encode(FORMAT))