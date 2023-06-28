from typing import List, Dict
from enum import Enum
from pydantic import BaseModel, Field
import datetime

class ProxyVersion(Enum):
    IPv6 = 6
    IPv4 = 4
    IPv4Shared = 3

class ProxyCountry(Enum):
    UKRAINE = 'ua'
    LATVIA = 'lv'
    RUSSIA = 'ru'
    BELGIUM = 'be'
    BELARUS = 'by'
    ROMANIA = 'ro'
    SLOVENIA = 'si'
    SOUTH_AFRICA = 'za'
    AUSTRALIA = 'au'
    JAPAN = 'jp'
    MOLDOVA = 'md'
    ISRAEL = 'il'
    SPAIN = 'es'
    GERMANY = 'de'
    KYRGYZSTAN = 'kg'
    TAJIKISTAN = 'tj'
    TURKMENISTAN = 'tm'
    UNITED_STATES = 'us'
    UNITED_KINGDOM = 'gb'
    EGYPT = 'eg'
    PHILIPPINES = 'ph'
    HONG_KONG = 'hk'
    KAZAKHSTAN = 'kz'
    BULGARIA = 'bg'
    MALAYSIA = 'my'
    THAILAND = 'th'
    SOUTH_KOREA = 'kr'
    SERBIA = 'rs'
    CYPRUS = 'cy'
    BANGLADESH = 'bd'
    UNITED_ARAB_EMIRATES = 'ae'
    UZBEKISTAN = 'uz'
    NIGERIA = 'ng'
    MEXICO = 'mx'
    TAIWAN = 'tw'
    SINGAPORE = 'sg'
    ITALY = 'it'
    BRAZIL = 'br'
    LITHUANIA = 'lt'
    INDONESIA = 'id'
    DENMARK = 'dk'
    VIETNAM = 'vn'
    INDIA = 'in'
    CHINA = 'cn'
    PORTUGAL = 'pt'
    NETHERLANDS = 'nl'
    GEORGIA = 'ge'
    IRELAND = 'ie'
    CHILE = 'cl'
    ARMENIA = 'am'
    ESTONIA = 'ee'
    FRANCE = 'fr'
    POLAND = 'pl'
    CZECH_REPUBLIC = 'cz'
    AUSTRIA = 'at'
    NORWAY = 'no'
    FINLAND = 'fi'
    GREECE = 'gr'
    SWITZERLAND = 'ch'
    SWEDEN = 'se'
    TURKEY = 'tr'
    CANADA = 'ca'

class ProxyState(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    EXPIRING = "expiring"
    all = "all"

class ProxyScheme(Enum):
    HTTPS = "http"
    SOCKS5 = "socks"

class Currency(Enum):
    RUB = "RUB"
    USD = "USD"


class Price(BaseModel):
    '''
    Contains information about the cost of the order, depending on the version, period and number of proxy.

    Attributes
    ----------
    price (float): 
        Total cost
    price_single (float):
        Price of one proxy
    period (int):
        Given period (days)
    count (int):
        Given amount of proxies
    '''
    price: float
    price_single: float
    period: int
    count: int


class Proxy(BaseModel):
    '''
    Contains full information about proxy

    Attributes
    ----------
    id (int):
        Proxy ID
    ip (str):
        Proxy IP
    host (str):
        Proxy Host
    port (str):
        Proxy Port
    user (str):
        Proxy Auth User
    pass (str):
        Proxy Auth Password
    type (str):
        Proxy scheme
    country (str):
        Proxy country code in iso2 format.
    date (str):
        Proxy issue date
    date_end (str):
        Proxy expiration date
    unixtime (int):
        Proxy issue date in unixtime
    unixtime_end (int):
        Proxy epxiration date in unixtime
    descr (str):
        Proxy technical description
    active (int):
        True - proxy is active, False - proxy is inactive
    proxy_link (str):
        Full proxy link address to connect to proxy
    '''

    id: int
    ip: str
    host: str
    port: str
    user: str
    pswd: str = Field(alias='pass')
    type: ProxyScheme
    country: ProxyCountry
    date: datetime.datetime
    date_end: datetime.datetime
    unixtime: int
    unixtime_end: int
    descr: str
    active: bool

    @property
    def proxy_link(self):
        if self.type == ProxyScheme.HTTPS:
            return f"http://{self.user}:{self.pswd}@{self.host}:{self.port}"
        elif self.type == ProxyScheme.SOCKS5:
            return f"socks5://{self.user}:{self.pswd}@{self.host}:{self.port}"

class ProxyList(BaseModel):
    '''
    Contains list of your proxies (dict format)

    Attributes
    ----------
    list_count (int):
        Amount of proxies (on page)
    list (Dict[str, Proxy]):
        Dictionary with keys representing proxy IDs and value representing proxy information (Proxy)
    '''
    list_count: int
    list: Dict[int, Proxy]

class ProxyListNokey(BaseModel):
    '''
    Contains list of your proxies (list format)

    Attributes
    ----------
    list_count (int):
        Amount of proxies (on page)
    list (List[Proxy]):
        List of proxies
    '''
    list_count: int
    list: List[Proxy]


class NewProxy(BaseModel):
    '''
    Contains full information about proxy

    Attributes
    ----------
    id (int):
        Proxy ID
    ip (str):
        Proxy IP
    host (str):
        Proxy Host
    port (str):
        Proxy Port
    user (str):
        Proxy Auth User
    pass (str):
        Proxy Auth Password
    type (str):
        Proxy scheme
    date (str):
        Proxy issue date
    date_end (str):
        Proxy expiration date
    unixtime (int):
        Proxy issue date in unixtime
    unixtime_end (int):
        Proxy epxiration date in unixtime
    active (int):
        1 - proxy is active, 0 - proxy is inactive
    '''
    id: int
    ip: str
    host: str
    port: str
    user: str
    pswd: str = Field(alias='pass')
    type: ProxyScheme
    date: datetime.datetime
    date_end: datetime.datetime
    unixtime: int
    unixtime_end: int
    active: bool

    @property
    def proxy_link(self):
        if self.type == ProxyScheme.HTTPS:
            return f"http://{self.user}:{self.pswd}@{self.host}:{self.port}"
        elif self.type == ProxyScheme.SOCKS5:
            return f"socks5://{self.user}:{self.pswd}@{self.host}:{self.port}"

class NewProxyList(BaseModel):
    '''
    Contains list of just bought proxies (dict format)

    Attributes
    ----------
    count (int):
        Amount of proxies
    price (float): 
        Total cost
    price_single (float):
        Price of one proxy
    period (int):
        Given period (days)
    country (str):
        Country Code of proxies
    list (Dict[str, NewProxy]):
        Dictionary with keys representing proxy IDs and value representing new proxy information (NewProxy)
    '''
    count: int
    price: float
    period: int
    country: ProxyCountry
    list: Dict[int, NewProxy]

class NewProxyListNokey(BaseModel):
    '''
    Contains list of just bought proxies (list format)

    Attributes
    ----------
    count (int):
        Amount of proxies
    price (float): 
        Total cost
    price_single (float):
        Price of one proxy
    period (int):
        Given period (days)
    country (str):
        Country Code of proxies
    list (List[NewProxy]):
        List of new proxies
    '''
    count: int
    price: float
    period: int
    country: ProxyCountry
    list: List[NewProxy]


class Prolong(BaseModel):
    '''
    Contains information about proxy prolonging

    Attributes
    ----------
    id (int):
        Proxy ID
    date_end (datetime.datetime):
        New proxy expiration date
    unixtime_end (int):
        New proxy expiration date in unixformat
    '''
    id: int
    date_end: datetime.datetime
    unixtime_end: int

class ProlongList(BaseModel):
    '''
    Contains list of prolongs

    Attributes
    ----------
    price (float): 
        Total cost
    period (int):
        Given period (days)
    count (int):
        Amount of proxies
    list (Dict[str, Prolong]):
        Dictionary with keys representing proxy IDs and value representing prolong information (Prolong)
    '''
    price: float
    period: int
    count: int
    list: Dict[int, Prolong]

class ProlongListNokey(BaseModel):
    '''
    Contains list of prolongs

    Attributes
    ----------
    price (float): 
        Total cost
    period (int):
        Given period (days)
    count (int):
        Amount of proxies
    list (List[Prolong]):
        List of Prolongs
    '''
    price: float
    period: int
    count: int
    list: List[Prolong]
