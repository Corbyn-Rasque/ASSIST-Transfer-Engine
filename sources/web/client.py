import time, random, hashlib, logging
from urllib         import parse
from pathlib        import Path
from enum           import IntEnum
from typing         import get_args
from urllib.parse   import urlencode
from curl_cffi      import Session, BrowserTypeLiteral

log = logging.getLogger(__name__)

DATA    = Path(__file__).parent / 'data'
RETRIES = 3

class ResponseError (Exception):
    '''Raised when ASSIST answers with a status the client can't recover from.'''

    def __init__(self, status: int, url: str, attempts: int = 1):
        self.status     = status
        self.url        = url
        self.attempts   = attempts
        super().__init__(f'{status} from {url}' + (f' after {attempts} attempts' if attempts > 1 else ''))

class NotFound (ResponseError):
    def __init__(self, url: str):
        super().__init__(404, url)

class Time (IntEnum):
    WAIT    = 10
    REFRESH = 5
    BETWEEN = 2

class Client:
    '''
    Fetches JSON from the ASSIST website, caching every successful response on disk.

    No network calls happen until the first request that misses the cache, so
    creating a client is free, and cached data can be read entirely offline.
    '''
    browser:    BrowserTypeLiteral | None
    session:    Session | None
    root:       str

    def __init__(self, root: str):
        self.browser = None
        self.session = None
        self.root    = root

    def get(self, url: str, params: dict | None = None) -> str:
        address = f'{url}?{urlencode(params or {})}'

        if (cached := self.file(address)).exists():
            log.debug('Cache hit: %s', address)
            return cached.read_text()

        for attempt in range(1, RETRIES + 1):
            session = self.session or self.token()

            log.debug('GET %s (attempt %d of %d)', address, attempt, RETRIES)
            response = session.get(address, headers = {'Referer': url})
            self.update()

            match response.status_code:
                case 200:
                    self.save(address, response.text)
                    time.sleep(Time.BETWEEN)
                    return response.text
                case 400 | 429 if attempt == RETRIES:
                    break
                case 400:
                    log.warning('400 from %s; refreshing session token', address)
                    self.token()
                case 404:
                    raise NotFound(address)
                case 429:
                    log.warning('Rate limited on %s; waiting %ds', address, Time.WAIT * attempt)
                    time.sleep(Time.WAIT * attempt)
                case status:
                    raise ResponseError(status, address)

        raise ResponseError(response.status_code, address, attempts = RETRIES)

    def token(self) -> Session:
        '''Starts a fresh session and picks up a new XSRF token from the site root.'''
        time.sleep(Time.REFRESH)
        self.browser = random.choice(get_args(BrowserTypeLiteral))
        self.session = Session(impersonate = self.browser)
        self.session.get(self.root)
        self.update()
        return self.session

    def update(self):
        if self.session is None:
            return
        if token := self.session.cookies.get("X-XSRF-TOKEN") or self.session.cookies.get("XSRF-TOKEN"):
            self.session.headers.update({
                "X-XSRF-TOKEN":     parse.unquote(token),
                "Accept":           "application/json, text/plain, */*",
                "Content-Type":     "application/json",
                "Cache-Control":    "no-cache",
                "Pragma":           "no-cache",
                "Accept-Language":  "en-US,en;q=0.9",
            })

    def file(self, address: str) -> Path:
        hash = hashlib.sha256(address.encode()).hexdigest()
        return DATA / f'{hash}.json'

    def save(self, address: str, text: str):
        DATA.mkdir(exist_ok = True)
        self.file(address).write_text(text)
