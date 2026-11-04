import time, random, json, hashlib
from urllib     import parse
from pathlib    import Path
from enum       import IntEnum
from typing     import get_args
from urllib.parse import urlencode, urljoin
from curl_cffi  import Session, Request, Response, BrowserTypeLiteral

DATA = Path(__file__).parent / 'data'

class NotFound (Exception): ...

class Time (IntEnum):
    WAIT    = 10
    REFRESH = 5
    BETWEEN = 2

class Scraper:
    browser:    BrowserTypeLiteral
    session:    Session
    root:       str

    def __init__(self, root: str):
        self.browser = random.choice(get_args(BrowserTypeLiteral))
        self.session = Session(impersonate = self.browser)
        self.root    = root
        self.token()
    
    def get(self, url: str, params: dict | None = None) -> str:
        print(url)
        params = params or {}
        prepared = Request(url=f'{url}?{urlencode(params)}', headers=self.session.headers, method='GET')

        if self.file(prepared).exists():
            return self.retrieve(prepared)

        response = self.session.get(prepared.url, headers={"Referer": url})

        self.update()

        match response.status_code:
            case 200:
                print('200')
                self.save(prepared, response)
            case 400:
                print('400')
                self.token()
                return self.get(url, params)
            case 404:
                print('404')
                raise NotFound()
            case 429:
                print('429')
                time.sleep(Time.WAIT)
                return self.get(url, params)
            
        time.sleep(Time.BETWEEN)
        return response.text

    def token(self):
        time.sleep(Time.REFRESH)
        self.browser = random.choice(get_args(BrowserTypeLiteral))
        self.session = Session(impersonate = self.browser)
        self.session.get(self.root)
        self.update()

    def update(self):
        if token := self.session.cookies.get("X-XSRF-TOKEN") or self.session.cookies.get("XSRF-TOKEN"):
            self.session.headers.update({
                "X-XSRF-TOKEN":     parse.unquote(token),
                "Accept":           "application/json, text/plain, */*",
                "Content-Type":     "application/json",
                "Cache-Control":    "no-cache",
                "Pragma":           "no-cache",
                "Accept-Language":  "en-US,en;q=0.9",
            })

    def file(self, prepared: Request) -> Path:
        hash = hashlib.sha256(prepared.url.encode()).hexdigest()
        return DATA / f'{hash}.json'

    def save(self, prepared: Request, retreived: Response):
        DATA.mkdir(exist_ok=True)
        self.file(prepared).write_text(retreived.text)

    def retrieve(self, prepared: Request) -> str:
        return self.file(prepared).read_text()