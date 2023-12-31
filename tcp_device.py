import logging
from multiprocessing import Process
import iperf3
from threading import RLock
from iperf3 import Client
from requests import Response
from zone import Zone

logger = logging.getLogger("Device")


class TCPDevice:
    device_name: str
    remote_host: str
    lock: RLock
    process: Process
    port: int
    zone: Zone
    client: Client

    def __init__(self, remote_host: str, device_name: str):
        super().__init__()
        self.lock = RLock()
        self.zone = Zone.A
        self.port = 5201
        self.device_name = device_name

        client = iperf3.Client()
        client.server_hostname = remote_host
        client.verbose = False
        client.reverse = False
        client.num_streams = 1
        client.bandwidth = 100000000

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
        logger.info("Starting Thread for iperf device")
        #self._iperf_test(time_seconds)
        self.process = Process(target=self._iperf_test, args=(time_seconds,))
        self.process.start()

    def _iperf_test(self, time_seconds: int):
        self.client.duration = time_seconds
        self.lock.acquire()
        self.client.port = self.port
        self.lock.release()
        logger.info(f"Starting iperf test on {self.client.server_hostname}:{self.client.port} (zone {self.zone}) for {time_seconds} sec")
        # Run iperf3 test
        result = self.client.run()

        # extract relevant data
        try:
            sent_mbps = int(result.sent_Mbps)
            received_mbps = int(result.received_Mbps)
            logger.info(f"\n    Sent Mbps:{sent_mbps} \n    Received Mbps:{received_mbps}")
        except AttributeError:
            logger.error(f"{self.device_name}: {result}")

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
