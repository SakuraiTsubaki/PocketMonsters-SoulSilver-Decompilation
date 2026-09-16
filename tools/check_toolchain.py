#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,os,shutil,subprocess
from dataclasses import dataclass,asdict
from pathlib import Path
@dataclass
class Check: name:str; kind:str; required:bool; path:str|None; version:str|None; ok:bool; note:str=""
def first_command(*names):
    for n in names:
        p=shutil.which(n)
        if p:return p
def version(p,args):
    if not p:return None
    try:r=subprocess.run([p,*args],text=True,capture_output=True,timeout=8,check=False)
    except Exception:return None
    t=(r.stdout or r.stderr).strip().splitlines();return t[0][:240] if t else None
def main():
    specs=[("git",("git",),["--version"],True),("python3",("python3",),["--version"],True),("make",("make",),["--version"],True),("cmake",("cmake",),["--version"],False),("ninja",("ninja",),["--version"],False),("clang",("clang",),["--version"],True),("llvm-objdump",("llvm-objdump",),["--version"],True),("llvm-objcopy",("llvm-objcopy",),["--version"],True),("arm-none-eabi-objdump",("arm-none-eabi-objdump",),["--version"],True),("arm-none-eabi-gcc",("arm-none-eabi-gcc",),["--version"],False),("gdb",("arm-none-eabi-gdb","gdb-multiarch","gdb"),["--version"],False),("wine",("wine64","wine"),["--version"],False),("ndstool",("ndstool",),["-?"],False),("melonDS",("melonDS","melonds"),["--help"],True),("DeSmuME",("desmume","desmume-cli"),["--version"],False),("dkp-pacman",("dkp-pacman",),["--version"],False)]
    checks=[]
    for label,cmds,args,required in specs:
        p=first_command(*cmds);checks.append(Check(label,"command",required,p,version(p,args),bool(p)))
    for m in ("capstone","construct","ndspy","lief"):
        s=importlib.util.find_spec(m);checks.append(Check(m,"python-module",False,getattr(s,"origin",None) if s else None,None,s is not None))
    dp=Path(os.environ.get("DEVKITPRO","/opt/devkitpro")); da=Path(os.environ.get("DEVKITARM",dp/"devkitARM")); checks += [Check("DEVKITPRO","directory",False,str(dp),None,dp.is_dir()),Check("DEVKITARM","directory",False,str(da),None,da.is_dir())]
    for n in ("MWCCARM_ROOT","NITROSDK_ROOT"):
        v=os.environ.get(n);checks.append(Check(n,"proprietary",False,v,None,bool(v and Path(v).exists()),"user-supplied only"))
    for c in checks: print(f'{"OK" if c.ok else ("MISSING" if c.required else "optional"):8} {c.name:22} {c.path or "-"}')
    out=Path("build/toolchain-report.json");out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({"schema_version":1,"checks":[asdict(c) for c in checks]},indent=2)+"\n")
    return 1 if any(c.required and not c.ok for c in checks) else 0
if __name__=="__main__": raise SystemExit(main())
