import logging
from pprint import pprint
import iperf3
from threading import RLock, Thread
from iperf3 import Client
from requests import Response
from zone import Zone

logger = logging.getLogger("Device")


class TCPDevice:
    remote_host: str
    lock: RLock
    thread: Thread
    port: int
    zone: Zone
    client: Client

    def __init__(self, remote_host: str):
        super().__init__()
        self.lock = RLock()
        self.zone = Zone.A
        self.port = 5201

        client = iperf3.Client()
        client.server_hostname = remote_host
        client.verbose = False
        client.reverse = False
        client.num_streams = 10
        client.bandwidth = 1000000000

        self.client = client

    def change_device_zone(self, zone: Zone):
        self.lock.acquire()
        self.zone = zone
        if self.zone == Zone.A:
            self.port = 5201
        else:
            self.port = 5202
        self.lock.release()

    def start_iperf_test(self, time_seconds: int):
        self.thread = Thread(target=self._iperf_test, args=[time_seconds])
        self.thread.start()

    def _iperf_test(self, time_seconds: int):
        self.client.duration = time_seconds
        self.lock.acquire()
        self.client.port = self.port
        self.lock.release()
        # Run iperf3 test
        result = self.client.run()

        # extract relevant data
        sent_mbps = int(result.sent_Mbps)
        received_mbps = int(result.received_Mbps)

        logger.info(f"\n    Sent Mbps:{sent_mbps} \n    Received Mbps:{received_mbps}")

    def analyze_request_result(self, result: Response):
        """
        Reads the response and analyze it
        """
        if result.text.find("Simple Bookstore") == -1:
            logger.info("NGINX has responded")
        elif result.status_code == 200:
            logger.info("Bookinfo has responded")
        else:
            logger.info("Unrecognized responded")
