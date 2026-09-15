# ARM9 `NitroMain` analysis

## Verified target
- Game: Pokémon SoulSilver
- Game code: `IPGK`
- Region/language: Korea / Korean
- ROM identity: `manifests/rom-baseline.json`

## Entry and boundary
- `_start` loads `0x02000CA5`; bit 0 selects Thumb state.
- `NitroMain` Thumb entry: `0x02000CA4`.
- Observed main-function instruction/literal boundary: `0x02000CA4..0x02000E47`.
- Literal pool begins at `0x02000E48`.
- Code span size: `0x1A4` (420) bytes.
- SHA-256 of that observed code span: `6b75d55ce654aa12109cbee921e8283eb513632510f517ca623223423561c2a2`.
- Call sites in the observed body: 53 total, including one register-indirect `BLX` callback site.

## Matched high-level flow
The Korean SoulSilver target has the same high-level HG/SS `NitroMain` organization reconstructed in `pret/pokeheartgold`: platform initialization, graphics/input/backlight work, 3D buffer-swap state, RTC/overlay manager, fonts/save/sound/timer, WFC/save validation, initial overlay selection, RNG/brightness/tick setup, and then the permanent per-frame loop.

## HG/SS comparison
The function boundary and control-flow organization match HeartGold, but the 420-byte body differs at twelve byte positions. The observed differences correspond chiefly to nearby call-target address shifts between the two complete binaries rather than a different main-loop design.

Examples include SoulSilver direct targets `0x020DBAA0`, `0x0202D0F4`, `0x0203A278`, `0x0203AF10`, `0x02092D28`, and related HG/SS address pairs.

## Evidence
- Local Korean SoulSilver ROM disassembly.
- Direct local comparison with the Korean HeartGold target.
- Structural/name cross-check against `pret/pokeheartgold`.

## Next mapping pass
1. Build complete SS↔HG direct-call correspondence.
2. Resolve names without assuming identical addresses across versions.
3. Follow intro-title and main-menu overlays.
4. Extend paired comparison through ARM9, ARM7, NitroFS resources, and all 129 ARM9 overlays.
