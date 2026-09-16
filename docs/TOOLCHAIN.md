# Toolchain — SoulSilver

```sh
bash tools/bootstrap_nds_toolchain.sh
source "$HOME/.local/share/pokemon-gen4-nds-toolchain/toolchain.env"
python3 tools/check_toolchain.py
```

The bootstrap installs the common NDS reverse-engineering stack: Git/Python/build tools, Clang/LLVM/LLD, GNU Arm binutils/GDB, Wine, libpng/pkg-config/pugixml, ndstool, devkitPro `nds-dev`/devkitARM/libnds, Python RE helpers, melonDS, plus optional DeSmuME/xdelta3/bsdiff.

Primary emulator is **melonDS 1.1**; Ubuntu x86_64 SHA-256: `99465129f5413b2aad332e4377e523cf3cda905dc329d47dcb1ad01ce2cb3f66`.

External HeartGold matching reference uses MWCC 2.0/sp2p2 and NitroSDK 4.2-071210-jp. The current target is **Korean SoulSilver**, so those versions remain reference-only until independently verified against this target. Proprietary components are never auto-downloaded or committed; `MWCCARM_ROOT` and `NITROSDK_ROOT` only point to user-supplied copies.

BIOS, firmware, retail ROMs, and proprietary console material remain local only.
