# Scrapy Manipulate Request Downloader Middleware

This is an async scrapy request downloader middleware, support random request and response manipulation.

With this, you can do any change to the reqeust and response in an easy way, you can send request by tls_client, 

pyhttpx, requests-go, etc. You can even manipulate chrome by selenium, undetected_chrome, playwright, etc. without

any thinking of the async logic behind the scrapy.

## Installation

```shell script
pip3 install scrapy-manipulate-request
```

## Usage

You need to enable `ManipulateRequestDownloaderMiddleware` in `DOWNLOADER_MIDDLEWARES` first:

```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy_manipulate_request.downloadermiddlewares.ManipulateRequestDownloaderMiddleware': 543,
}
```

Notice, this middleware is async, that means it is affected by some scrapy settings, such as:

```python
CONCURRENT_REQUESTS = 16

```

To manipulate request and response, it is very simple and convenient, just add manipulate_request function

in your spider, and send it to the meta, it's something like parse function.

```python
import scrapy

class TestSpider(scrapy.Spider):
    name = "test"

    def start_requests(self,):
        meta_data = {'manipulate_request', self.manipulate_request}
        yield scrapy.Request(url="https://tls.browserleaks.com/json", meta=meta_data)
    
    def manipulate_request(self, request, spider):
    
        # return None, the requesst will be ignored
        # return scrapy.http.HtmlResponse or scrapy.http.TextResponse object,
        # the process of handle response will be started.
        pass
    
    def parse(self, response):
        pass
```

## Useful Example

### Send request by tls_client in order to bypass ja3 verification

```python
import scrapy
import tls_client
from scrapy.http import TextResponse

class TestSpider(scrapy.Spider):
    name = "test"

    def start_requests(self,):
        meta_data = {'manipulate_request', self.manipulate_request}
        yield scrapy.Request(url="https://tls.browserleaks.com/json", meta=meta_data)
    
    def manipulate_request(self, request, spider):
        url = request.url
        headers = request.headers.to_unicode_dict()
        tls_session = tls_client.Session(
            client_identifier='chrome_112',
            random_tls_extension_order=True
        )
        proxy = 'http://username:password@ip:port'
        raw_response = tls_session.get(url=url, headers=headers, proxy=proxy)
        response = TextResponse(url=request.url, status=raw_response.status_code, headers=raw_response.headers,
                                body=raw_response.text, request=request, encoding='utf-8')
        return response
        
        # return None, the requesst will be ignored
        # return scrapy.http.HtmlResponse or scrapy.http.TextResponse object,
        # the process of handle response will be started.
    
    def parse(self, response):
        pass
```

More and detailed tls_client usage see [Python-Tls-Client](https://github.com/FlorianREGAZ/Python-Tls-Client).

### Use undetected chrom to operate webpage

```python
import scrapy
from pprint import pformat
from scrapy.http import HtmlResponse
from seleniumwire import undetected_chromedriver as uc

class TestSpider(scrapy.Spider):
    name = "test"

    def start_requests(self,):
        meta_data = {'manipulate_request', self.manipulate_request}
        yield scrapy.Request(url="https://tls.browserleaks.com/json", meta=meta_data)
    
    def manipulate_request(self, request, spider):
        chrome_options = uc.ChromeOptions()
        chrome_options.add_experimental_option()
        chrome_options.add_argument()
        chrome_options.add_extension()
        seleniumwire_options = {
            'proxy': {
                'http': 'http://username:password@ip:port',
                'https': 'https://username:password@ip:port',
            }
        }
        browser = uc.Chrome(version_main=108, options=chrome_options, seleniumwire_options= seleniumwire_options,
                            headless=True, enable_cdp_events=True)
        browser.set_page_load_timeout(10)
        browser.maximize_window()
        browser.add_cdp_listener('Network.requestWillBeSent', self.mylousyprintfunction)
        browser.execute_script()
        browser.execute_cdp_cmd()
        browser.request_interceptor = self.request_interceptor
        browser.get("https://tls.browserleaks.com/json")
        elements = browser.find_elements()
        ...
        raw_response = browser.page_source
        response = HtmlResponse(url=request.url, status=200, body=raw_response, request=request, encoding='utf-8')
        return response
        # return None, the requesst will be ignored
        # return scrapy.http.HtmlResponse or scrapy.http.TextResponse object,
        # the process of handle response will be started.

    def mylousyprintfunction(self, message):
        print(pformat(message))

    def request_interceptor(self, request):
        request.headers['New-Header'] = 'Some Value'
        del request.headers['Referer']
        request.headers['Referer'] = 'some_referer'
```

More and detailed chrome operations see [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
and [selenium-wire](https://github.com/wkeeling/selenium-wire).