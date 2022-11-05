
from .ac_comunicacao.ac_rabbit import AcRabbit


class Ac(AcRabbit): 
    #Estado inicial do ar-condicionado (atualmente)
    def __init__(self, state, ambient_temperature, queue):
        self.state = state  #Estado: true/false (ligado/desligado)
        #Inicialmente, so ha uma temperatura (sem modificacao)
        self.ambient_temperature = ambient_temperature
        self.target_temperature = ambient_temperature
        self.inicial_temperature = ambient_temperature
        #Nome da fila/objeto
        self.queue = queue

    #Ligar o objeto
    def on(self):
        self.state = True
        #Atualiza a temperatura ambiente se uma nova temperatura for setada
        self.ambient_temperature = self.target_temperature
        return self.state

    #Desligar o objeto
    def off(self):
        self.state = False
        #Objeto desligado, volta para a temperatura ambiente
        self.ambient_temperature = self.inicial_temperature
        return self.state

    #Mudar o valor do atributo do objeto
    def set_attribute(self, rate):
        #rate = novo valor
        self.target_temperature = rate
        if self.state == True:
            #Atualiza a temperatura ambiente
            self.ambient_temperature = self.target_temperature
        return self.target_temperature