# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: distributedKeyValStore.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='distributedKeyValStore.proto',
  package='distributedkeyvalstore',
  syntax='proto3',
  serialized_pb=_b('\n\x1c\x64istributedKeyValStore.proto\x12\x16\x64istributedkeyvalstore\"*\n\nGetRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0f\n\x07success\x18\x02 \x01(\x08\"7\n\x08GetReply\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x0f\n\x07success\x18\x03 \x01(\x08\"9\n\nPutRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x0f\n\x07success\x18\x03 \x01(\x08\"7\n\x08PutReply\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x0f\n\x07success\x18\x03 \x01(\x08\"-\n\rDeleteRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0f\n\x07success\x18\x02 \x01(\x08\"+\n\x0b\x44\x65leteReply\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0f\n\x07success\x18\x02 \x01(\x08\x32\x8c\x02\n\x0bKeyValStore\x12P\n\x06getrpc\x12\".distributedkeyvalstore.GetRequest\x1a .distributedkeyvalstore.GetReply\"\x00\x12P\n\x06putrpc\x12\".distributedkeyvalstore.PutRequest\x1a .distributedkeyvalstore.PutReply\"\x00\x12Y\n\tdeleterpc\x12%.distributedkeyvalstore.DeleteRequest\x1a#.distributedkeyvalstore.DeleteReply\"\x00\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_GETREQUEST = _descriptor.Descriptor(
  name='GetRequest',
  full_name='distributedkeyvalstore.GetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='distributedkeyvalstore.GetRequest.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='success', full_name='distributedkeyvalstore.GetRequest.success', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=56,
  serialized_end=98,
)


_GETREPLY = _descriptor.Descriptor(
  name='GetReply',
  full_name='distributedkeyvalstore.GetReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='distributedkeyvalstore.GetReply.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='distributedkeyvalstore.GetReply.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='success', full_name='distributedkeyvalstore.GetReply.success', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=100,
  serialized_end=155,
)


_PUTREQUEST = _descriptor.Descriptor(
  name='PutRequest',
  full_name='distributedkeyvalstore.PutRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='distributedkeyvalstore.PutRequest.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='distributedkeyvalstore.PutRequest.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='success', full_name='distributedkeyvalstore.PutRequest.success', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=157,
  serialized_end=214,
)


_PUTREPLY = _descriptor.Descriptor(
  name='PutReply',
  full_name='distributedkeyvalstore.PutReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='distributedkeyvalstore.PutReply.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='distributedkeyvalstore.PutReply.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='success', full_name='distributedkeyvalstore.PutReply.success', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=216,
  serialized_end=271,
)


_DELETEREQUEST = _descriptor.Descriptor(
  name='DeleteRequest',
  full_name='distributedkeyvalstore.DeleteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='distributedkeyvalstore.DeleteRequest.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='success', full_name='distributedkeyvalstore.DeleteRequest.success', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=273,
  serialized_end=318,
)


_DELETEREPLY = _descriptor.Descriptor(
  name='DeleteReply',
  full_name='distributedkeyvalstore.DeleteReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='distributedkeyvalstore.DeleteReply.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='success', full_name='distributedkeyvalstore.DeleteReply.success', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=320,
  serialized_end=363,
)

DESCRIPTOR.message_types_by_name['GetRequest'] = _GETREQUEST
DESCRIPTOR.message_types_by_name['GetReply'] = _GETREPLY
DESCRIPTOR.message_types_by_name['PutRequest'] = _PUTREQUEST
DESCRIPTOR.message_types_by_name['PutReply'] = _PUTREPLY
DESCRIPTOR.message_types_by_name['DeleteRequest'] = _DELETEREQUEST
DESCRIPTOR.message_types_by_name['DeleteReply'] = _DELETEREPLY

GetRequest = _reflection.GeneratedProtocolMessageType('GetRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETREQUEST,
  __module__ = 'distributedKeyValStore_pb2'
  # @@protoc_insertion_point(class_scope:distributedkeyvalstore.GetRequest)
  ))
_sym_db.RegisterMessage(GetRequest)

GetReply = _reflection.GeneratedProtocolMessageType('GetReply', (_message.Message,), dict(
  DESCRIPTOR = _GETREPLY,
  __module__ = 'distributedKeyValStore_pb2'
  # @@protoc_insertion_point(class_scope:distributedkeyvalstore.GetReply)
  ))
_sym_db.RegisterMessage(GetReply)

PutRequest = _reflection.GeneratedProtocolMessageType('PutRequest', (_message.Message,), dict(
  DESCRIPTOR = _PUTREQUEST,
  __module__ = 'distributedKeyValStore_pb2'
  # @@protoc_insertion_point(class_scope:distributedkeyvalstore.PutRequest)
  ))
_sym_db.RegisterMessage(PutRequest)

PutReply = _reflection.GeneratedProtocolMessageType('PutReply', (_message.Message,), dict(
  DESCRIPTOR = _PUTREPLY,
  __module__ = 'distributedKeyValStore_pb2'
  # @@protoc_insertion_point(class_scope:distributedkeyvalstore.PutReply)
  ))
_sym_db.RegisterMessage(PutReply)

DeleteRequest = _reflection.GeneratedProtocolMessageType('DeleteRequest', (_message.Message,), dict(
  DESCRIPTOR = _DELETEREQUEST,
  __module__ = 'distributedKeyValStore_pb2'
  # @@protoc_insertion_point(class_scope:distributedkeyvalstore.DeleteRequest)
  ))
_sym_db.RegisterMessage(DeleteRequest)

DeleteReply = _reflection.GeneratedProtocolMessageType('DeleteReply', (_message.Message,), dict(
  DESCRIPTOR = _DELETEREPLY,
  __module__ = 'distributedKeyValStore_pb2'
  # @@protoc_insertion_point(class_scope:distributedkeyvalstore.DeleteReply)
  ))
_sym_db.RegisterMessage(DeleteReply)


import grpc
from grpc.beta import implementations as beta_implementations
from grpc.beta import interfaces as beta_interfaces
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities


class KeyValStoreStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.getrpc = channel.unary_unary(
        '/distributedkeyvalstore.KeyValStore/getrpc',
        request_serializer=GetRequest.SerializeToString,
        response_deserializer=GetReply.FromString,
        )
    self.putrpc = channel.unary_unary(
        '/distributedkeyvalstore.KeyValStore/putrpc',
        request_serializer=PutRequest.SerializeToString,
        response_deserializer=PutReply.FromString,
        )
    self.deleterpc = channel.unary_unary(
        '/distributedkeyvalstore.KeyValStore/deleterpc',
        request_serializer=DeleteRequest.SerializeToString,
        response_deserializer=DeleteReply.FromString,
        )


class KeyValStoreServicer(object):

  def getrpc(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def putrpc(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def deleterpc(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_KeyValStoreServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'getrpc': grpc.unary_unary_rpc_method_handler(
          servicer.getrpc,
          request_deserializer=GetRequest.FromString,
          response_serializer=GetReply.SerializeToString,
      ),
      'putrpc': grpc.unary_unary_rpc_method_handler(
          servicer.putrpc,
          request_deserializer=PutRequest.FromString,
          response_serializer=PutReply.SerializeToString,
      ),
      'deleterpc': grpc.unary_unary_rpc_method_handler(
          servicer.deleterpc,
          request_deserializer=DeleteRequest.FromString,
          response_serializer=DeleteReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'distributedkeyvalstore.KeyValStore', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class BetaKeyValStoreServicer(object):
  def getrpc(self, request, context):
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def putrpc(self, request, context):
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def deleterpc(self, request, context):
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


class BetaKeyValStoreStub(object):
  def getrpc(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    raise NotImplementedError()
  getrpc.future = None
  def putrpc(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    raise NotImplementedError()
  putrpc.future = None
  def deleterpc(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    raise NotImplementedError()
  deleterpc.future = None


def beta_create_KeyValStore_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
  request_deserializers = {
    ('distributedkeyvalstore.KeyValStore', 'deleterpc'): DeleteRequest.FromString,
    ('distributedkeyvalstore.KeyValStore', 'getrpc'): GetRequest.FromString,
    ('distributedkeyvalstore.KeyValStore', 'putrpc'): PutRequest.FromString,
  }
  response_serializers = {
    ('distributedkeyvalstore.KeyValStore', 'deleterpc'): DeleteReply.SerializeToString,
    ('distributedkeyvalstore.KeyValStore', 'getrpc'): GetReply.SerializeToString,
    ('distributedkeyvalstore.KeyValStore', 'putrpc'): PutReply.SerializeToString,
  }
  method_implementations = {
    ('distributedkeyvalstore.KeyValStore', 'deleterpc'): face_utilities.unary_unary_inline(servicer.deleterpc),
    ('distributedkeyvalstore.KeyValStore', 'getrpc'): face_utilities.unary_unary_inline(servicer.getrpc),
    ('distributedkeyvalstore.KeyValStore', 'putrpc'): face_utilities.unary_unary_inline(servicer.putrpc),
  }
  server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
  return beta_implementations.server(method_implementations, options=server_options)


def beta_create_KeyValStore_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
  request_serializers = {
    ('distributedkeyvalstore.KeyValStore', 'deleterpc'): DeleteRequest.SerializeToString,
    ('distributedkeyvalstore.KeyValStore', 'getrpc'): GetRequest.SerializeToString,
    ('distributedkeyvalstore.KeyValStore', 'putrpc'): PutRequest.SerializeToString,
  }
  response_deserializers = {
    ('distributedkeyvalstore.KeyValStore', 'deleterpc'): DeleteReply.FromString,
    ('distributedkeyvalstore.KeyValStore', 'getrpc'): GetReply.FromString,
    ('distributedkeyvalstore.KeyValStore', 'putrpc'): PutReply.FromString,
  }
  cardinalities = {
    'deleterpc': cardinality.Cardinality.UNARY_UNARY,
    'getrpc': cardinality.Cardinality.UNARY_UNARY,
    'putrpc': cardinality.Cardinality.UNARY_UNARY,
  }
  stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
  return beta_implementations.dynamic_stub(channel, 'distributedkeyvalstore.KeyValStore', cardinalities, options=stub_options)
# @@protoc_insertion_point(module_scope)