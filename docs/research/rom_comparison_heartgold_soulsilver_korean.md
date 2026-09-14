# HeartGold / SoulSilver Korean ROM comparison baseline

**Date observed:** 2026-09-14  
**Verification:** Observed  
**Targets:** project-provided Korean HeartGold (`IPKK`) and SoulSilver (`IPGK`), header version 0

The supplied ROMs are treated as direct observed targets. Their whole-ROM identities are not currently promoted to canonical clean-dump status; however, multiple core data archives match the PRET HeartGold/SoulSilver USA filesystem hashes byte-for-byte, making the internal structural observations below independently useful.

## Container and executable overview

- Both ROMs are 128 MiB.
- Both contain 129 ARM9 overlay records and no ARM7 overlay table.
- ARM7 is byte-identical between HeartGold and SoulSilver.
- ARM9 differs and SoulSilver's ARM9 is four bytes larger (`765,208` vs `765,204`).
- Both contain 511 FAT entries and 382 FNT-named files.
- 379 of the 382 named files are byte-identical between versions.
- Only three named NitroFS paths differ at whole-file level.
- Only 11 of the 129 ARM9 overlays are byte-identical; 118 differ. This broad executable delta must be separated from gameplay/content differences because build-time constants, code layout, and relocations may amplify binary differences.

## The three version-differentiated named archives

The observed differing paths line up exactly with the version-dependent archive mappings in the public source reconstruction:

| NitroFS path | Reconstructed role | Observed member-level delta |
| --- | --- | ---: |
| `a/0/7/5` | Pokédex height/weight version archive (`zukan_hw_data_*`) | 2 members total; 1 differs |
| `a/1/3/3` | Pokédex encounter/area version archive (`zukan_enc_*`) | 3,962 members; 130 differ |
| `a/2/5/2` | Headbutt encounter archive (`headbutt.*`) | 540 members; 33 differ |

The public `filesystem.mk` also explicitly marks these three targets as version-dependent, which independently supports the path interpretation.

## Core archive mapping and equality

Important serialized paths include:

| NitroFS path | Reconstructed data |
| --- | --- |
| `a/0/0/0` | move battle scripts |
| `a/0/0/1` | battle subscripts |
| `a/0/0/2` | Pokémon personal data |
| `a/0/0/3` | experience growth tables |
| `a/0/0/4` | Pokémon graphics |
| `a/0/1/1` | move data table |
| `a/0/1/2` | field script sequence archive |
| `a/0/1/7` | item data |
| `a/0/2/7` | message data |
| `a/0/3/2` | zone event data |
| `a/0/3/3` | level-up learnsets |
| `a/0/3/4` | evolution data |
| `a/0/3/7` | grass/field encounter data |
| `a/0/5/5` | trainer metadata |
| `a/0/5/6` | trainer parties |
| `a/1/3/6` | secondary encounter data |
| `a/1/6/9` | Pokéathlon performance data |
| `a/2/3/0` | Safari Zone encounter data |

Between the supplied HeartGold and SoulSilver ROMs, the personal, move, item, evolution, growth, learnset, and trainer archives are byte-identical. Version-specific Pokémon availability is therefore not encoded by duplicating those core species/trainer tables wholesale.

## Observed active data counts

| Data | Count/record size |
| --- | ---: |
| personal | 508 × 44 bytes |
| growth tables | 8 × 404 bytes |
| move table | 471 × 16 bytes |
| item table | 514 × 34 bytes |
| level-up learnsets | 508 members |
| evolution table | 508 × 44 bytes |
| trainer metadata | 738 records |
| trainer parties | 738 members |
| primary encounters | 142 × 196 bytes |
| secondary encounters | 142 × 196 bytes |
| performance data | 554 × 20 bytes |
| Safari Zone encounters | 12 × 912 bytes |
| Headbutt archive | 540 members |

## Cross-check against PRET filesystem hashes

Several language-independent/shared archives from the Korean targets exactly match the PRET USA HeartGold/SoulSilver filesystem hashes, including:

- `a/0/0/2` personal data
- `a/0/1/1` move data
- `a/0/1/7` item data
- `a/0/3/3` level-up learnsets
- `a/0/3/4` evolution data
- `a/0/3/7` primary encounters

This does **not** make the whole supplied ROMs canonical USA or Korean clean dumps. It confirms that substantial core game-data archives are exact matches to an independently reconstructed retail baseline.

## Generation IV continuity observations

Compared with the observed Platinum active data:

- Platinum and HGSS `evo.narc` are byte-identical in full.
- The experience growth-table archive is byte-identical across the observed Diamond/Pearl, Platinum, and HGSS targets.
- Platinum → HGSS level-up learnsets differ in 14 record IDs: `155, 156, 157, 249, 250, 382, 383, 384, 449, 450, 483, 484, 487, 501`.
- Platinum → HGSS move data differs in exactly one record, ID `258`.
- Platinum has 446 item records; HGSS has 514. Among the first 446, 29 records differ, and HGSS appends 68 records.
- Platinum and HGSS both have 508 personal-data records, but 272 records differ, showing that the evolution/growth layers are more stable than the personal-data layer across the two Generation IV branches.

## Next reconstruction work

1. Decode the three version-differentiated archives at semantic record level and identify every affected species/area/encounter.
2. Reconstruct the 118 differing overlays at function/symbol level instead of treating raw byte inequality as 118 independent features.
3. Decode personal/move/item/learnset deltas against Platinum and classify rule changes introduced by HGSS.
4. Continue through maps, scripts, event flags, Pokégear, following Pokémon, Pokéathlon, Safari Zone, Headbutt, radio/phone, trainer rematches, and Pokéwalker-related data.
