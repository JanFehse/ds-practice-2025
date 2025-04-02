from shared import order_pb2 as _order_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueueOrderRequest(_message.Message):
    __slots__ = ("info", "booksInCart", "name", "CreditCard", "BillingAddress")
    INFO_FIELD_NUMBER: _ClassVar[int]
    BOOKSINCART_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    info: _order_pb2.ExecInfo
    booksInCart: _containers.RepeatedCompositeFieldContainer[OrderedBook]
    name: str
    CreditCard: _order_pb2.CreditCard
    BillingAddress: _order_pb2.BillingAddress
    def __init__(self, info: _Optional[_Union[_order_pb2.ExecInfo, _Mapping]] = ..., booksInCart: _Optional[_Iterable[_Union[OrderedBook, _Mapping]]] = ..., name: _Optional[str] = ..., CreditCard: _Optional[_Union[_order_pb2.CreditCard, _Mapping]] = ..., BillingAddress: _Optional[_Union[_order_pb2.BillingAddress, _Mapping]] = ...) -> None: ...

class DequeueOrderResponse(_message.Message):
    __slots__ = ("order", "error")
    ORDER_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    order: QueueOrderRequest
    error: _order_pb2.ErrorResponse
    def __init__(self, order: _Optional[_Union[QueueOrderRequest, _Mapping]] = ..., error: _Optional[_Union[_order_pb2.ErrorResponse, _Mapping]] = ...) -> None: ...

class OrderedBook(_message.Message):
    __slots__ = ("title", "quantity")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    title: str
    quantity: int
    def __init__(self, title: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class CoordinateRequest(_message.Message):
    __slots__ = ("portnumber",)
    PORTNUMBER_FIELD_NUMBER: _ClassVar[int]
    portnumber: str
    def __init__(self, portnumber: _Optional[str] = ...) -> None: ...

class CoordinateResponse(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...
