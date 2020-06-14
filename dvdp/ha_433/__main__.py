import argparse
import asyncio
import logging
from pathlib import Path

from dvdp.ha_433 import HA433Light
from dvdp.recorder_433 import RECORDINGS_DIR, get_recordings
from dvdp.ha_mqtt.client import MQTTClient


def exception_handler(loop, context):
    loop.default_exception_handler(context)
    logging.error(context)
    loop.stop()


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
    )
    parser = argparse.ArgumentParser(
        'Allow Home assistant to control 433 devices over MQTT.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        'brokerip',
        help=f'IP of broker.',
        type=str
    )
    parser.add_argument(
        '--name',
        '-n',
        help=f'Name of client.',
        default='devices_433',
        type=str
    )
    parser.add_argument(
        '--username',
        '-u',
        help='Username to use when connecting to MQTT broker.',
        type=str,
    )
    parser.add_argument(
        '--password',
        '-p',
        help='Password to use when connecting to MQTT broker.',
        type=str,
    )
    parser.add_argument(
        '--pin',
        default=14,
        help='BCM pin on rasberry pi used for transmission',
        type=int,
    )
    parser.add_argument(
        '--recordings',
        '-r',
        help='Directory containing recordings.',
        type=Path,
        default=RECORDINGS_DIR,
    )

    args = parser.parse_args()
    broker_ip = args.brokerip
    client_name = args.name
    pin = args.pin
    source_dir = args.recordings
    recordings = get_recordings(source_dir)
    username = args.username
    password = args.password

    mqtt_client = MQTTClient(broker_ip, client_name, username, password)
    devices = [
        HA433Light(name, mqtt_client, pin, source_dir)
        for name in recordings.keys()
    ]

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(device.start())
        for device in devices
    ]
    loop.set_exception_handler(exception_handler)
    loop.run_until_complete(
        asyncio.gather(
            *tasks,
            return_exceptions=True,
        )
    )


if __name__ == '__main__':
    main()
