from .lamp_comms.lamp_rabbit import LampRabbit


class Lamp(LampRabbit): 
    def __init__(self, state, ambient_luminosity, queue):
        self.state = state
        self.ambient_luminosity = ambient_luminosity
        self.target_luminosity = ambient_luminosity
        self.inicial_luminosity = ambient_luminosity
        self.queue = queue

    def on(self):
        self.state = True
        self.ambient_luminosity = self.target_luminosity
        return self.state

    def off(self):
        self.state = False
        self.ambient_luminosity = self.inicial_luminosity
        return self.state

    def set_attribute(self, rate):
        self.target_luminosity = rate
        if self.state == True:
            self.ambient_luminosity = self.target_luminosity
        return self.target_luminosity
