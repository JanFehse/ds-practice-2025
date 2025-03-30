from shared import order_pb2 as _order_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union, List as _List

DESCRIPTOR: _descriptor.FileDescriptor

class Book(_message.Message):
    __slots__ = ("bookId", "title", "author")
    BOOKID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    bookId: int
    title: str
    author: str
    def __init__(self, bookId: int = ..., title: str = ..., author: str = ...) -> None: ...

class QueueOrderRequest(_message.Message):
    __slots__ = ("info", "booksInCart", "name", "CreditCard", "BillingAddress")
    INFO_FIELD_NUMBER: _ClassVar[int]
    BOOKSINCART_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    info: _order_pb2.ExecInfo
    booksInCart: _List["Book"]
    name: str
    CreditCard: _order_pb2.CreditCard
    BillingAddress: _order_pb2.BillingAddress
    def __init__(self, info: _Optional[_Union[_order_pb2.ExecInfo, _Mapping]] = ..., booksInCart: _Optional[_List[_Union["Book", _Mapping]]] = ..., name: str = ..., CreditCard: _Optional[_Union[_order_pb2.CreditCard, _Mapping]] = ..., BillingAddress: _Optional[_Union[_order_pb2.BillingAddress, _Mapping]] = ...) -> None: ...
