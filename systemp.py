#!/usr/bin/env python3
"""
Acquire CPU temperature and publish it to MQTT.
"""

import argparse
import json
import logging
import socket
import ssl
import sys
import time

import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_minimqtt.adafruit_minimqtt import MMQTTException

from logutil import LogLevelAction


def parse_args():
    """
    Parse command line arguments
    """

    parser = argparse.ArgumentParser(
        description="Publish system temperature to MQTT",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mqtt_hostname",
        help="MQTT broker hostname",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        action=LogLevelAction,
        help='Set log level (e.g. "ERROR")',
        default=logging.INFO,
    )
    parser.add_argument(
        "-t",
        "--timeout",
        help="Timeout in seconds to sleep between publishing",
        default=5,
    )
    parser.add_argument(
        "-p",
        "--port",
        help="MQTT broker port",
        default=1883,
    )
    parser.add_argument(
        "--mqtt_topic",
        help="MQTT topic to publish to",
        required=True,
    )

    return parser.parse_args()


def main():
    """
    read system temperature and publish to MQTT in a cycle
    """
    args = parse_args()

    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(args.loglevel)

    mqtt = MQTT.MQTT(
        broker=args.mqtt_hostname,
        port=args.mqtt_port,
        socket_pool=socket,
        ssl_context=ssl.create_default_context(),
    )
    logger.info(f"Connecting to MQTT broker {args.mqtt_hostname} on port {args.mqtt_port}")
    mqtt.connect()

    while True:
        # Make sure to stay connected to the broker e.g. in case of keep alive.
        try:
            mqtt.loop(1)
        except MMQTTException as mqtt_exc:
            logger.warning(f"Got MQTT exception: {mqtt_exc}")
            mqtt.reconnect()

        with open(
            "/sys/class/thermal/thermal_zone0/temp", encoding="ascii"
        ) as file_handle:
            val = file_handle.read()
            if len(val) == 0:
                logger.debug("Empty read")
                continue

        temp_val = float(val) / 1000
        logger.debug(f"Current system temperature: {temp_val}")
        mqtt_payload_dict = {"sys_temperature": temp_val}

        try:
            mqtt.publish(args.mqtt_topic, json.dumps(mqtt_payload_dict))
        except MMQTTException as mqtt_exc:
            logger.warning(f"Got MQTT exception: {mqtt_exc}")
            mqtt.reconnect()

        logger.debug(f"Sleeping for {args.timeout} seconds")
        time.sleep(args.timeout)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
