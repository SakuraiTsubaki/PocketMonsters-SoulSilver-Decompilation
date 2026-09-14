# Core data Phase 1 — HeartGold / SoulSilver

## Evidence status

The locally available Korean SoulSilver image (`IPGK`, version 0) is retained as a historical/scene **comparison source**. Whole-ROM clean-reference identities are tracked separately in `manifests/clean_reference.json`; no guessed byte repair is used.

## Core archive inventory

| Dataset | Members | Record form |
| --- | ---: | --- |
| `a/0/0/2` personal | 508 | 44-byte records |
| `a/0/3/4` evolution | 508 | 44-byte records |
| `a/0/3/3` level-up learnsets | 508 | packed 16-bit entries + sentinel |
| `a/0/1/1` moves | 471 | 16-byte records |
| `a/0/1/7` items | 514 | 34-byte records |
| `a/0/0/3` growth | 8 | 404-byte tables |

The same six archives are byte-identical between the project-provided HeartGold and SoulSilver images.

## Platinum → HGSS exact record counts

- personal: 272 changed records.
- evolution: **0 changed records**.
- learnsets: **14 changed records**: 155 Cyndaquil, 156 Quilava, 157 Typhlosion, 249 Lugia, 250 Ho-Oh, 382 Kyogre, 383 Groudon, 384 Rayquaza, 449 Hippopotas, 450 Hippowdon, 483 Dialga, 484 Palkia, 487 Giratina, and 501 Giratina Origin.
- moves: **1 changed record**, Hail (258).
- items: 446 → 514 data records. Logical item-ID/data-ID remapping is required; raw same-index comparison is not semantic comparison.
- growth tables: byte-identical.

## Personal-data changes

The major HGSS-specific categories are:

- TM/HM compatibility mask changes: 170 records.
- Safari flee-rate population: 134 records.
- Shuckle (213): common and rare held item both `ITEM_ORAN_BERRY (155) → ITEM_BERRY_JUICE (43)`.
- Pichu (172): packed body-color/sprite byte `0x02 → 0x82`; body color remains 2 and `flipSprite` changes from false to true.
- Electabuzz/Magmar/Elekid/Magby: Platinum rare Electirizer/Magmarizer entries are cleared.
- Electivire/Magmortar: rare Electirizer/Magmarizer entries are retained.

## Learnset changes

### Johto fire starter family

Cyndaquil's Smokescreen moves from level 4 to 6. Quilava and Typhlosion retain a level-1 reminder entry and move their second Smokescreen entry from level 4 to 6.

### Hippopotas family

Hippopotas and Hippowdon gain Dig at level 19; their existing level-19 Take Down remains.

### Lugia / Ho-Oh

Both receive a substantial reorder. Weather Ball is added at level 1; Lugia gains Dragon Rush at level 15 and moves Aeroblast to level 43; Ho-Oh gains Brave Bird at level 15 and moves Sacred Fire to level 43. Their weather, recovery, and late-game move levels are reordered accordingly.

### Weather trio

Kyogre, Groudon, and Rayquaza receive broad level-order rewrites. HGSS introduces Aqua Ring/Muddy Water for Kyogre, Lava Plume/Hammer Arm for Groudon, and Hyper Voice/Air Slash for Rayquaza, while retaining their signature/endgame move sets at reorganized levels.

### Creation trio

Dialga, Palkia, Giratina Altered, and the Giratina Origin data-form slot are compressed from a Platinum level progression reaching level 90 into an HGSS progression whose signature move lands at level 46. Dialga gains Power Gem and Metal Burst; Palkia gains Power Gem and level-42 Hydro Pump; Giratina gains Shadow Sneak and Destiny Bond.

The complete before/after learnset records are documented in the Platinum repository's `docs/research/core-data-phase1.md` and were derived directly from the local NARC members.

## Move-table delta

Hail (258) is the only Platinum→HGSS move-record change. Platinum has flags byte `0x02`; HGSS has `0x00`. Under the Generation IV move-flag ordering this clears `MOVE_FLAG_CAN_PROTECT`. All other Hail fields are identical.

## Item-table alignment result

Raw NARC member indices are not logical item IDs. HGSS keeps the logical Generation IV item-ID space but changes the dense item-data mapping:

- `ITEM_GRISEOUS_ORB` is data member 112 in HGSS.
- logical IDs 113–134 remain unused and map to fallback data rather than dedicated records.
- `ITEM_EXPLORER_KIT` (logical ID 428) no longer has a dedicated item-data member and maps to the fallback record.
- `ITEM_LOOT_SACK` therefore begins at data member 406.
- Platinum's `VS Recorder`, `Gracidea`, and `Secret Key` are retained as HGSS data members 442–444.
- all 69 HGSS-new logical item IDs 468–536 have dedicated data records, producing the net archive growth `446 - 1 + 69 = 514`.

After logical-ID/data-ID alignment, the directly observed existing-item parameter changes are:

- `X Sp. Def` (ID 62): HGSS adds the missing low/medium friendship modifiers (`+1`, `+1`), bringing it in line with the other X-stat items.
- `Growth Mulch`, `Damp Mulch`, `Stable Mulch`, `Gooey Mulch` (IDs 95–98): the Platinum field-use handler is cleared in HGSS.

The apparent numeric changes in Griseous/Adamant/Lustrous Orb hold-effect bytes and in the VS Recorder/Gracidea field-use-function byte are treated as **enum/handler index remapping**, not by themselves as semantic behavior changes.

## HG ↔ SS

For personal, evolution, level-up learnsets, moves, items, and growth tables: **0 differing records**. Version exclusivity in these games is therefore implemented outside these six core tables (encounters, Pokédex area data, scripts/code, etc.).
