from concurrent.futures import ThreadPoolExecutor

import requests
from http import HTTPStatus
import logging


class RequestClass:
    """RequestClass"""

    def start_query(self, url, **kwargs):
        logging.info(f"Request: {url}")
        print(f"Request: {url}")

        try:
            response = requests.request(method='GET',
                                        url=url,
                                        params=kwargs,
                                        timeout=10)
        except Exception as e:
            print(e)
            raise e
        status_code = response.status_code

        logging.info(f"Request: {url}, code={status_code}")
        print(f"Request: {url}, code={status_code}")

        if HTTPStatus.OK != status_code:
            return
        return response.content

import time
executor = ThreadPoolExecutor(max_workers=2)

def put_query(*args, **kwargs):
    executor.submit(RequestClass().start_query, *args, **kwargs)


put_query('http://google.com', k=1)
put_query('http://python.org', k=3)
put_query('http://rx.js', k=2)

while True:
    put_query('http://google.com', k=1)
    put_query('http://python.org', k=3)
    put_query('http://rx.js', k=2)

