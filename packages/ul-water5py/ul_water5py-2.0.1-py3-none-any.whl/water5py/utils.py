class Water5Exception(Exception):
    def __init__(self, massage: str, *args, **kwargs) -> None:
        super(*args, **kwargs)
        self.message = massage


def byte_battery_power_to_float32(data: int) -> float:
    return 2 + (data >> 7) + (data & 0x7F) / 100


def new_numeric_fromInt(base: str, scale: int) -> float:
    result: str
    base = str(base)
    dot_index = len(base) - scale
    if dot_index > 0:
        result = base[:dot_index]
        result += "."
        result += base[dot_index:]
    else:
        result = "0."
        while dot_index != 0:
            dot_index += 1
            result += "0"
        result += base
    return float(result)
