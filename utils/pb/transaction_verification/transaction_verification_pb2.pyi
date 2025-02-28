from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransactionRequest(_message.Message):
    __slots__ = ("name", "CreditCardNumber", "expirationDate", "cvv", "BillingAddress")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREDITCARDNUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    name: str
    CreditCardNumber: str
    expirationDate: str
    cvv: str
    BillingAddress: BillingAddress
    def __init__(self, name: _Optional[str] = ..., CreditCardNumber: _Optional[str] = ..., expirationDate: _Optional[str] = ..., cvv: _Optional[str] = ..., BillingAddress: _Optional[_Union[BillingAddress, _Mapping]] = ...) -> None: ...

class TransactionResponse(_message.Message):
    __slots__ = ("transactionVerified",)
    TRANSACTIONVERIFIED_FIELD_NUMBER: _ClassVar[int]
    transactionVerified: bool
    def __init__(self, transactionVerified: bool = ...) -> None: ...

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
