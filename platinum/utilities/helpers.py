from enum import Enum


class VariableIdEnum(Enum):
    CONFIG_DATA = 0x00
    LIVE_DATA = 0x01
    ZERO_SENSOR_1 = 0x02
    SPAN_SENSOR_1_R1 = 0x03
    LIVE_DATA_SIMPLE = 0x06
    USER_DATA = 0x0B


def generate_and_add_checksum(command: bytearray) -> bytearray:
    checksum = sum(command).to_bytes(2, "big")

    command.extend(checksum)
    return command


def generate_read_frame(command: VariableIdEnum) -> bytearray:
    frame = [0x10, 0x13, command.value, 0x10, 0x1F]
    frame_bytearray = bytearray(frame)

    return generate_and_add_checksum(frame_bytearray)


def generate_write_frame(command: VariableIdEnum) -> bytearray:
    frame = [0x10, 0x15, command.value, 0x10, 0x1F]
    frame_bytearray = bytearray(frame)

    return generate_and_add_checksum(frame_bytearray)
