# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: transaction_verification/transaction_verification.proto
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
    'transaction_verification/transaction_verification.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from shared import order_pb2 as shared_dot_order__pb2
from suggestions import suggestions_pb2 as suggestions_dot_suggestions__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7transaction_verification/transaction_verification.proto\x12\tbookstore\x1a\x12shared/order.proto\x1a\x1dsuggestions/suggestions.proto\"\xc9\x01\n\x12TransactionRequest\x12!\n\x04info\x18\x01 \x01(\x0b\x32\x13.bookstore.ExecInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12)\n\nCreditCard\x18\x03 \x01(\x0b\x32\x15.bookstore.CreditCard\x12\x31\n\x0e\x42illingAddress\x18\x04 \x01(\x0b\x32\x19.bookstore.BillingAddress\x12$\n\x0b\x62ooksInCart\x18\x05 \x03(\x0b\x32\x0f.bookstore.Book\"2\n\x13TransactionResponse\x12\x1b\n\x13transactionVerified\x18\x01 \x01(\x08\x32\xf4\x01\n\x1eTransactionVerificationService\x12P\n\x15InitVerifyTransaction\x12\x1d.bookstore.TransactionRequest\x1a\x18.bookstore.ErrorResponse\x12\x42\n\x11VerifyTransaction\x12\x13.bookstore.ExecInfo\x1a\x18.bookstore.ErrorResponse\x12<\n\x0b\x44\x65leteOrder\x12\x13.bookstore.ExecInfo\x1a\x18.bookstore.ErrorResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_verification.transaction_verification_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TRANSACTIONREQUEST']._serialized_start=122
  _globals['_TRANSACTIONREQUEST']._serialized_end=323
  _globals['_TRANSACTIONRESPONSE']._serialized_start=325
  _globals['_TRANSACTIONRESPONSE']._serialized_end=375
  _globals['_TRANSACTIONVERIFICATIONSERVICE']._serialized_start=378
  _globals['_TRANSACTIONVERIFICATIONSERVICE']._serialized_end=622
# @@protoc_insertion_point(module_scope)
