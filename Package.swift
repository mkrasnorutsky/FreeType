// swift-tools-version: 5.9
import PackageDescription
let package = Package(
    name: "FreeType",
    platforms: [.iOS("18.0")],
    products: [.library(name: "FreeType", targets: ["FreeType"])],
    targets: [
        .binaryTarget(name: "CFreeType", url: "https://github.com/mkrasnorutsky/FreeType/releases/download/0.1.0/FreeType.xcframework.zip", checksum: "78944338593587a4cdaf2ce6d39dc80fd51e2568e7648304ca1ebaba58779662"),
        .target(name: "FreeType", dependencies: ["CFreeType"], path: "apple/SPM", publicHeadersPath: "include")
    ]
)
