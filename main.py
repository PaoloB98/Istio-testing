import logging
import sys
from device import Device

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")
logger.addHandler(logging.StreamHandler(sys.stdout))


def main() -> int:
    logger.info("Starting...")
    # Qua è dove parte l'eseguzione del software
    device_n1 = Device(url_for_request="http://example.com")
    # Richieste continue, vedi console per codice stato richieste.
    device_n1.continuous_requesting(time_seconds=30, interval_between_req=5)

    return 0


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
