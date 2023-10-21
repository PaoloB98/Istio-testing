import logging

import requests
import time

class Device():
    url_for_requests: str # URL used for requesting

    def __init__(self, url_for_request):
        super().__init__()
        self.url_for_requests = url_for_request

    def continuous_requesting(self, time_seconds: int, interval_between_req: int):
        n_of_request = int(time_seconds/interval_between_req)

        for request_number in range(1,n_of_request):
            logging.info(f"Request n. {request_number}")
            result = requests.get(url=self.url_for_requests)
            time.sleep(interval_between_req)
