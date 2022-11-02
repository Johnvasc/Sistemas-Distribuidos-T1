
from .lamp_comms.lamp_rabbit import LampRabbit


class Lamp(LampRabbit): 
    #Estado inicial da lampada (atualmente)
    def __init__(self, state, ambient_luminosity, queue):
        self.state = state  #Estado: true/false (ligado/desligado)
        #Inicialmente, so ha uma luminosidade (sem modificacao)
        self.ambient_luminosity = ambient_luminosity
        self.target_luminosity = ambient_luminosity
        self.inicial_luminosity = ambient_luminosity
        #Nome da fila/objeto
        self.queue = queue

    #Ligar o objeto
    def on(self):
        self.state = True
        #Atualiza a luminosidade ambiente se uma nova luminosidade for setada
        self.ambient_luminosity = self.target_luminosity
        return self.state

    #Desligar o objeto
    def off(self):
        self.state = False
        #Objeto desligado, volta para a luminosidade ambiente
        self.ambient_luminosity = self.inicial_luminosity
        return self.state

    #Mudar o valor do atributo do objeto
    def set_attribute(self, rate):
        #rate = novo valor
        self.target_luminosity = rate
        if self.state == True:
            #Atualiza a luminosidade ambiente
            self.ambient_luminosity = self.target_luminosity
        return self.target_luminosity
