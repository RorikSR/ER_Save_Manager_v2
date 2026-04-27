import binascii
import hashlib


SLOT_COUNT = 10
SLOT_CHECKSUM_START = 0x00000300
SLOT_DATA_START = 0x00000310
SLOT_STRIDE = 2621456
SLOT_DATA_LENGTH = 2621440
SLOT_CHECKSUM_LENGTH = 16
GENERAL_CHECKSUM_START = 0x019003A0
GENERAL_DATA_START = 0x019003B0
GENERAL_DATA_END = 0x019603AF + 1


def _md5_bytes(data):
    return hashlib.md5(data).digest()


def recalculate_data(data):
    save_bytes = bytearray(data)

    for slot_index in range(SLOT_COUNT):
        checksum_start = SLOT_CHECKSUM_START + (slot_index * SLOT_STRIDE)
        data_start = SLOT_DATA_START + (slot_index * SLOT_STRIDE)
        data_end = data_start + SLOT_DATA_LENGTH
        slot_data = save_bytes[data_start:data_end]
        save_bytes[checksum_start : checksum_start + SLOT_CHECKSUM_LENGTH] = _md5_bytes(slot_data)

    general = save_bytes[GENERAL_DATA_START:GENERAL_DATA_END]
    save_bytes[GENERAL_CHECKSUM_START : GENERAL_CHECKSUM_START + SLOT_CHECKSUM_LENGTH] = _md5_bytes(general)
    return bytes(save_bytes)


def verify_data(data):
    issues = []
    for slot_index in range(SLOT_COUNT):
        checksum_start = SLOT_CHECKSUM_START + (slot_index * SLOT_STRIDE)
        data_start = SLOT_DATA_START + (slot_index * SLOT_STRIDE)
        data_end = data_start + SLOT_DATA_LENGTH
        expected = _md5_bytes(data[data_start:data_end])
        actual = data[checksum_start : checksum_start + SLOT_CHECKSUM_LENGTH]
        if actual != expected:
            issues.append(
                {
                    "kind": "slot",
                    "slot": slot_index + 1,
                    "expected": binascii.hexlify(expected).decode("ascii"),
                    "actual": binascii.hexlify(actual).decode("ascii"),
                }
            )

    general_expected = _md5_bytes(data[GENERAL_DATA_START:GENERAL_DATA_END])
    general_actual = data[GENERAL_CHECKSUM_START : GENERAL_CHECKSUM_START + SLOT_CHECKSUM_LENGTH]
    if general_actual != general_expected:
        issues.append(
            {
                "kind": "general",
                "expected": binascii.hexlify(general_expected).decode("ascii"),
                "actual": binascii.hexlify(general_actual).decode("ascii"),
            }
        )

    return {"valid": not issues, "issues": issues}
