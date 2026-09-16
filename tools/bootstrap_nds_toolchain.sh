#!/usr/bin/env bash
set -euo pipefail
TOOL_ROOT="${GEN4_TOOL_ROOT:-$HOME/.local/share/pokemon-gen4-nds-toolchain}"; BIN_DIR="$TOOL_ROOT/bin"; SRC_DIR="$TOOL_ROOT/src"; VENV_DIR="$TOOL_ROOT/venv"; EMU_DIR="$TOOL_ROOT/emulators"
INSTALL_DEVKITPRO=1; INSTALL_MELONDS=1; INSTALL_PYTHON_EXTRAS=1; INSTALL_NDSTOOL=1; INSTALL_APT=1
usage(){ cat <<'USAGE'
Usage: tools/bootstrap_nds_toolchain.sh [options]
  --root PATH
  --skip-apt
  --skip-devkitpro
  --skip-melonds
  --skip-python-extras
  --skip-ndstool
  -h, --help
The script never downloads proprietary Metrowerks compiler or Nintendo NitroSDK files.
USAGE
}
while (($#)); do case "$1" in --root) TOOL_ROOT="$2"; shift 2;; --skip-apt) INSTALL_APT=0; shift;; --skip-devkitpro) INSTALL_DEVKITPRO=0; shift;; --skip-melonds) INSTALL_MELONDS=0; shift;; --skip-python-extras) INSTALL_PYTHON_EXTRAS=0; shift;; --skip-ndstool) INSTALL_NDSTOOL=0; shift;; -h|--help) usage; exit 0;; *) echo "Unknown option: $1" >&2; usage >&2; exit 2;; esac; done
BIN_DIR="$TOOL_ROOT/bin"; SRC_DIR="$TOOL_ROOT/src"; VENV_DIR="$TOOL_ROOT/venv"; EMU_DIR="$TOOL_ROOT/emulators"; mkdir -p "$BIN_DIR" "$SRC_DIR" "$EMU_DIR"
if [[ $(id -u) -eq 0 ]]; then SUDO=(); elif command -v sudo >/dev/null 2>&1; then SUDO=(sudo); else echo "sudo is required" >&2; exit 1; fi
install_apt_packages(){ [[ $INSTALL_APT -eq 1 ]] || return 0; command -v apt-get >/dev/null 2>&1 || return 0; "${SUDO[@]}" apt-get update; local required=(build-essential git curl ca-certificates unzip zip xz-utils p7zip-full python3 python3-venv python3-pip cmake ninja-build clang llvm lld binutils-arm-none-eabi gdb-multiarch wine64 libpng-dev pkg-config libpugixml-dev); "${SUDO[@]}" apt-get install -y "${required[@]}"; local optional=(gcc-arm-none-eabi xdelta3 bsdiff desmume); for pkg in "${optional[@]}"; do apt-cache show "$pkg" >/dev/null 2>&1 && "${SUDO[@]}" apt-get install -y "$pkg" || true; done; }
install_python_extras(){ [[ $INSTALL_PYTHON_EXTRAS -eq 1 ]] || return 0; python3 -m venv "$VENV_DIR"; "$VENV_DIR/bin/python" -m pip install --upgrade pip; "$VENV_DIR/bin/python" -m pip install 'capstone>=5,<6' 'construct>=2.10,<3' 'ndspy>=4,<5'; "$VENV_DIR/bin/python" -m pip install 'lief>=0.16,<1' || true; }
install_ndstool(){ [[ $INSTALL_NDSTOOL -eq 1 ]] || return 0; command -v ndstool >/dev/null 2>&1 && return 0; [[ -x "$BIN_DIR/ndstool" ]] && return 0; local dst="$SRC_DIR/ndstool"; if [[ ! -d "$dst/.git" ]]; then rm -rf "$dst"; git clone --depth 1 https://github.com/blocksds/ndstool.git "$dst"; else git -C "$dst" pull --ff-only; fi; make -C "$dst" -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)"; install -m 0755 "$dst/ndstool" "$BIN_DIR/ndstool"; }
install_devkitpro(){ [[ $INSTALL_DEVKITPRO -eq 1 ]] || return 0; if ! command -v dkp-pacman >/dev/null 2>&1; then command -v apt-get >/dev/null 2>&1 || return 1; local tmp="$(mktemp -d)"; curl -fsSL https://apt.devkitpro.org/install-devkitpro-pacman -o "$tmp/install-devkitpro-pacman"; chmod +x "$tmp/install-devkitpro-pacman"; "${SUDO[@]}" "$tmp/install-devkitpro-pacman"; rm -rf "$tmp"; fi; "${SUDO[@]}" dkp-pacman -Syu --noconfirm; "${SUDO[@]}" dkp-pacman -S --needed --noconfirm nds-dev; }
install_melonds(){ [[ $INSTALL_MELONDS -eq 1 ]] || return 0; command -v melonDS >/dev/null 2>&1 && return 0; command -v melonds >/dev/null 2>&1 && return 0; [[ -x "$BIN_DIR/melonDS" ]] && return 0; local asset_arch release_json asset_json url digest name version tmp dest candidate; case "$(uname -m)" in x86_64|amd64) asset_arch=x86_64;; aarch64|arm64) asset_arch=aarch64;; *) echo "Unsupported melonDS architecture" >&2; return 1;; esac; version="${MELONDS_VERSION:-1.1}"; if [[ "$version" == latest ]]; then release_json="$(curl -fsSL https://api.github.com/repos/melonDS-emu/melonDS/releases/latest)"; else release_json="$(curl -fsSL "https://api.github.com/repos/melonDS-emu/melonDS/releases/tags/$version")"; fi; asset_json="$(printf '%s' "$release_json" | python3 -c 'import json,sys; arch=sys.argv[1]; d=json.load(sys.stdin); w=f"ubuntu-{arch}.zip"; a=next((x for x in d.get("assets",[]) if x.get("name","").endswith(w)),None); a or (_ for _ in ()).throw(SystemExit("melonDS asset not found")); print(json.dumps({"name":a["name"],"url":a["browser_download_url"],"digest":a.get("digest","")}))' "$asset_arch")"; name="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["name"])' <<<"$asset_json")"; url="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["url"])' <<<"$asset_json")"; digest="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("digest",""))' <<<"$asset_json")"; tmp="$(mktemp -d)"; curl -fL "$url" -o "$tmp/$name"; [[ "$digest" == sha256:* ]] && printf '%s  %s\n' "${digest#sha256:}" "$tmp/$name" | sha256sum -c -; dest="$EMU_DIR/melonDS-$version"; rm -rf "$dest"; mkdir -p "$dest"; unzip -q "$tmp/$name" -d "$dest"; candidate="$(find "$dest" -maxdepth 3 -type f \( -name melonDS -o -name melonds \) -print -quit)"; [[ -n "$candidate" ]] || return 1; chmod +x "$candidate"; ln -sfn "$candidate" "$BIN_DIR/melonDS"; rm -rf "$tmp"; }
write_env_file(){ local env_file="$TOOL_ROOT/toolchain.env"; cat > "$env_file" <<ENV
export GEN4_TOOL_ROOT="$TOOL_ROOT"
export PATH="$BIN_DIR:$VENV_DIR/bin:\$PATH"
if [ -d /opt/devkitpro ]; then export DEVKITPRO=/opt/devkitpro; export DEVKITARM=/opt/devkitpro/devkitARM; fi
ENV
 echo "Environment file: $env_file"; }
install_apt_packages; install_python_extras; install_ndstool; install_devkitpro; install_melonds; write_env_file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; [[ -f "$SCRIPT_DIR/check_toolchain.py" ]] && PATH="$BIN_DIR:$VENV_DIR/bin:$PATH" python3 "$SCRIPT_DIR/check_toolchain.py" || true
