# Public Source Registry — Pocket Monsters SoulSilver

This registry tracks public material used to reconstruct and compare Pocket Monsters SoulSilver without assuming access to an original ROM image.

## Rules

- Japanese earliest retail release is the historical baseline.
- Record every official region, language, and revision separately.
- Do not mark releases identical without positive evidence.
- Preserve conflicting claims and their sources.
- Record redistribution/licensing status before copying external material into this repository.
- Every research result derived from a source should link back to a registry entry.
- The registry is an exhaustive-census index, not a representative reading list. Historical, superseded, forked, archived, and conflicting public research remains in scope.

## Evidence status

- `CONFIRMED_IDENTICAL`
- `CONFIRMED_DIFFERENT`
- `UNVERIFIED`
- `CONFLICTING_EVIDENCE`

## Source registry

| ID | Source | Source type | Game | Region | Language | Revision | Component / scope | Original or derived | Redistribution status | Verification | Cross-check | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SS-SRC-0001` | [pret/pokeheartgold](https://github.com/pret/pokeheartgold) | Public disassembly/decompilation project | HeartGold/SoulSilver | USA target | English | matching targets | Code, overlays, filesystem, data, assets, build/reconstruction | Derived source project | Follow upstream terms; no retail ROM | Strong technical reference | No-Intro-linked identities; tools; scrcmd database | Builds SoulSilver USA SHA-1 `f8dc38ea20c17541a43b58c5e6d18c1732c7e582` and HeartGold USA SHA-1 `4fcded0e2713dc03929845de631d0932ea2b5a37`. Shared HGSS source must not erase SoulSilver-exclusive data. |
| `SS-SRC-0002` | [Project Pokémon PPRE](https://github.com/projectpokemon/PPRE) | Historical ROM-editor source | HGSS / Gen IV | USA-focused | English | multiple supported games | Pokémon, text, move editing and format/tool lineage | Derived technical tooling | Follow upstream terms | Historical technical reference | PRET; older editors | PPRE supports HeartGold and SoulSilver and provides historical implementation evidence for Gen IV formats. |
| `SS-SRC-0003` | [DS-Pokemon-Rom-Editor/scrcmd-database](https://github.com/DS-Pokemon-Rom-Editor/scrcmd-database) | Script-command research database | D/P/Pt/HGSS | Multi-game | Technical metadata | current V2 + legacy | Script opcodes, movement commands, macros, sounds, flags/vars, comparisons, special overworld IDs | Derived from DSPRE/decomp/community | Follow upstream license | Strong living technical reference | `SS-SRC-0001`; DSPRE | HGSS metadata is enriched from PRET; use game/version provenance when applying shared command names. |
| `SS-SRC-0004` | [Project Pokémon — Gen IV BDHC terrain research](https://projectpokemon.org/home/forums/topic/37816-gen-iv-bdhc-files-terrain-settings/) | Reverse-engineering research | D/P/Pt/HGSS | Multi-game | English research notes | N/A | BDHC terrain/collision format | Derived community research | Citation/link only | Technical reference; reproduce before promoting | Editors/decomp | Relevant to SoulSilver map reconstruction; exact HGSS usage must be checked rather than assumed from DPPt. |
| `SS-SRC-0005` | [Bulbapedia — List of glitches in Generation IV](https://bulbapedia.bulbagarden.net/wiki/List_of_glitches_in_Generation_IV) | Specialist glitch index | D/P/Pt/HGSS | Multi-region | English | multiple | HGSS-specific and shared Gen IV glitches | Derived | Citation/link only | Secondary discovery index | Decomp code; technical forums; contemporary reports | Includes Buena's Password, Pokémon Lullaby underflow, Pokéwalker cloning and shared glitches. Exact conditions still require independent evidence. |
| `SS-SRC-0006` | [Bulbapedia — HeartGold and SoulSilver versions](https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_HeartGold_and_SoulSilver_Versions) | Specialist wiki / content index | HeartGold/SoulSilver | Multi-region | Multi-language | multiple | Remake changes, regional differences, events, Pokéwalker/Pokéathlon/content inventory | Derived | Citation/link only | Secondary index | GSC originals, official material, PRET, event archives | Discovery/index source only; all substantial claims are to be re-sourced and version-qualified. |

## Difference registry

| ID | Japanese baseline | Compared release | Component | Difference class | Evidence status | Source IDs | Notes |
|---|---|---|---|---|---|---|---|

## Census workstreams

The survey includes Japanese SS as the historical baseline; all regional/language/revision retail builds; all public PRET history/forks/issues/PRs; historical ROM editors and tooling; Project Pokémon research/attachments; map/terrain/script/text/audio/save/Pokéwalker research; distributions/Wonder Cards/NWC/GTS; GSC→HGSS remake comparisons; glitches/TAS/exploits; unused/debug/development material; demos/service software; specialist databases/wikis as leads; and archived/dead-link recoveries.

## Coverage backlog

The registry is expected to cover release/revision inventories; ARM9/ARM7 and overlays; NitroFS/NARC; scripts; text; Johto/Kanto maps; GSC→HGSS map/event/NPC/trainer/wild/music comparisons; Pokémon/trainer/item/move/encounter data; following Pokémon; Pokéathlon; Battle Frontier; Pokéwalker hardware/protocol/course data; graphics/sprites/models/animation; audio; save; local wireless/NWC/GTS/Mystery Gift; distributions; bugs/fixes; unused/debug/development remnants; localization/censorship; tools; specialist databases/wikis; and archival community research. Entries above are only the first census batch and do not define the final scope.
