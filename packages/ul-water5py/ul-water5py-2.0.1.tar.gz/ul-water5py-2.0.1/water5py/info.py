from pydantic import BaseModel

from .type_massage import INFO_PACKET_CODE_CHANNEL1, INFO_PACKET_CODE_CHANNEL2
from .utils import new_numeric_fromInt, Water5Exception


class InfoPacketMeta(BaseModel):
    channel_bit_size: int = 8
    counter_bit_size: int = 32
    count_send_message_bit_size: int = 16
    signal_level_bit_size: int = 6
    max_rate_bit_size: int = 2


class InfoPacketData(BaseModel):
    channel: int
    counter: float
    count_send_message: int
    signal_level: int
    max_rate: int

    @staticmethod
    def parse_info(packet: bytes, sigh: int) -> "InfoPacketData":
        if packet[0] == INFO_PACKET_CODE_CHANNEL1:
            channel = 1
        elif packet[0] == INFO_PACKET_CODE_CHANNEL2:
            channel = 2
        else:
            raise Water5Exception(f"invalid channel id. '{packet[0]}' was given")

        counter = packet[1]
        counter |= packet[2] << 8
        counter |= packet[3] << 16
        counter |= packet[4] << 24

        count_send_message = packet[5]
        count_send_message |= packet[6] << 8

        signal_level = (packet[7] & 192) >> 6

        max_rate = (packet[7] & 63)

        return InfoPacketData(
            channel=channel,
            counter=new_numeric_fromInt(str(counter), sigh),
            count_send_message=count_send_message,
            signal_level=signal_level,
            max_rate=max_rate,
        )
