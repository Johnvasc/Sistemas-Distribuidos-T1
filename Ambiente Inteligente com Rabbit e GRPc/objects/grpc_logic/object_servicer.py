from generated import object_pb2
from generated import object_pb2_grpc

class ObjectServicer(object_pb2_grpc.ObjectServicer):
  def __init__(self, object):
    self.object = object

  def On(self, request, context):
    response = object_pb2.RespondState()
    response.state = self.object.on()
    return response

  def Off(self, request, context):
    response = object_pb2.RespondState()
    response.state = self.object.off()
    return response

  def SetAttribute(self, request, context):
    response = object_pb2.RespondAttribute()
    response.value = self.object.set_attribute(request.value)
    return response
