from .exceptions import *
from .types import *
import datetime, aiohttp

class ProxySix():
    '''Class to work with proxy provider API proxy6.net'''
    URL = "https://proxy6.net/api"

    def __init__(self, api_key: str) -> None:
        '''
        Initialize instance of ProxyService

        Parameters
        ----------
        api_key (str):
            API key from proxy6.net (`https://proxy6.net/en/user/developers`)
        '''
        self.api_key: str = api_key
        self.user_id: int = None
        self.balance: float = None
        self.currency: Currency = None
        self.date_mod: datetime.datetime = None

    async def _private_request(self, method: str, params: dict) -> dict:
        url = f"{self.URL}/{self.api_key}/{method}/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as r:
                if r.status == 200:
                    data = await r.json()
                    status = data.get("status", None)
                    if status == "yes" or status == "no":
                        return data
                return None
                                     
    def _extract_data(self, data: dict, method: str):
        if data is None:
            raise UnknownError("Invalid Request")
        
        if data.get("user_id", None) is not None:
            self.user_id = int(data['user_id'])
            data.pop("user_id", None)
        if data.get("balance", None) is not None:
            self.balance = float(data['balance'])
            data.pop("balance", None)
        if data.get("currency", None) is not None:
            self.currency = Currency(data['currency'])
            data.pop("currency", None)
        if data.get("date_mod", None) is not None:
            self.date_mod = datetime.datetime.strptime(data["date_mod"], "%Y-%m-%d %H:%M:%S")
            data.pop("date_mod", None)

        if data.get("status") == "yes":
            data.pop("status", None)
            if method == "getprice":
                return Price(**data)
            elif method == "getcount":
                return int(data["count"])
            elif method == "getcountry":
                return list([ProxyCountry(code) for code in data["list"]])
            elif method == "getproxy":
                if isinstance(data["list"], dict):
                    return ProxyList(**data)
                else:
                    return ProxyListNokey(**data)
            elif method == "settype":
                return True
            elif method == "setdescr":
                return int(data["count"])
            elif method == "buy":
                if isinstance(data["list"], dict):
                    return NewProxyList(**data)
                else:
                    return NewProxyListNokey(**data)
            elif method == "prolong":
                if isinstance(data["list"], dict):
                    return ProlongList(**data)
                else:
                    return ProlongListNokey(**data)
            elif method == "delete":
                return int(data["count"])
            elif method == "check":
                return data["proxy_status"]
        
        
        else:
            data.pop("status", None)
            error_id = int(data.get("error_id", None))
            error_message = data.get("error", None)
            if error_id == 100:
                raise InvalidAPIKey(error_message)
            elif error_id == 105:
                raise InvalidIP(error_message)
            elif error_id == 110:
                raise InvalidMethod(error_message)
            elif error_id == 200:
                raise InvalidCount(error_message)
            elif error_id == 210:
                raise InvalidPeriod(error_message)
            elif error_id == 220:
                raise InvalidCountry(error_message)
            elif error_id == 230:
                raise InvalidProxyIDs(error_message)
            elif error_id == 240:
                raise InvalidVersion(error_message)
            elif error_id == 250:
                raise InvalidDescription(error_message)
            elif error_id == 260:
                raise InvalidType(error_message)
            elif error_id == 300:
                raise ProxiesUnavailable(error_message)
            elif error_id == 400:
                raise InsufficientFunds(error_message)
            elif error_id == 404:
                raise ElementNotFound(error_message)
            elif error_id == 410:
                raise PriceError(error_message)
            else:
                raise UnknownError(error_message)
    
    async def getPrice(self, count: int, period: int, version: ProxyVersion = ProxyVersion.IPv6) -> Price:
        '''
        Get information about the cost of the order, depending on the version, period and number of proxy

        Parameters
        ----------
        count (int):
            Number of proxies (Required)
        period (int):
            Number of days (Required)
        version (ProxyVersion):
            Proxy version (default: IPv6)

        Returns
        -------
            data (PriceDict)
        '''
        method = "getprice"
        params = {
            "count" : count,
            "period" : period,
            "version" : version.value
        }
        res = await self._private_request(method, params)
        return self._extract_data(res, method)
    
    async def getCount(self, country: ProxyCountry, version: ProxyVersion = ProxyVersion.IPv6) -> int:
        '''
        Get an information on amount of proxies available to purchase for a selected country

        Parameters
        ----------
        country (ProxyCountry):
            Country Code (Required)
        version (ProxyVersion):
            Proxy version (default: IPv6)

        Returns
        -------
            data (CountDict)
        '''
        method = "getcount"
        params = {
            "country" : country.value,
            "version" : version.value
        }
        res = await self._private_request(method, params)
        return self._extract_data(res, method)
    
    async def getCountry(self, version: ProxyVersion = ProxyVersion.IPv6) -> List[ProxyCountry]:
        '''
        Get information on available for proxies purchase countries

        Parameters
        ----------
        version (ProxyVersion):
            Proxy Version (default: IPv6)

        Returns
        -------
            data (CountryDict)
        '''
        method = "getcountry"
        params = {"version" : version.value}
        res = await self._private_request(method, params)
        return self._extract_data(res, method)
    
    async def getProxy(self, 
            state: ProxyState = ProxyState.all, 
            description: str = None, 
            nokey: bool = False, 
            page: int = 1, 
            limit: int = 1000) -> ProxyList | ProxyListNokey:
        '''
        Returns the list of your proxies

        Parameters
        ----------
        state (ProxyState):
            State of proxies to return (default - All)
        description (str):
            Technical comment you've entered when purchased proxy. 
            Proxies with exact same description will be returned (deafult - None)
        nokey (bool):
            True - proxies will be returned as list. False - proxies will be returned as dictionary (key - proxy id, value - proxy info)
        page (int):
            Page number to return (default - 1)
        limit (int):
            Limit of proxies to return (default - 1000; max. value)

        Returns
        -------
        data (ProxyList | ProxyListNokey):
            Information about proxies
        '''
        method = "getproxy"
        params = {
            "state" : state.value,
            "page" : page,
            "limit" : limit
        }
        if description is not None:
            params["descr"] = description
        if nokey:
            params["nokey"] = ""

        res = await self._private_request(method, params)
        return self._extract_data(res, method)
    
    async def setType(self, ids: List[int], type: ProxyScheme) -> bool:
        '''
        Changes the type (protocol) in the proxy list

        Parameters
        ----------
        ids (List[int]):
            List of proxy IDs to change type (Required)
        type (ProxyScheme):
            New scheme to be applied to chosen proxies (Required)

        Returns
        -------
        result (bool):
            True - succsefully changed type
        '''
        method = "settype"
        params = {
            "ids" : ",".join(map(str, ids)),
            "type" : type.value
        }
        res = await self._private_request(method, params)
        return self._extract_data(res, method)
    
    async def setDescription(self, new: str, old: str = None, ids: List[int] = None) -> int:
        '''
        Updates technical comments in the proxy list that was added when buying (method `buy`)

        Parameters
        ----------
        new (str):
            New description to set (Required)
        old (str):
            Old description to replace
        ids (List[int]):
            List of proxy IDs to set new description to

        *Either `old` or `ids` parameter must be set.

        Returns
        -------
        count (int) 
            Amount of proxies that were changed
        '''
        method = "setdescr"
        params = {
            "new" : new
        }
        if old is not None:
            params["old"] = old
        if ids is not None:
            params["ids"] = ",".join(map(str, ids))
        
        res = await self._private_request(method, params)
        return self._extract_data(res, method)
    
    async def buyProxy(self, 
        count: int, 
        period: int, 
        country: ProxyCountry, 
        version: ProxyVersion = ProxyVersion.IPv6, 
        type: ProxyScheme = ProxyScheme.HTTPS, 
        description: str = None, 
        auto_prolong: bool = False, 
        nokey: bool = False) -> NewProxyList | NewProxyListNokey:
        '''
        Used for proxy purchases

        Parameters
        ----------
        count (int):
            Amount of proxies to buy (Required)
        period (int):
            Period for which proxies are purchased in days (Required)
        country (ProxyCountry):
            Country of proxy (Required)
        version (ProxyVersion):
            Proxy Version (IPv4, IPv4Shared, IPv6)
        type (ProxyScheme):
            Proxy Scheme (http, socks)
        desciption (str):
            Technical description for proxy. (Max value 50 characters)
        auto_prolong (bool):
            True - prolong proxy automatically, False - do not prolong
        nokey (bool):
            True - proxies will be returned as list. False - proxies will be returned as dictionary (key - proxy id, value - proxy info)

        Returns
        -------
        data (NewProxyList | NewProxyListNokey):
            Information about just bought proxies
        '''
        method = "buy"
        params = {
            "count" : count,
            "period" : period,
            "country" : country.value,
            "version" : version.value,
            "type" : type.value,
        }
        if description is not None:
            params["descr"] = description
        
        if auto_prolong:
            params["auto_prolong"] = ""
        if nokey:
            params["nokey"] = ""

        res = await self._private_request(method, params)
        return self._extract_data(res, method)
    
    async def prolongProxy(self, period: int, ids: List[int], nokey: bool = False) -> ProlongList | ProlongListNokey:
        '''
        Used to extend existing proxies

        Parameters
        ----------
        period (int):
            Extension period in days (Required)
        ids (List[int]):
            List of proxy IDs to set new description to (Required)
        nokey (bool):
            True - proxies will be returned as list. False - proxies will be returned as dictionary (key - proxy id, value - proxy info)

        Returns
        -------
        data (ProlongList | ProlongListNokey)
            Information about prolongs
        '''
        method = "prolong"
        params = {
            "period" : period,
            "ids" : ",".join(map(str, ids))
        }
        if nokey:
            params["nokey"] = ""

        res = await self._private_request(method, params)
        return self._extract_data(res, method)
    
    async def deleteProxy(self, ids: List[int] = None, description: str = None) -> int:
        '''
        Used to delete proxies

        Parameters
        ----------
        ids (List[int]):
            List of proxy IDs to set new description to (Required)
        description (str):
            New description to set (Required)

        *Either `ids` or `description` parameter must be set.

        Returns
        -------
        data (int):
            Amount of just deleted proxies
        '''
        method = "delete"
        params = {}
        if ids is not None:
            params["ids"] = ",".join(map(str, ids))
        if description is not None:
            params["descr"] = description

        res = await self._private_request(method, params)
        return self._extract_data(res, method)
    
    async def checkProxy(self, id: int) -> bool:
        '''
        Used to check the validity of the proxy

        Parameters
        ----------
        ids (int):
            Proxy ID to check

        Returns
        -------
        data (bool):
            True - proxy is working. False - proxy is not working
        '''
        method = "check"
        params = {
            "ids" : id
        }

        res = await self._private_request(method, params)
        return self._extract_data(res, method)
