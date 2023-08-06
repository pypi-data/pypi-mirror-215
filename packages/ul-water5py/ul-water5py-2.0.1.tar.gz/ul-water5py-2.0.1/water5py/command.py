from pydantic import BaseModel

from .type_massage import COMMAND_PACKET_CHANNEL1, COMMAND_PACKET_CHANNEL2
from .utils import byte_battery_power_to_float32, new_numeric_fromInt, Water5Exception


class CommandPacketMeta(BaseModel):
    channel_bit_size: int = 8
    counter_bit_size: int = 32
    command_code_bit_size: int = 8
    temperature_bit_size: int = 8
    battery_bit_size: int = 8


class CommandPacketData(BaseModel):
    channel: int
    counter: float
    command_code: int
    temperature: int
    battery: float

    @staticmethod
    def parse_command(packet: bytes, sigh: int) -> 'CommandPacketData':
        if packet[0] == COMMAND_PACKET_CHANNEL1:
            channel = 1
        elif packet[0] == COMMAND_PACKET_CHANNEL2:
            channel = 2
        else:
            raise Water5Exception(f"invalid channel id. '{packet[0]}' was given")

        counter = packet[1]
        counter |= packet[2] << 8
        counter |= packet[3] << 16
        counter |= packet[4] << 24
        command_code = packet[5]
        temperature = packet[6]
        battery = byte_battery_power_to_float32(packet[7])

        return CommandPacketData(
            channel=channel,
            counter=new_numeric_fromInt(str(counter), sigh),
            command_code=command_code,
            temperature=temperature,
            battery=battery,
        )
