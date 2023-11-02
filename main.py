import logging
import sys
from device import Device
from k8s_manager import update_tcp_route, update_http_route

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")
#logger.addHandler(logging.StreamHandler(sys.stdout))


def main() -> int:
    logger.info("Starting...")
    # Qua è dove parte l'eseguzione del software

    #device_n1 = Device(url_for_request="http://192.168.254.213/productpage")
    # Richieste continue.
    #device_n1.continuous_requesting(time_seconds=150, interval_between_req=3)

    # Changing the TCP rule from serv-a to serv-b
    update_tcp_route()

    # To be completed
    update_http_route()

    # Aspetta che il processo figlio finisca (il dispositivo che fa richieste)
    #device_n1.thread.join()

    return 0


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
