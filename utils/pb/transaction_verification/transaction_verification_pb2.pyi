from shared import order_pb2 as _order_pb2
from suggestions import suggestions_pb2 as _suggestions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransactionRequest(_message.Message):
    __slots__ = ("info", "name", "CreditCard", "BillingAddress", "booksInCart")
    INFO_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    BOOKSINCART_FIELD_NUMBER: _ClassVar[int]
    info: _order_pb2.ExecInfo
    name: str
    CreditCard: _order_pb2.CreditCard
    BillingAddress: _order_pb2.BillingAddress
    booksInCart: _containers.RepeatedCompositeFieldContainer[_suggestions_pb2.Book]
    def __init__(self, info: _Optional[_Union[_order_pb2.ExecInfo, _Mapping]] = ..., name: _Optional[str] = ..., CreditCard: _Optional[_Union[_order_pb2.CreditCard, _Mapping]] = ..., BillingAddress: _Optional[_Union[_order_pb2.BillingAddress, _Mapping]] = ..., booksInCart: _Optional[_Iterable[_Union[_suggestions_pb2.Book, _Mapping]]] = ...) -> None: ...

class TransactionResponse(_message.Message):
    __slots__ = ("transactionVerified",)
    TRANSACTIONVERIFIED_FIELD_NUMBER: _ClassVar[int]
    transactionVerified: bool
    def __init__(self, transactionVerified: bool = ...) -> None: ...
