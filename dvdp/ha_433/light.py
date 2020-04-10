from pathlib import Path

from dvdp.transmitter_433 import transmit
from dvdp.ha_mqtt.light import HAMQTTLight
from dvdp.ha_mqtt.client import MQTTClient


class HA433Light:
    def __init__(
            self,
            name: str,
            mqtt_client: MQTTClient,
            pin: int,
            recording_dir: Path,
    ):
        self.__mqtt_light = HAMQTTLight(
            name,
            mqtt_client,
            self.__on_state_change,
        )
        self.__pin = pin
        self.__recording_dir = recording_dir
        self.__name = name

    def __on_state_change(self, state):
        record_file_name = (self.__name + '_' + state + '.csv')
        transmit(
            self.__recording_dir / record_file_name,
            self.__pin,
        )

    async def start(self):
        await self.__mqtt_light.start()
