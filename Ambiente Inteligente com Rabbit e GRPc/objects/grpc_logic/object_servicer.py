
from generated import object_pb2
from generated import object_pb2_grpc


#ObjectServicer fornece uma implementacao dos metodos do servico Object
class ObjectServicer(object_pb2_grpc.ObjectServicer):
  def __init__(self, object):
    self.object = object

  #Metodo para chamar a funcao de ligar do objeto
  def On(self, request, context):
    response = object_pb2.RespondState()
    response.state = self.object.on()
    return response

  #Metodo para chamar a funcao de desligar do objeto
  def Off(self, request, context):
    response = object_pb2.RespondState()
    response.state = self.object.off()
    return response

  #Metodo para chamar a funcaode mudar o valor do atributo do objeto
  def SetAttribute(self, request, context):
    response = object_pb2.RespondAttribute()
    response.value = self.object.set_attribute(request.value)
    return response
