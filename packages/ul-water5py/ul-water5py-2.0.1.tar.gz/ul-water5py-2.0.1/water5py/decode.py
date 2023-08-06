from typing import Union, Tuple

from .command import CommandPacketData, CommandPacketMeta
from .daily import DailyPacketData, DailyPacketMeta
from .info import InfoPacketData, InfoPacketMeta
from .reset import ResetPacketData, ResetPacketMeta
from .type_massage import *
from .utils import Water5Exception
from .weekly import WeeklyPacketData, WeeklyPacketMeta

TW5Package = Union[Tuple[WeeklyPacketData, WeeklyPacketMeta],
                   Tuple[InfoPacketData, InfoPacketMeta],
                   Tuple[CommandPacketData, CommandPacketMeta],
                   Tuple[ResetPacketData, ResetPacketMeta],
                   Tuple[DailyPacketData, DailyPacketMeta],
]


def w5_decode(packet: bytes, nbfi_iterator: int, sigh: int = 3) -> TW5Package:
    if len(packet) != 8:
        raise Water5Exception("Error size packet Water5")
    if (packet[0] & 1) == 0:
        return DailyPacketData.parse_daily(packet, nbfi_iterator, sigh), DailyPacketMeta()
    if packet[0] == WEEKLY_PACKET_CODE_CHANNEL2 or packet[0] == WEEKLY_PACKET_CODE_CHANNEL1:
        return WeeklyPacketData.parse_weekly(packet, sigh), WeeklyPacketMeta()
    if packet[0] == INFO_PACKET_CODE_CHANNEL1 or packet[0] == INFO_PACKET_CODE_CHANNEL2:
        return InfoPacketData.parse_info(packet, sigh), InfoPacketMeta()
    if packet[0] == COMMAND_PACKET_CHANNEL1 or packet[0] == COMMAND_PACKET_CHANNEL2:
        return CommandPacketData.parse_command(packet, sigh), CommandPacketMeta()
    if packet[0] == COLD_RESET_PACKET_CHANNEL1 or packet[0] == COMMAND_PACKET_CHANNEL2:
        return ResetPacketData.parser_reset(packet, sigh), ResetPacketMeta()
    raise Water5Exception(f"Unsupported type of water5 packet, '{packet[0]}' was given")
