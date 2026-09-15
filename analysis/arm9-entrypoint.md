# ARM9 entrypoint — Phase 1

Target: `IPGK` / Korea Korean / ROM version byte `0`.

## Observed boundaries

| Address | Working identity | Evidence |
|---:|---|---|
| `0x02000800` | `_start` | Exact ROM entrypoint; startup structure matches the Generation IV NitroSDK crt0 sequence |
| `0x02000954` | `INITi_CpuClear32` | Three direct clear calls; instruction sequence equivalent to the D/P startup helper |
| `0x02000970` | `MIi_UncompressBackward` | Direct startup call; instruction sequence equivalent to the D/P decompressor helper |
| `0x02000A1C` | `do_autoload` | Direct startup call; shared crt0 autoload structure |
| `0x02000AB0` | `init_cp15` | First startup call; CP15 initialization pattern |
| `0x02000B98` | `NitroStartUp` | Startup call position and shared runtime pattern |
| `0x020F39D0` | `_fp_init` | Reference-supported from startup call ordering |
| `0x020F5144` | `__call_static_initializers` | Reference-supported from startup call ordering |

The `NitroMain` literal is `0x02000CA5`; bit 0 marks Thumb state, giving code address `0x02000CA4`.

## Startup fingerprint

SoulSilver and HeartGold differ by only **two bytes** in the entire first `0x200` bytes at `0x02000800`–`0x02000A00`. Both differences occur in branch immediates for the two far runtime-initialization calls (`_fp_init` and `__call_static_initializers`); the common startup body and `NitroMain` literal are otherwise identical in this window.

## Confidence

- Addresses and bytes: **Observed** from the verified Korean SoulSilver ROM.
- Runtime identities: **Reference-supported / sequence-matched** against the D/P NitroSDK startup reconstruction.
- Game-specific code beyond this startup chain remains address-named until independently reconstructed.
