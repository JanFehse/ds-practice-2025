# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: suggestions/suggestions.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'suggestions/suggestions.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from shared import order_pb2 as shared_dot_order__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsuggestions/suggestions.proto\x12\tbookstore\x1a\x12shared/order.proto\"]\n\x12SuggestionsRequest\x12!\n\x04info\x18\x01 \x01(\x0b\x32\x13.bookstore.ExecInfo\x12$\n\x0b\x62ooksInCart\x18\x02 \x03(\x0b\x32\x0f.bookstore.Book\">\n\x13SuggestionsResponse\x12\'\n\x0e\x62ooksSuggested\x18\x01 \x03(\x0b\x32\x0f.bookstore.Book\"5\n\x04\x42ook\x12\x0e\n\x06\x62ookId\x18\x01 \x01(\x03\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t2\xe2\x01\n\x12SuggestionsService\x12M\n\x12InitGetSuggestions\x12\x1d.bookstore.SuggestionsRequest\x1a\x18.bookstore.ErrorResponse\x12?\n\x0eGetSuggestions\x12\x13.bookstore.ExecInfo\x1a\x18.bookstore.ErrorResponse\x12<\n\x0b\x44\x65leteOrder\x12\x13.bookstore.ExecInfo\x1a\x18.bookstore.ErrorResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'suggestions.suggestions_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SUGGESTIONSREQUEST']._serialized_start=64
  _globals['_SUGGESTIONSREQUEST']._serialized_end=157
  _globals['_SUGGESTIONSRESPONSE']._serialized_start=159
  _globals['_SUGGESTIONSRESPONSE']._serialized_end=221
  _globals['_BOOK']._serialized_start=223
  _globals['_BOOK']._serialized_end=276
  _globals['_SUGGESTIONSSERVICE']._serialized_start=279
  _globals['_SUGGESTIONSSERVICE']._serialized_end=505
# @@protoc_insertion_point(module_scope)
