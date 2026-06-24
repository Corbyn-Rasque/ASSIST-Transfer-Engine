import time, random
from typing     import get_args
from urllib     import parse
from enum       import IntEnum, StrEnum
from curl_cffi  import requests, Response, BrowserTypeLiteral

from sources.web.area       import Area
from sources.web.courses    import Course

class NotFound (Exception): ...

class Time (IntEnum):
    WAIT    = 60
    REFRESH = 10
    BETWEEN = 5

class Scraper:
    browser:    BrowserTypeLiteral
    session:    requests.Session
    root:       str

    def __init__(self, root: str):
        self.browser = random.choice(get_args(BrowserTypeLiteral))
        self.session = requests.Session()
        self.root    = root
        self.get(root)

    def get(self, url: str, params: dict | None = None) -> Response:
        params = params or {}
        response: Response = self.session.get(url, params = params)

        self.update()

        match response.status_code:
            case 400:
                self.token()
                return self.get(url, params)
            case 404:
                raise NotFound()
            case 429:
                time.sleep(Time.WAIT)
                return self.get(url, params)

        time.sleep(Time.BETWEEN)
        return response
    
    def token(self):
        time.sleep(Time.REFRESH)
        self.session = requests.Session()
        self.session.get(self.root)
        self.update()

    def update(self):
        if token := self.session.cookies.get("X-XSRF-TOKEN") or self.session.cookies.get("XSRF-TOKEN"):
            self.session.headers.update({
                "X-XSRF-TOKEN": parse.unquote(token),
                "Accept": "application/json, text/plain, */*",
            })

