import logging
import requests
import time
from threading import RLock, Thread
from requests import Response
from zone import Zone
logger = logging.getLogger("Device")
import logging
logging.getLogger("requests").setLevel(logging.ERROR)



class HTTPDevice:
    url_for_requests: str  # URL used for requesting
    zone: Zone
    lock: RLock
    thread: Thread
    headers: dict

    def __init__(self, url_for_request):
        super().__init__()
        self.lock = RLock()
        self.url_for_requests = url_for_request
        self.headers = {'zone': 'A'}

    def change_device_zone(self, zone: Zone):
        self.lock.acquire()
        self.zone = zone
        if self.zone == Zone.A:
            self.headers['zone'] = 'A'
        else:
            self.headers['zone'] = 'B'
        self.lock.release()

    def _request(self, time_seconds: int, interval_between_req: int):
        """
        Performs continuously a GET request to the URL in the Device (self.url)
        :param time_seconds: The total time
        :param interval_between_req: Interval between requests
        :return:
        """
        n_of_request = int(time_seconds / interval_between_req)

        for request_number in range(1, n_of_request):
            logger.info(f"Request n. {request_number}")
            self.lock.acquire()
            http_result: Response = requests.get(url=self.url_for_requests, headers=self.headers)
            self.lock.release()
            self.analyze_request_result(http_result)
            logger.info(f"Response status: {http_result.status_code}\n----\n")
            time.sleep(interval_between_req)

    def continuous_requesting(self, time_seconds: int, interval_between_req: float):
        self.thread = Thread(target=self._request, args=[time_seconds, interval_between_req])
        self.thread.start()

    def analyze_request_result(self, result: Response):
        """
        Reads the response and analyze it
        """
        if result.status_code == 200:
            if result.text.find("Simple Bookstore") == -1:
                logger.info("NGINX has responded")
            else:
                logger.info("Bookinfo has responded")
        else:
            logger.error("Unrecognized responded")
