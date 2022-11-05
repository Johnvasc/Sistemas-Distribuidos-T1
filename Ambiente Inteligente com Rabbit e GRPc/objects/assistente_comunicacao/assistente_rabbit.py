from objects.queue_logic import recebe_rabbit as rr
import threading

FORMAT = 'utf-8'

class HomeAssistantRabbit():
  #Funcao de conexao via RabbitMQ
  def connect_rabbit(self):
    connection, channel = rr.connect()
    return connection, channel
    
  def start_principal_queue(self):
    def callback_new_queue(ch, method, properties, body):
      def callback_queue(ch, method, properties, body): 
          #O objeto constantemente envia uma mensagem com suas informacoes para a fila com seu nome
          #Fila a qual foi criada conexao via RabbitMQ com o home assistant

          #Mensagem lida da fila
          mensagem = body.decode(FORMAT)
          #Cada informacao separadamente
          itens = mensagem.split()
          #Link do nome do objeto/nome da fila com a mensagem lida
          self.objects_data[itens[0]] = mensagem
          #print(f'A mensagem eh {mensagem}, os itens sao {itens} e os dados salvos sao {self.objects_data[itens[0]]}')

      #Recebe via RabbitMQ, a partir da fila home, o nome da fila/objeto e sua porta

      #Mensagem com nome da fila/objeto e porta
      mensagem = body.decode(FORMAT)
      #Nome da fila/objeto
      new_queue = mensagem.split()[0]
      #print(f'A mensagem eh {mensagem} e o nome da fila eh {new_queue}')

      #Criando comunicacao via gRPC
      self.create_new_remote_object(mensagem)
      
      #Thread de consumo da nova fila criada (fila de comunicacao do objeto novo)
      thread_queue = threading.Thread(target = rr.consume_queue, args = (new_queue, callback_queue), daemon = True)
      thread_queue.start()

    #Thread de consumo da fila principal (home)
    consume_thread_queue = threading.Thread(target = rr.consume_queue, args = (self.main_queue, callback_new_queue), daemon = True)
    consume_thread_queue.start()

  #Fila a qual se um objeto enviar uma mensagem, esse objeto eh considerado finalizado (conexao cortada)
  def start_end_queue(self):
    def callback_end_queue(ch, method, properties, body):
      #A mensagem recebida eh o nome da fila/objeto
      object_selected = body.decode(FORMAT)
      #Retira da lista de objetos conectados ao home assistant
      self.objects.pop(object_selected, None)
      #Retira da lista de dados dos objetos conectados ao home assistant
      self.objects_data.pop(object_selected, None)
      print(f"O Objeto foi desconectado. {object_selected}")

    #Thread de consumo da fila de fim de objetos (close)
    consume_thread_queue = threading.Thread(target = rr.consume_queue, args = (self.final_queue, callback_end_queue), daemon = True)
    consume_thread_queue.start()