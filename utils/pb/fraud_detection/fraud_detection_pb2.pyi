from shared import order_pb2 as _order_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InitDetectFraudRequest(_message.Message):
    __slots__ = ("info", "CreditCard", "BillingAddress")
    INFO_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    info: _order_pb2.ExecInfo
    CreditCard: _order_pb2.CreditCard
    BillingAddress: _order_pb2.BillingAddress
    def __init__(self, info: _Optional[_Union[_order_pb2.ExecInfo, _Mapping]] = ..., CreditCard: _Optional[_Union[_order_pb2.CreditCard, _Mapping]] = ..., BillingAddress: _Optional[_Union[_order_pb2.BillingAddress, _Mapping]] = ...) -> None: ...

class DetectFraudResponse(_message.Message):
    __slots__ = ("isLegit",)
    ISLEGIT_FIELD_NUMBER: _ClassVar[int]
    isLegit: bool
    def __init__(self, isLegit: bool = ...) -> None: ...
