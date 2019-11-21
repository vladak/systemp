#!/usr/bin/env python3
"""
Acquire CPU temperature and present it via HTTP for Prometheus server.
"""

import logging
import sys
import time
import socket
from prometheus_client import start_http_server, Gauge


EXPOSED_PORT = 8222   # port to listen on for HTTP requests


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    logger.info("Listening on port " + str(EXPOSED_PORT))
    start_http_server(EXPOSED_PORT)

    sleep_seconds = 5

    hostname = socket.gethostname().split(".")[0]
    g = Gauge('CPU_temp_' + hostname, 'CPU temperature on ' + hostname)

    while True:
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            val = f.read()
            if len(val) == 0:
                logger.debug("Empty read")
                continue

        temp = float(val) / 1000
        logger.debug(temp)
        g.set(temp)

        logger.debug("Sleeping for " + str(sleep_seconds) + " seconds")
        time.sleep(sleep_seconds)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
