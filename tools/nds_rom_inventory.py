#!/usr/bin/env python3
"""Emit a reproducible Nintendo DS ROM baseline inventory as JSON without redistributing ROM contents."""
from __future__ import annotations
import argparse, collections, hashlib, json, os, struct, zlib

def u16(b,o): return struct.unpack_from('<H',b,o)[0]
def u32(b,o): return struct.unpack_from('<I',b,o)[0]
def hashes(b): return {'crc32':f'{zlib.crc32(b)&0xffffffff:08x}','md5':hashlib.md5(b).hexdigest(),'sha1':hashlib.sha1(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest()}
def parse_fnt(r,fo,fs,fa,fas):
 f=r[fo:fo+fs];dc=u16(f,6) if len(f)>=8 else 0;ds=[struct.unpack_from('<IHH',f,i*8) for i in range(dc)];es={}
 for i,(so,fi,_pa) in enumerate(ds):
  p=so;a=[]
  while p<len(f):
   v=f[p];p+=1
   if not v: break
   d=bool(v&0x80);n=v&0x7f;nm=f[p:p+n].decode('ascii','replace');p+=n
   if d: cid=u16(f,p)-0xf000;p+=2;a.append(('d',nm,cid))
   else: a.append(('f',nm,fi));fi+=1
  es[i]=a
 paths={}
 def walk(i,pre):
  for k,n,v in es.get(i,[]):
   if k=='f': paths[v]=pre+n
   else: walk(v,pre+n+'/')
 if ds: walk(0,'')
 fat=[struct.unpack_from('<II',r,fa+i*8) for i in range(fas//8)]
 return paths,fat,dc
def banner(r,o):
 if not o or o+0x840>len(r): return {}
 v=u16(r,o);cnt=6 if v==1 else 7 if v==2 else 8;langs=['ja','en','fr','de','it','es','zh','ko'];titles={}
 for i,lang in enumerate(langs[:cnt]):
  t=r[o+0x240+i*0x100:o+0x340+i*0x100].decode('utf-16le','replace').split('\x00',1)[0]
  if t: titles[lang]=t
 return {'version':v,'titles':titles}
def inventory(path):
 r=open(path,'rb').read();h=r[:0x200];fo,fs,fa,fas=struct.unpack_from('<IIII',h,0x40);o9,s9,o7,s7=struct.unpack_from('<IIII',h,0x50);paths,fat,dc=parse_fnt(r,fo,fs,fa,fas);ext=collections.Counter();top=collections.Counter()
 for i,_ in enumerate(fat):
  n=paths.get(i,f'__unnamed__/{i:04d}');top[n.split('/',1)[0]]+=1;ext[os.path.splitext(n)[1].lower() or '<none>']+=1
 return {'filename':os.path.basename(path),'size_bytes':len(r),'hashes':hashes(r),'header':{'title':h[:12].rstrip(b'\0').decode('ascii','replace'),'game_code':h[12:16].decode('ascii','replace'),'maker_code':h[16:18].decode('ascii','replace'),'unit_code':h[0x12],'device_capacity':h[0x14],'rom_version':h[0x1e],'arm9':{'offset':u32(h,0x20),'entry':u32(h,0x24),'ram':u32(h,0x28),'size':u32(h,0x2c)},'arm7':{'offset':u32(h,0x30),'entry':u32(h,0x34),'ram':u32(h,0x38),'size':u32(h,0x3c)},'fnt':{'offset':fo,'size':fs},'fat':{'offset':fa,'size':fas},'overlay9':{'offset':o9,'size':s9,'count':s9//32},'overlay7':{'offset':o7,'size':s7,'count':s7//32},'banner_offset':u32(h,0x68),'used_rom_size':u32(h,0x80),'header_size':u32(h,0x84)},'nitrofs':{'directory_count':dc,'fat_file_count':len(fat),'named_file_count':len(paths),'top_level_counts':dict(sorted(top.items())),'extension_counts':dict(sorted(ext.items()))},'banner':banner(r,u32(h,0x68))}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('rom');ap.add_argument('-o','--output');a=ap.parse_args();t=json.dumps(inventory(a.rom),ensure_ascii=False,indent=2)+'\n'
 if a.output: open(a.output,'w',encoding='utf-8').write(t)
 else: print(t,end='')
if __name__=='__main__': main()
