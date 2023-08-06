from pydantic import BaseModel

from .type_massage import COLD_RESET_PACKET_CHANNEL1, COLD_RESET_PACKET_CHANNEL2
from .utils import new_numeric_fromInt, Water5Exception


class ResetPacketMeta(BaseModel):
    channel_bit_size: int = 8
    counter_bit_size: int = 32
    hardware_rev_bit_size: int = 8
    div_bit_size: int = 2
    software_rev_bit_size: int = 6
    crc_time_bit_size: int = 8


class ResetPacketData(BaseModel):
    channel: int
    counter: float
    hardware_rev: int
    div: int
    software_rev: int
    crc_time: int

    @staticmethod
    def parser_reset(packet: bytes, sigh: int) -> "ResetPacketData":
        if packet[0] == COLD_RESET_PACKET_CHANNEL1:
            channel = 1
        elif packet[0] == COLD_RESET_PACKET_CHANNEL2:
            channel = 2
        else:
            raise Water5Exception(f"invalid channel id. '{packet[0]}' was given")

        channel = channel
        counter = packet[1]
        counter |= packet[2] << 8
        counter |= packet[3] << 16
        counter |= packet[4] << 24
        hardware_rev = packet[5]
        div = (packet[6] & 192) >> 6
        software_rev = packet[6] & 63
        crc_time = packet[7]

        return ResetPacketData(
            channel=channel,
            counter=new_numeric_fromInt(str(counter), sigh),
            hardware_rev=hardware_rev,
            div=div,
            software_rev=software_rev,
            crc_time=crc_time,
        )
