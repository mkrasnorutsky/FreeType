// swift-tools-version: 5.9
import PackageDescription
let package = Package(
    name: "FreeType",
    platforms: [.iOS("18.0")],
    products: [.library(name: "FreeType", targets: ["FreeType"])],
    targets: [
        .binaryTarget(name: "CFreeType", path: "dist/FreeType.xcframework"),
        .target(name: "FreeType", dependencies: ["CFreeType"], path: "apple/SPM", publicHeadersPath: "include")
    ]
)
