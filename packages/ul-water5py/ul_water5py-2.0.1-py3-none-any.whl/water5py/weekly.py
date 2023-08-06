from typing import List

from pydantic import BaseModel

from .type_massage import WEEKLY_PACKET_CODE_CHANNEL1, WEEKLY_PACKET_CODE_CHANNEL2
from .utils import byte_battery_power_to_float32, new_numeric_fromInt, Water5Exception


class WeeklyPacketMeta(BaseModel):
    channel_bit_size: int = 8
    counter_bit_size: int = 27
    day_rate_bit_size: int = 21
    battery_bit_size: int = 8


class WeeklyPacketData(BaseModel):
    channel: int
    counter: float
    day_rate: List[int]
    battery: float

    @staticmethod
    def parse_weekly(packet: bytes, sigh: int) -> "WeeklyPacketData":
        if packet[0] == WEEKLY_PACKET_CODE_CHANNEL1:
            channel = 1
        elif packet[0] == WEEKLY_PACKET_CODE_CHANNEL2:
            channel = 2
        else:
            raise Water5Exception(f"invalid channel id. '{packet[0]}' was given")

        channel = channel
        counter = packet[1]
        counter |= packet[2] << 8
        counter |= packet[3] << 16
        counter |= (packet[4] & 7) << 24

        day_rate = []
        day_rate.insert(0, ((packet[4] & 56) >> 3))
        day_rate.insert(1, (((packet[5] & 1) << 2) | ((packet[4] & 192) >> 6)))
        day_rate.insert(2, ((packet[5] & 14) >> 1))
        day_rate.insert(3, ((packet[5] & 112) >> 4))
        day_rate.insert(4, (((packet[6] & 3) << 1) | ((packet[5] & 128) >> 7)))
        day_rate.insert(5, ((packet[6] & 28) >> 2))
        day_rate.insert(6, ((packet[6] & 224) >> 5))
        day_rate.reverse()
        battery = byte_battery_power_to_float32(packet[7])

        return WeeklyPacketData(
            channel=channel,
            counter=float(new_numeric_fromInt(str(counter), sigh)),
            day_rate=day_rate,
            battery=battery,
        )
