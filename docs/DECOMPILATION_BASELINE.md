# Decompilation Baseline — SoulSilver

This document records the first ROM-derived structural baseline for **SoulSilver**.

## Target identity

- Game title field: `POKEMON SS`
- Game code: `IPGK`
- Region / language: Korea / Korean
- Header ROM version byte: `0`
- ROM size: `134217728` bytes
- SHA-256: `8e1c82d2f718fa404f0b13df1666c70cdfaa75cb67e0adcbdcfb6c002f4d8b55`
- SHA-1: `0330e6449306606114a92bdbb3f9d3d51d392b96`
- MD5: `4e36e0c8c693d7cf52753f8601db5bbf`
- Verification status: **Internal identity verified; external preservation hash verification pending**

## Executable layout

- ARM9: ROM offset `0x4000`, size `765208` bytes, RAM `0x02000000`, entry `0x02000800`
- ARM7: ROM offset `0x2F7A00`, size `161496` bytes, RAM `0x02380000`, entry `0x02380000`
- ARM9 overlays: `129`
- ARM7 overlays: `0`

## NitroFS / FAT

- FAT entries: `511`
- NitroFS named files: `382`
- Verified boundary: FAT entries = ARM9 overlays + NitroFS files = `129 + 382 = 511`
- Header CRC matches: `true`

### Top-level NitroFS counts

- `a`: 265
- `data`: 84
- `pbr`: 23
- `fielddata`: 6
- `dwc`: 1
- `msgdata`: 1
- `poketool`: 1
- `tel`: 1

## HeartGold ↔ SoulSilver first-pass differential

- Shared NitroFS files with identical bytes: `379`
- NitroFS files with byte differences: `3` (`a/0/7/5`, `a/1/3/3`, `a/2/5/2`)
- NARC member differences: `a/0/7/5` → 1 of 2; `a/1/3/3` → 130 of 3962; `a/2/5/2` → 33 of 540.
- ARM7 identical: `true`
- ARM9 identical: `false`
- ARM9 overlays with byte differences or uniqueness: `118` of `129`

## Evidence status

- **Observed**: Values above were parsed directly from the supplied ROM image.
- **Reproduced**: Header CRC verification and FAT/overlay/NitroFS accounting were reproduced by `tools/nds_inventory.py`.
- **Matched**: Only targets explicitly noted as externally hash-matched should be treated as preservation-verified.

Raw ROM images are not stored in this repository.
