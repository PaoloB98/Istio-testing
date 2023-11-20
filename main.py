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

    case_b_tcp()

    return 0


def case_a_http():
    # Resetting to product page rule
    update_http_route("bookinfo-a", "productpage", 9080)
    sleep(0.5)

    device = HTTPDevice(url_for_request="http://192.168.254.213/productpage")
    # Richieste continue.
    device.continuous_requesting(time_seconds=40, interval_between_req=0.5)

    sleep(5)
    update_http_route("bookinfo-a", "nginx-serv", 80)
    device.thread.join()


def case_a_tcp():
    # Resetting zone A for tcp
    update_tcp_route("iperf-tcp-a", "iperf-service-a", 5201)
    sleep(0.5)

    device = TCPDevice('192.168.254.238')
    # Richieste continue.
    device.start_iperf_test(10)

    sleep(5)
    update_tcp_route("iperf-tcp-a", "iperf-service-b", 5201)
    device.thread.join()
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
    device.continuous_requesting(time_seconds=3, interval_between_req=0.1)

    sleep(1)
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

    device1 = TCPDevice('192.168.254.238')
    device1.start_iperf_test(10)
    sleep(3)
    device1.change_device_zone(Zone.B) # It is not doing anything for now once the test has already started.

    # Wait before moving the device
    sleep(25)
    create_tcp_route(deleted_route)

    device2 = TCPDevice('192.168.254.238')
    device2.change_device_zone(Zone.A) # Starting a new dev on zone B
    device2.start_iperf_test(20)

    device1.thread.join()
    device2.thread.join()
    logger.info("Case B TCP ENDED")

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
