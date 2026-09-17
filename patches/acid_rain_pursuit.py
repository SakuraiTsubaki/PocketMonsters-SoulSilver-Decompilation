#!/usr/bin/env python3
"""Fix G4-BAT-018 (Acid Rain) in the exact IPGK Rev 0 battle subscript archive."""
import argparse
import struct
from pathlib import Path

GAME_CODE = b"IPGK"
ROM_VERSION = 0
SUB_SEQ_FILE_ID = 130
PURSUIT_MEMBER = 153
BUG_TUPLE_OFFSET = 0x394
BUG_TUPLE = (57, 18, 7, 43)
FIX_TUPLE = (57, 7, 18, 43)


def u32(data, off):
    return struct.unpack_from("<I", data, off)[0]


def locate_member(data, file_id, member_id):
    fat = u32(data, 0x48)
    file_start, file_end = struct.unpack_from("<II", data, fat + file_id * 8)
    narc = data[file_start:file_end]
    if narc[:4] != b"NARC":
        raise SystemExit("target file is not a NARC archive")
    pos = struct.unpack_from("<H", narc, 12)[0]
    entries = None
    gmif = None
    for _ in range(struct.unpack_from("<H", narc, 14)[0]):
        magic = narc[pos:pos + 4]
        size = u32(narc, pos + 4)
        if magic == b"BTAF":
            count = struct.unpack_from("<H", narc, pos + 8)[0]
            entries = [struct.unpack_from("<II", narc, pos + 12 + i * 8) for i in range(count)]
        elif magic == b"GMIF":
            gmif = pos + 8
        pos += size
    if entries is None or gmif is None or member_id >= len(entries):
        raise SystemExit("unexpected subscript archive layout")
    start, _ = entries[member_id]
    return file_start + gmif + start


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()
    data = bytearray(Path(args.input).read_bytes())
    if data[12:16] != GAME_CODE or data[0x1E] != ROM_VERSION:
        raise SystemExit("input is not IPGK Rev 0")
    member = locate_member(data, SUB_SEQ_FILE_ID, PURSUIT_MEMBER)
    off = member + BUG_TUPLE_OFFSET
    current = struct.unpack_from("<IIII", data, off)
    if current == FIX_TUPLE:
        raise SystemExit("Acid Rain fix is already present")
    if current != BUG_TUPLE:
        raise SystemExit(f"unexpected Pursuit tuple: {current}")
    struct.pack_into("<IIII", data, off, *FIX_TUPLE)
    Path(args.output).write_bytes(data)


if __name__ == "__main__":
    main()
