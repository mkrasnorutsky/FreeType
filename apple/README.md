# FreeType for iOS and Swift Package Manager

The full tracked upstream source and history are preserved, based on revision `8f24d5a911d3c9a6574367cf992d1a73b9803d19`. This is the FreeType dependency needed by OpenSceneGraph's font plugin.

## Use the published package

Add `https://github.com/mkrasnorutsky/FreeType.git` in Xcode and select the **FreeType** product, version **0.1.0** or later. The package downloads a checksum-verified static XCFramework. It supports **arm64 iPhone, arm64 Simulator and x86_64 Simulator**, with iOS 18 minimum. Static linking avoids an additional runtime framework to embed or sign.

[Release 0.1.0](https://github.com/mkrasnorutsky/FreeType/releases/tag/0.1.0) includes the XCFramework ZIP, checksum and build manifest. SPM integrates prebuilt C code; it does not run CMake during package resolution.

## Build from source

Requirements: macOS, Xcode with iPhoneOS/iPhoneSimulator SDKs, Python 3, CMake and Git. No signing identity or third-party downloads are needed for the build.

```sh
git clone https://github.com/mkrasnorutsky/FreeType.git
cd FreeType
python3 apple/scripts/build_xcframework.py
python3 apple/scripts/validate_xcframework.py
```

CMake builds all three architectures separately, `lipo` merges only the Simulator libraries, and Xcode produces `dist/FreeType.xcframework`. All installed public headers and a Clang module map are included. `--jobs N`, `--output PATH` and `--deployment-target VERSION` configure builds. A manual GitHub Actions workflow runs the same build and validation steps.

To match OneClickPilot's existing font dependency, external zlib, bzip2, PNG, HarfBuzz, Brotli and HVF integrations are disabled. This package does not claim those optional capabilities. TrueType/OpenType font rendering remains available. The build manifest records these options.

To use rebuilt artifacts locally, copy `apple/Package.local.swift` to the root `Package.swift`, then add this folder as a local package. The binary module is **CFreeType**, and the wrapper/product is **FreeType**. Public C headers remain accessible through `ft2build.h` and `FT_*_H` include macros. Do not also link the old local FreeType archive.

## Release packaging

```sh
python3 apple/scripts/package_release.py --tag 0.2.0
```

Upload the generated ZIP and checksums to the corresponding GitHub release. Commit the generated `dist/Package.swift` as the root manifest at the release revision. Never replace published ZIP contents under an existing version: checksums are immutable.

## Licensing

Original licensing files are preserved and included in the XCFramework's `Licenses` directory. FreeType is dual-licensed under the FreeType Project License and GPLv2; select the appropriate terms for your distribution. Under the FreeType Project License, retain the license and attribution, including the required acknowledgement in your product documentation. See `docs/FTL.TXT` and `LICENSE.TXT` for the exact terms.
