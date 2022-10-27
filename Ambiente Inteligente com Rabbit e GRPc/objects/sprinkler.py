from .sprinkler_comms.sprinkler_rabbit import SprinklerRabbit

class Sprinkler(SprinklerRabbit): 
    def __init__(self, state, ambient_humidity, queue):
        self.state = state
        self.ambient_humidity = ambient_humidity
        self.target_humidity = ambient_humidity
        self.inicial_humidity = ambient_humidity
        self.queue = queue

    def on(self):
        self.state = True
        self.ambient_humidity = self.target_humidity
        return self.state

    def off(self):
        self.state = False
        self.ambient_humidity = self.inicial_humidity
        return self.state

    def set_attribute(self, rate):
        self.target_humidity = rate
        if self.state == True:
            self.ambient_humidity = self.target_humidity
        return self.target_humidity
