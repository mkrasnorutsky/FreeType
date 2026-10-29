#!/usr/bin/env python3
"""Build FreeType for arm64 iPhone and arm64/x86_64 Simulator; package a static XCFramework."""
import argparse, json, plistlib, shutil, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
import os
WORK=Path(os.environ.get("APPLE_BUILD_ROOT", str(ROOT))).expanduser().resolve()
def run(*args,**kw):
    print('+',' '.join(map(str,args)),flush=True)
    return subprocess.run(list(map(str,args)),check=True,**kw)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--jobs',type=int,default=6)
    p.add_argument('--output',type=Path,default=WORK/'dist')
    p.add_argument('--deployment-target',default='18.0')
    a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    configurations=[('ios-arm64','iphoneos','arm64'),('simulator-arm64','iphonesimulator','arm64'),('simulator-x86_64','iphonesimulator','x86_64')]
    built={}
    for label,sdk,arch in configurations:
        build=WORK/'out/apple'/label;prefix=build/'install'
        run('cmake','-S',ROOT,'-B',build,'-DCMAKE_SYSTEM_NAME=iOS','-DCMAKE_OSX_SYSROOT='+sdk,'-DCMAKE_OSX_ARCHITECTURES='+arch,
            '-DCMAKE_OSX_DEPLOYMENT_TARGET='+a.deployment_target,'-DCMAKE_BUILD_TYPE=Release','-DBUILD_SHARED_LIBS=OFF',
            '-DCMAKE_INSTALL_PREFIX='+str(prefix),'-DCMAKE_XCODE_ATTRIBUTE_CODE_SIGNING_ALLOWED=NO',
            *['-DFT_DISABLE_'+feature+'=ON' for feature in ['ZLIB','BZIP2','PNG','HARFBUZZ','BROTLI','HVF']])
        run('cmake','--build',build,'--parallel',a.jobs)
        run('cmake','--install',build)
        built[label]=prefix
    staging=out/'staging'
    if staging.exists():shutil.rmtree(staging)
    staging.mkdir()
    sim=staging/'libfreetype.a'
    run('lipo','-create',built['simulator-arm64']/'lib/libfreetype.a',built['simulator-x86_64']/'lib/libfreetype.a','-output',sim)
    headers=staging/'Headers';shutil.copytree(built['ios-arm64']/'include/freetype2',headers)
    (headers/'CFreeType.h').write_text('#pragma once\n#include <ft2build.h>\n#include FT_FREETYPE_H\n')
    (headers/'CFreeType').mkdir(exist_ok=True)
    (headers/'CFreeType/module.modulemap').write_text('module CFreeType {\n header "../CFreeType.h"\n export *\n}\n')
    artifact=out/'FreeType.xcframework'
    if artifact.exists():shutil.rmtree(artifact)
    run('xcodebuild','-create-xcframework','-library',built['ios-arm64']/'lib/libfreetype.a','-headers',headers,'-library',sim,'-headers',headers,'-output',artifact)
    notices=artifact/'Licenses';notices.mkdir()
    for name in ['LICENSE.TXT','docs/FTL.TXT','docs/GPLv2.TXT','docs/README','README']:
        source=ROOT/name
        if source.is_file():shutil.copy2(source,notices/source.name)
    revision=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
    (out/'build-manifest.json').write_text(json.dumps({'source_revision':revision,'minimum_ios':a.deployment_target,'slices':[x[0] for x in configurations],
        'disabled_optional_dependencies':['zlib','bzip2','png','harfbuzz','brotli','hvf'],'linkage':'static'},indent=2)+'\n')
    print('Created',artifact)
if __name__=='__main__':main()
