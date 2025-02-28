from shared import order_pb2 as _order_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransactionRequest(_message.Message):
    __slots__ = ("name", "CreditCard", "BillingAddress")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    name: str
    CreditCard: _order_pb2.CreditCard
    BillingAddress: _order_pb2.BillingAddress
    def __init__(self, name: _Optional[str] = ..., CreditCard: _Optional[_Union[_order_pb2.CreditCard, _Mapping]] = ..., BillingAddress: _Optional[_Union[_order_pb2.BillingAddress, _Mapping]] = ...) -> None: ...

class TransactionResponse(_message.Message):
    __slots__ = ("transactionVerified",)
    TRANSACTIONVERIFIED_FIELD_NUMBER: _ClassVar[int]
    transactionVerified: bool
    def __init__(self, transactionVerified: bool = ...) -> None: ...
