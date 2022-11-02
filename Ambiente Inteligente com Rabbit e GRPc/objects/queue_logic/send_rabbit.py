
#Arquivo voltado para o envio de informações nas filas

import pika

#Cria conexao via RabbitMQ
def create_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    channel = connection.channel()
    return connection, channel

#Cria a fila no RabbitMQ a partir do nome passado como argumento
def create_queue(channel, name_queue):
    channel.queue_declare(queue = f'{name_queue}')

#Envio da publicacao (mensagem) para a fila especifica
def send_info(channel, info, name_queue):
    channel.basic_publish(exchange = '', routing_key = name_queue, body = f'{info}')
    print(f" [x] Sent '{info}' on queue '{name_queue}'!\n")

#Fechar conexao
def close_connection(connection):
    connection.close()