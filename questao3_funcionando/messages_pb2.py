# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0emessages.proto\"\x92\x01\n\x12\x41pplicationMessage\x12-\n\x04type\x18\x01 \x01(\x0e\x32\x1f.ApplicationMessage.MessageType\x12\x0f\n\x07\x63ommand\x18\x02 \x01(\t\x12\x0c\n\x04\x61rgs\x18\x03 \x01(\t\".\n\x0bMessageType\x12\x12\n\x0eIDENTIFICATION\x10\x00\x12\x0b\n\x07\x43OMMAND\x10\x01\"E\n\x06Object\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\t\x12\x0c\n\x04temp\x18\x04 \x01(\x05\"\x8b\x01\n\x0eGatewayMessage\x12\x32\n\rresponse_type\x18\x01 \x01(\x0e\x32\x1b.GatewayMessage.MessageType\x12\x17\n\x06object\x18\x02 \x03(\x0b\x32\x07.Object\",\n\x0bMessageType\x12\n\n\x06UPDATE\x10\x00\x12\x07\n\x03GET\x10\x01\x12\x08\n\x04LIST\x10\x02\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _APPLICATIONMESSAGE._serialized_start=19
  _APPLICATIONMESSAGE._serialized_end=165
  _APPLICATIONMESSAGE_MESSAGETYPE._serialized_start=119
  _APPLICATIONMESSAGE_MESSAGETYPE._serialized_end=165
  _OBJECT._serialized_start=167
  _OBJECT._serialized_end=236
  _GATEWAYMESSAGE._serialized_start=239
  _GATEWAYMESSAGE._serialized_end=378
  _GATEWAYMESSAGE_MESSAGETYPE._serialized_start=334
  _GATEWAYMESSAGE_MESSAGETYPE._serialized_end=378
# @@protoc_insertion_point(module_scope)
