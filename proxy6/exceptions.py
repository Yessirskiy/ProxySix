class BadRequest(Exception):
    def __init__(self, message):       
        self.message = message    
        super().__init__(message)

class InvalidAPIKey(BadRequest):
    '''Raised when provided API Key is invalid'''
    pass

class InvalidIP(BadRequest):
    '''Raised when API was accessed from an incorrect IP'''
    pass

class InvalidMethod(BadRequest):
    '''Raised when wrong (non-existant) API method was called'''
    pass

class InvalidCount(BadRequest):
    '''Raised when wrong proxies quantity, wrong amount or no quantity input'''
    pass

class InvalidPeriod(BadRequest):
    '''Raised when period error, wrong period input (days) or no input'''
    pass

class InvalidCountry(BadRequest):
    '''Raised when country error, wrong country input (iso2 for country input) or no input'''
    pass

class InvalidProxyIDs(BadRequest):
    '''Raised when error of the list of the proxy numbers. Proxy numbers have to divided with comas'''
    pass

class InvalidVersion(BadRequest):
    '''Raised when proxy version is specified incorrectly'''
    pass

class InvalidDescription(BadRequest):
    '''Raised when tech description error'''
    pass

class InvalidType(BadRequest):
    '''Raised when proxy type (protocol) error. Incorrect or missing'''
    pass

class ProxiesUnavailable(BadRequest):
    '''Raised after attempt of purchase of more proxies than available on the service'''
    pass

class InsufficientFunds(BadRequest):
    '''Raised when not enough funds on your account'''
    pass

class ElementNotFound(BadRequest):
    '''Raised when the requested item was not found'''
    pass

class PriceError(BadRequest):
    '''Raised when total cost is less than or equal to zero'''
    pass

class UnknownError(BadRequest):
    '''Raised when unknow error occured'''
    pass