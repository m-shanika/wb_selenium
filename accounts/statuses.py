from dataclasses import dataclass, field
import typing
from strenum import StrEnum

class OSOperationStatus(StrEnum):
    TZ_INPOOL = "TZ_INPOOL"
    TZ_NUM_WAIT = "TZ_NUM_WAIT"
    TZ_NUM_ANSWER = "TZ_NUM_ANSWER"
    TZ_OVER_EMPTY = "TZ_OVER_EMPTY"
    TZ_OVER_OK = "TZ_OVER_OK"
    ERROR_NO_TZID = "ERROR_NO_TZID"
    ERROR_NO_OPERATIONS = "ERROR_NO_OPERATIONS"
    
class Sex(StrEnum):
    MALE = "male",
    FEMALE = "female"
    
class FDGender(StrEnum):
    MAN = "man"
    WOMAN = "woman"
    UNSET = "unset"
    
@dataclass
class FDResponse:
    LastName: str
    FirstName: str
    

@dataclass
class OSBalance:
    response: str
    balance: float
    zbalance: float
    
@dataclass
class OSCountry:
    name: str
    original: str
    code: int
    pos: int
    other: bool
    new: bool
    enable: bool
    
@dataclass
class OSService:
    id: int
    count: int
    price: str
    service: str
    slug: str
    
@dataclass
class OSTariffs:
    response: str
    countries: typing.List[typing.Dict[str, OSCountry]] = field(default_factory=list)
    services: typing.List[typing.Dict[str, OSService]] = field(default_factory=list)
    favorite_countries: typing.List[typing.Dict[str, OSCountry]] = field(default_factory=list)
    favorite_services: typing.List[typing.Dict[str, OSService]] = field(default_factory=list)
    page: int = None
    country: int = None
    filter: str = None
    end: bool = None
    favorites: str = None
    
    
@dataclass
class OSNumber:
    response: str
    tzid: int
    number: str = None
    country: int = None
    service: str = None
    title: str = None
    response_text: str = None
    time: str = None
    
@dataclass
class CaptchaAnswer:
    captchaSolve: str
    taskId: str
    error: bool
    errorBody: str
    
@dataclass
class OSStatus:
    country: int
    sum: int
    service: str
    number: str
    response: OSOperationStatus
    tzid: int
    time: int
    form: str
    subscription_package_id: int
    msg: str = None
    webhook_url: str = None
    
    
@dataclass
class Profile:
    surname: str
    name: str
    session: str
    phone_number: str
    sex: Sex
    cookie: str
    token: str



