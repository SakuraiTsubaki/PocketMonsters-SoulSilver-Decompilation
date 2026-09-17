# Generation IV Bug/Glitch/Error Elimination Program

## Goal

Eliminate confirmed unintended behavior in the SoulSilver target while preserving intended Generation IV mechanics, content, compatibility, and historical evidence. Reports are not treated as facts until reproduced or supported by ROM/source evidence.

## Target baseline

- Title: **포켓몬스터 소울실버**
- Game code: `IPGK`
- Region/language: **Korea Korean**
- Header ROM version: `0`
- SHA-256: `8e1c82d2f718fa404f0b13df1666c70cdfaa75cb67e0adcbdcfb6c002f4d8b55`
- FAT/NitroFS entries: **511**
- ARM9 overlays: **129**
- Identity: local image identified; independent preservation-catalog match pending

The ROM stays outside Git. Commit only non-ROM evidence, source, scripts, manifests, patches, tests, and hashes.

## Required workflow

1. Identify exact game/region/revision applicability.
2. Reproduce the issue or establish it from source/ROM evidence.
3. Locate the responsible executable, overlay, archive, script, map, text, or state machine.
4. Add a regression test where automation is possible.
5. Correct the root cause rather than copying an offset from another revision.
6. Compare D/P/Pt/HG/SS and official regional/revision fixes.
7. Verify the changed binary regions with `scripts/nds_inventory.py`.
8. Test adjacent normal behavior, save/load, and communication when relevant.
9. Track the result in `manifests/bugfix-matrix.csv`.

## Registry policy

The registry distinguishes `confirmed_public`, `region_specific`, `research_required`, `assessment_required`, and `discovery_track`. Network or server behavior is assessed separately from a local ROM defect. Historical unused/development data is documented rather than deleted merely because it is unused.

Seed sources include Bulbapedia's Generation IV battle/overworld/general glitch lists and Smogon's Generation IV competitive glitch survey. The registry also includes systematic arithmetic, bounds, save, map, battle, localization, graphics/audio, communication, and cross-revision audit tracks so completion is not limited to known wiki entries.

## Completion rule

Do not call the target bug-free until all confirmed entries are fixed or proven non-applicable, research entries are resolved with evidence, systematic audit tracks are completed, and regression verification finds no unresolved defect introduced by the fixes.
