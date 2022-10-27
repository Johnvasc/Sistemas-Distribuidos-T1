from objects.home_assistant_comms.home_assistant_rabbit import HomeAssistantRabbit
from objects.home_assistant_comms.home_assistant_grpc import HomeAssistantGRPC
from objects.home_assistant_comms.home_assistant_tcp import HomeAssistantTCP



class HomeAssistant(HomeAssistantRabbit, HomeAssistantGRPC, HomeAssistantTCP):
  def __init__(self):
    self.queue_principal = 'home'
    self.end_queue = 'close'
    self.objects = {}
    self.objects_data = {}
