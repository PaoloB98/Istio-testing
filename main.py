import logging
import sys
from time import sleep
from http_device import HTTPDevice, Zone
from k8s_manager import *
from tcp_device import TCPDevice


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")


def main() -> int:
    logger.info("Starting...")

    #case_a_tcp()
    case_b_tcp()
    #case_a_http()
    #case_b_http()
    #case_c_http()

    return 0


def case_a_http():
    # Resetting to product page rule
    update_http_route("bookinfo-a", "productpage", 9080)
    sleep(0.5)

    device = HTTPDevice(url_for_request="http://192.168.254.213/productpage")
    # Richieste continue.
    device.continuous_requesting(time_seconds=5, interval_between_req=0.05)

    sleep(1)
    update_http_route("bookinfo-a", "nginx-serv", 80)
    device.thread.join()


def case_a_tcp():
    # Resetting zone A for tcp
    update_tcp_route("iperf-tcp-a", "iperf-service-a", 5201)
    sleep(0.5)

    device = TCPDevice('192.168.254.238', "Device 1")
    # Richieste continue.
    device.start_iperf_test(30)

    sleep(5)
    update_tcp_route("iperf-tcp-a", "iperf-service-b", 5201)
    device.process.join()
    update_tcp_route("iperf-tcp-a", "iperf-service-a", 5201)

def case_b_http():
    # PRESET
    # Resetting zone A http rule
    update_http_route("bookinfo-a", "productpage", 9080)
    # Resetting zone B http rule
    update_http_route("bookinfo-b", "nginx-serv", 80)
    # Deleting rule on zone B
    deleted_rule = delete_http_rule("bookinfo-b")

    # Starting device HTTP
    sleep(0.5)
    device = HTTPDevice(url_for_request="http://192.168.254.213/productpage")
    # Continuous requests
    device.continuous_requesting(time_seconds=20, interval_between_req=0.1)

    sleep(7)
    # Moving device to zone B
    device.change_device_zone(Zone.B)
    logger.info("#################Device zone has changed-!-!-!-!####################")
    # Creating the deleted rule to point zone B
    logger.info("Creating rule for zone B")
    recreated_rule = create_http_rule(deleted_rule)
    device.thread.join()

def case_b_tcp():
    # Resetting zone A for TCP
    update_tcp_route("iperf-tcp-a", "iperf-service-a", 5201)
    # Resetting zone B for TCP
    update_tcp_route("iperf-tcp-b", "iperf-service-b", 5201)
    deleted_route = delete_tcp_route("iperf-tcp-b")
    # Give time to k8s to update
    sleep(0.5)

    device1 = TCPDevice('192.168.254.238', "Device 1")
    device1.start_iperf_test(35)
    device1.process.join() # Wait for the test to finish
    logger.info("Finish")

    create_tcp_route(deleted_route)
    device1.change_device_zone(Zone.B)
    sleep(0.2)
    device1.start_iperf_test(25)
    device1.process.join()
    logger.info("Finish")

    logger.info("Case B TCP ENDED")

def case_c_http():
    # PRESET
    # Resetting zone A http rule
    update_http_route("bookinfo-a", "productpage", 9080)
    # Resetting zone B http rule
    update_http_route("bookinfo-b", "nginx-serv", 80)

    # Starting device HTTP
    sleep(0.5)
    device = HTTPDevice(url_for_request="http://192.168.254.213/productpage")
    # Continuous requests
    device.continuous_requesting(time_seconds=20, interval_between_req=0.1)

    sleep(7)
    # Moving device to zone B
    device.change_device_zone(Zone.B)
    logger.info("#################Device zone has changed-!-!-!-!####################")
    device.thread.join()

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit


