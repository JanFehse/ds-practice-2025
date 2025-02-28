from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectFraudRequest(_message.Message):
    __slots__ = ("CreditCardNumber", "BillingAddress")
    CREDITCARDNUMBER_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    CreditCardNumber: str
    BillingAddress: BillingAddress
    def __init__(self, CreditCardNumber: _Optional[str] = ..., BillingAddress: _Optional[_Union[BillingAddress, _Mapping]] = ...) -> None: ...

class DetectFraudResponse(_message.Message):
    __slots__ = ("isLegit",)
    ISLEGIT_FIELD_NUMBER: _ClassVar[int]
    isLegit: bool
    def __init__(self, isLegit: bool = ...) -> None: ...

class BillingAddress(_message.Message):
    __slots__ = ("street", "city", "state", "zip", "country")
    STREET_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ZIP_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    street: str
    city: str
    state: str
    zip: str
    country: str
    def __init__(self, street: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., zip: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...
