
from objects.ac import Ac

from objects.grpc_config.objeto_de_servico import ObjectServicer
from concurrent import futures
from generated import object_pb2_grpc
import random
import grpc

#Nome das filas criadas pelo home assistant
queue_main = 'principal'
final_queue = 'finalizado'

#Nome da fila e do objeto que ficara salvo em uma lista no home assistant
name_queue = input('Nome do AC: ')

while name_queue == 'principal' or name_queue == 'finalizado':
    print('Nome nao disponiveis para uso, tente outro nome!')
    name_queue = input('Nome do AC: ')

#Temperatura atual do ambiente
temperatura_inicial = random.randint(18,22)
print(f'A temperatura ambiente eh {temperatura_inicial} graus!')

#Porta de comunicacao
porta_ac = input("Port: ")

#Status inicial do objeto
ac = Ac(False, temperatura_inicial, name_queue)

#---------------------------------------------------------------------------------------------

#Comunicacao RabbitMQ
connection, channel = ac.connect_rabbit()

#Cria fila para o objeto em questao
ac.set_queue(channel, ac.queue) 
#Cria fila principal do home assistant, caso ela ja nao exista
ac.set_queue(channel, queue_main) #se liga com a queue principal
#Cria fila de termino do home assistant, caso ela ja nao exista
ac.set_queue(channel, final_queue)

#Envio do nome da fila do objeto para o home assistent se conectar com sua fila
ac.send_queue(channel, f"{ac.queue} {porta_ac}", queue_main) #envia a queue do objeto ac pro home assistent conectar com sua fila (queue recepção)
#Envio da mensagem com seu conteudo (nome, estado, atributo)
ac.send_temperature_updates(channel)

#---------------------------------------------------------------------------------------------

#Comunicacao gRPC
ac_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
object_pb2_grpc.add_ObjectServicer_to_server(ObjectServicer(ac), ac_grpc_server)
ac_grpc_server.add_insecure_port(f"localhost:{porta_ac}")
ac_grpc_server.start()

#---------------------------------------------------------------------------------------------

input('Pressione ENTER para sair\n')
#Fecha conexao enviando o nome da fila/objeto para a fila close
ac.close(connection, channel, final_queue)