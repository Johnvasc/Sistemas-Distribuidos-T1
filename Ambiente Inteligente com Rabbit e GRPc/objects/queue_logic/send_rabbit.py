# Esse arquivo realiza a logica para o envio de informações em filas
import pika

def create_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    channel = connection.channel()
    return connection, channel

def create_queue(channel, name_queue):
    channel.queue_declare(queue = f'{name_queue}')

def send_info(channel, info, name_queue):
    channel.basic_publish(exchange = '', routing_key = name_queue, body = f'{info}')
    print(f" [x] Sent '{info}' on queue '{name_queue}'!\n")

def close_connection(connection):
    connection.close()