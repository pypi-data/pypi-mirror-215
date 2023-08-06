from typing import List

from pydantic import BaseModel

from .utils import new_numeric_fromInt, Water5Exception


class DailyPacketMeta(BaseModel):
    channel_bit_size: int = 1
    counter_bit_size: int = 15
    hour_rate_bit_size: int = 48


class DailyPacketData(BaseModel):
    channel: int
    counter: float
    hour_rate: List[int]

    @staticmethod
    def parse_daily(packet: bytes, nbfi_iterator: int, sigh: int) -> "DailyPacketData":
        if (nbfi_iterator % 2) == 0:
            channel = 2
        elif (nbfi_iterator % 2) == 1:
            channel = 1
        else:
            raise Water5Exception(f"invalid channel id. '{packet[0]}' was given")

        counter = packet[0] >> 1
        counter |= packet[1] << 7

        hour_rate = []
        for i in range(24):
            hour_rate.append(packet[2 + i // 4] & (3 << ((i % 4) * 2)) >> ((i % 4) * 2))

        return DailyPacketData(
            channel=channel,
            counter=new_numeric_fromInt(str(counter), sigh),
            hour_rate=hour_rate,
        )
