
from generated import object_pb2_grpc
import grpc

class HomeAssistantGRPC():

    #Criacao do canal de comunicao
    def start_grpc_client(self, port):
        channel = grpc.insecure_channel(f"localhost:{port}")
        return channel

    #Criando o Stub da comunicacao gRPC
    def create_new_remote_object(self, msg):
        object_name, new_port = msg.split()[0], msg.split()[1]

        #Criacao do cannal de comunicação gRPC o objeto em questao
        channel = self.start_grpc_client(new_port) 

        #Guarda o canal de comunicação, usando o nome como referencia para o objeto em questão
        self.objects[object_name] = object_pb2_grpc.ObjectStub(channel)