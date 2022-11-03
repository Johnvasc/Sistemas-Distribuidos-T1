
from objects.ac import Ac

from objects.grpc_logic.object_servicer import ObjectServicer
from concurrent import futures
from generated import object_pb2_grpc
import grpc

#Nome das filas criadas pelo home assistant
queue_principal = 'home'
end_queue = 'close'

#Nome da fila e do objeto que ficara salvo em uma lista no home assistant
name_queue = input('Nome do AC: ')
#Tempeatura atual do ambiente
temp_inicial = input("Qual a temperatura ambiente (em °C)? ")
#Porta de comunicacao
ac_port = input("Port: ")

#Status inicial do objeto
ac = Ac(False, temp_inicial, name_queue)

#---------------------------------------------------------------------------------------------

#Comunicacao RabbitMQ
connection, channel = ac.connect_rabbit()

#Cria fila para o objeto em questao
ac.set_queue(channel, ac.queue) 
#Cria fila principal do home assistant, caso ela ja nao exista
ac.set_queue(channel, queue_principal) #se liga com a queue principal
#Cria fila de termino do home assistant, caso ela ja nao exista
ac.set_queue(channel, end_queue)

#Envio do nome da fila do objeto para o home assistent se conectar com sua fila
ac.send_queue(channel, f"{ac.queue} {ac_port}", queue_principal) #envia a queue do objeto ac pro home assistent conectar com sua fila (queue recepção)
#Envio da mensagem com seu conteudo (nome, estado, atributo)
ac.send_temperature_updates(channel)

#---------------------------------------------------------------------------------------------

#Comunicacao gRPC
ac_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
object_pb2_grpc.add_ObjectServicer_to_server(ObjectServicer(ac), ac_grpc_server)
ac_grpc_server.add_insecure_port(f"localhost:{ac_port}")
ac_grpc_server.start()

#---------------------------------------------------------------------------------------------

input('Pressione ENTER para sair\n')
#Fecha conexao enviando o nome da fila/objeto para a fila close
ac.close(connection, channel, end_queue)