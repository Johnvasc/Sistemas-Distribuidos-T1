
from .sprinkler_comunicacao.rabbit_sprinkler import SprinklerRabbit


class Sprinkler(SprinklerRabbit): 
    #Estado inicial do irrigador (atualmente)
    def __init__(self, state, ambient_humidity, queue):
        self.state = state  #Estado: true/false (ligado/desligado)
        #Inicialmente, so ha uma umidade (sem modificacao)
        self.ambient_humidity = ambient_humidity
        self.target_humidity = ambient_humidity
        self.inicial_humidity = ambient_humidity
        #Nome da fila/objeto
        self.queue = queue

    #Ligar o objeto
    def on(self):
        self.state = True
        #Atualiza a luminosidade ambiente se uma nova umidade for setada
        self.ambient_humidity = self.target_humidity
        return self.state

    #Desligar o objeto
    def off(self):
        self.state = False
        #Objeto desligado, volta para a umidade ambiente
        self.ambient_humidity = self.inicial_humidity
        return self.state

    #Mudar o valor do atributo do objeto
    def set_attribute(self, rate):
        #rate = novo valor
        self.target_humidity = rate
        if self.state == True:
            #Atualiza a umidade ambiente
            self.ambient_humidity = self.target_humidity
        return self.target_humidity
