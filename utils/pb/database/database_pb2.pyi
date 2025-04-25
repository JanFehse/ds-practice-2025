from shared import order_pb2 as _order_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReadRequest(_message.Message):
    __slots__ = ("title",)
    TITLE_FIELD_NUMBER: _ClassVar[int]
    title: str
    def __init__(self, title: _Optional[str] = ...) -> None: ...

class ReadResponse(_message.Message):
    __slots__ = ("amount",)
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    amount: int
    def __init__(self, amount: _Optional[int] = ...) -> None: ...

class WriteRequest(_message.Message):
    __slots__ = ("title", "new_stock")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    NEW_STOCK_FIELD_NUMBER: _ClassVar[int]
    title: str
    new_stock: int
    def __init__(self, title: _Optional[str] = ..., new_stock: _Optional[int] = ...) -> None: ...

class ChangeAmountRequest(_message.Message):
    __slots__ = ("title", "amount")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    title: str
    amount: int
    def __init__(self, title: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...

class PrepareRequest(_message.Message):
    __slots__ = ("books", "id")
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    books: _containers.RepeatedCompositeFieldContainer[ChangeAmountRequest]
    id: int
    def __init__(self, books: _Optional[_Iterable[_Union[ChangeAmountRequest, _Mapping]]] = ..., id: _Optional[int] = ...) -> None: ...
