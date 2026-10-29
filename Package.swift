// swift-tools-version: 5.9
import PackageDescription
let package = Package(
    name: "FreeType",
    platforms: [.iOS("18.0")],
    products: [.library(name: "FreeType", targets: ["FreeType"])],
    targets: [
        .binaryTarget(name: "CFreeType", url: "https://github.com/mkrasnorutsky/FreeType/releases/download/0.1.1/FreeType.xcframework.zip", checksum: "17cc8a2994007fa50cab824f8dee6ccd1585a6981c1bf467f1e8b2e01965c646"),
        .target(name: "FreeType", dependencies: ["CFreeType"], path: "apple/SPM", publicHeadersPath: "include")
    ]
)
