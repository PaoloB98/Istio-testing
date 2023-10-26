import logging
import requests
import time
from threading import RLock, Thread

logger = logging.getLogger("Device")


class Device:
    url_for_requests: str  # URL used for requesting
    zone: int
    lock: RLock
    thread: Thread

    def __init__(self, url_for_request):
        super().__init__()
        self.lock = RLock()
        self.url_for_requests = url_for_request

    def _request(self, time_seconds: int, interval_between_req: int):
        n_of_request = int(time_seconds / interval_between_req)

        for request_number in range(1, n_of_request):
            logger.info(f"Request n. {request_number}")
            result = requests.get(url=self.url_for_requests)
            logger.info(f"Response status: {result.status_code}\n----\n")
            time.sleep(interval_between_req)

    def continuous_requesting(self, time_seconds: int, interval_between_req: int):
        self.thread = Thread(target=self._request, args=[time_seconds, interval_between_req])
        self.thread.start()

    def change_zone(self):
        """
        Invert the zone of the device, suppose only 2 zones.
        :return:
        """
        self.lock.acquire()
        if self.zone == 0:
            self.zone = 1
        else:
            self.zone = 0
        self.lock.release()
