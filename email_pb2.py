# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: email.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x65mail.proto\x12\x05\x65mail\"T\n\x0c\x45mailRequest\x12\x0f\n\x07subject\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0f\n\x07\x65mailTo\x18\x03 \x01(\t\x12\x11\n\temailFrom\x18\x04 \x01(\t\"1\n\rEmailResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2H\n\x0c\x45mailService\x12\x38\n\tSendEmail\x12\x13.email.EmailRequest\x1a\x14.email.EmailResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'email_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMAILREQUEST._serialized_start=22
  _EMAILREQUEST._serialized_end=106
  _EMAILRESPONSE._serialized_start=108
  _EMAILRESPONSE._serialized_end=157
  _EMAILSERVICE._serialized_start=159
  _EMAILSERVICE._serialized_end=231
# @@protoc_insertion_point(module_scope)
