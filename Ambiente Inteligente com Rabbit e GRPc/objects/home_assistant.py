
from objects.assistente_comunicacao.assistente_rabbit import HomeAssistantRabbit
from objects.assistente_comunicacao.assistente_grpc import HomeAssistantGRPC
from objects.assistente_comunicacao.assistente_tcp import HomeAssistantTCP

class HomeAssistant(HomeAssistantRabbit, HomeAssistantGRPC, HomeAssistantTCP):
  def __init__(self):
    self.main_queue = 'principal'
    self.final_queue = 'finalizado'
    self.objects = {}
    self.objects_data = {}
