from .ac_comms.ac_rabbit import AcRabbit

class Ac(AcRabbit): 
    def __init__(self, state, ambient_temperature, queue):
        self.state = state
        self.ambient_temperature = ambient_temperature
        self.target_temperature = ambient_temperature
        self.inicial_temperature = ambient_temperature
        self.queue = queue

    def on(self):
        self.state = True
        self.ambient_temperature = self.target_temperature
        return self.state

    def off(self):
        self.state = False
        self.ambient_temperature = self.inicial_temperature
        return self.state

    def set_attribute(self, rate):
        self.target_temperature = rate
        if self.state == True:
            self.ambient_temperature = self.target_temperature
        return self.target_temperature