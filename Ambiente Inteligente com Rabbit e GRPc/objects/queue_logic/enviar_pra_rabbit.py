
#Arquivo voltado para o envio de informações nas filas

import pika

#Cria conexao via RabbitMQ
def create_connection():
    conexao = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    channel = conexao.channel()
    return conexao, channel

#Cria a fila no RabbitMQ a partir do nome passado como argumento
def create_queue(channel, nome_queue):
    channel.queue_declare(queue = f'{nome_queue}')

#Envio da publicacao (mensagem) para a fila especifica
def send_info(channel, info, nome_queue):
    channel.basic_publish(exchange = '', routing_key = nome_queue, body = f'{info}')
    print(f" [x] Mandando '{info}' na fila '{nome_queue}'!\n")

#Fechar conexao
def close_connection(conexao):
    conexao.close()