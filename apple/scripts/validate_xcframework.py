#!/usr/bin/env python3
"""Validate slice metadata and link the FreeType public API for every architecture."""
from pathlib import Path
import argparse,plistlib,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[2]
import os
WORK=Path(os.environ.get("APPLE_BUILD_ROOT", str(ROOT))).expanduser().resolve()
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--artifacts',type=Path,default=WORK/'dist');a=p.parse_args()
artifact=a.artifacts/'FreeType.xcframework';info=plistlib.loads((artifact/'Info.plist').read_bytes())
assert len(info['AvailableLibraries'])==2
for entry in info['AvailableLibraries']:
    simulator=entry.get('SupportedPlatformVariant')=='simulator'
    assert entry['SupportedPlatform']=='ios'
    assert set(entry['SupportedArchitectures'])==({'arm64','x86_64'} if simulator else {'arm64'})
    folder=artifact/entry['LibraryIdentifier'];library=folder/entry['LibraryPath'];headers=folder/entry['HeadersPath']
    subprocess.run(['lipo',str(library),'-verify_arch',*entry['SupportedArchitectures']],check=True)
    sdk=subprocess.check_output(['xcrun','--sdk','iphonesimulator' if simulator else 'iphoneos','--show-sdk-path'],text=True).strip()
    for arch in entry['SupportedArchitectures']:
        triple=arch+'-apple-ios18.0'+('-simulator' if simulator else '')
        with tempfile.TemporaryDirectory(prefix='freetype-client-') as directory:
            client=Path(directory)/'client.c';client.write_text('#include <CFreeType.h>\nint main(void){FT_Library library; FT_Error result=FT_Init_FreeType(&library); if(!result) FT_Done_FreeType(library); return result;}\n')
            subprocess.run(['xcrun','clang','-target',triple,'-isysroot',sdk,'-fmodules','-fmodules-cache-path='+directory+'/modules','-I'+str(headers),str(client),str(library),'-o',directory+'/client'],check=True)
print('PASS: arm64 device, arm64 Simulator and x86_64 Simulator API linking')
