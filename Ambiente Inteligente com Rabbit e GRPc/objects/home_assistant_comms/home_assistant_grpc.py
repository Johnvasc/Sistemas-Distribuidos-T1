from generated import object_pb2_grpc
import grpc
import time


class HomeAssistantGRPC():

    def start_grpc_client(self, port):
        channel = grpc.insecure_channel(f"localhost:{port}")
        return channel

    def create_new_remote_object(self, msg):
        object_name, new_port = msg.split()[0], msg.split()[1]

        channel = self.start_grpc_client(new_port) #cria o cannal de comunicação grpc para esse objeto
        self.objects[object_name] = object_pb2_grpc.ObjectStub(channel) #armazena o canal de comunicação para esse novo objeto usando o nome como referencia