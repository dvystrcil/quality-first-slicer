# OrcaSlicer v2.4.2 platform dependency matrix

**Status:** Remote CMake-source inventory; not a completed SBOM, license audit, archive verification, or build validation  
**Upstream baseline:** [OrcaSlicer v2.4.2](https://github.com/OrcaSlicer/OrcaSlicer/tree/v2.4.2), commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**Reviewed:** 2026-11-03  
**Primary source files:** `deps/CMakeLists.txt`, `deps/deps-linux.cmake`, `deps/deps-macos.cmake`, `deps/deps-mingw.cmake`, `deps/deps-windows.cmake`, `deps/deps-unix-common.cmake`, and the component files under `deps/*/*.cmake`.

This document expands the earlier Linux-first inventory into a platform-selection matrix. It records active declarations visible in the v2.4.2 CMake source, including important conditionals. It does not establish that every dependency is built in every configuration: system-package discovery, `FLATPAK`, architecture, compiler, and cross-compilation options change the effective build.

## 1. Platform selection

The dependency project selects one platform file in this order:

| Build condition | Included file | Platform-specific behavior |
|---|---|---|
| `MSVC` | `deps/deps-windows.cmake` | Visual Studio toolset mapping; x86, x64, and ARM64 dependency bundles; optional Debug dependency builds |
| `APPLE` | `deps/deps-macos.cmake` | macOS deployment target (defaults to 11.3), SDK/framework search behavior, availability warnings treated as errors, cross-architecture handling |
| `MINGW` | `deps/deps-mingw.cmake` | GCC Boost toolset, 64-bit dependency setting, MinGW-specific TBB workaround |
| Otherwise | `deps/deps-linux.cmake` | Linux dependency path; position-independent code |

Linux and macOS include `deps/deps-unix-common.cmake`. MinGW also includes that common file. It probes for system ZLIB and warns if it is absent. The EXPAT probe in that common file is commented out, although the main dependency CMake later performs its own EXPAT discovery.

The platform files are primarily configuration overlays: most dependency source declarations live in shared component CMake files and are therefore reused across platforms, with selected platform-specific branches and patches described below.

## 2. Shared dependency source inventory

The following are active source declarations found in the v2.4.2 dependency CMake files. Hashes are copied from OrcaSlicer's build scripts; **none were independently recalculated in this review**.

| Component | Declared source / version | Declared integrity pin | Notes |
|---|---|---|---|
| Boost | boostorg/boost 1.84.0 release archive | SHA-256 `4d27e9efed0f6f152dc28db6430b9d3dfb40c0345da7342eaa5a987dde57bd95` | Selected components and build options are constrained in CMake |
| Cereal | USCiLab/cereal v1.3.0 | SHA-256 `71642cb54658e98c8f07a0f0d08bf9766f1c3771496936f6014169d3726d9657` | Archive |
| CGAL | CGAL 5.6.3 | SHA-256 `5d577acb4a9918ccb960491482da7a3838f8d363aff47e14d703f19fd84733d4` | Release archive |
| Draco | Google Draco 1.5.7 | SHA-256 `27b72ba2d5ff3d0a9814ad40d4cb88f8dc89a35491c0866d952473f8f9416b77` | Tag archive |
| Eigen | Eigen 5.0.1 | SHA-256 `0dbb1f9e3aaad66f352c03227d8c983f6f0b49e0b07e71a7300f4abcc01aee12` | GitLab archive |
| FreeType | SoftFever `orca_deps` release, 2.12.1 | SHA-256 `efe71fd4b8246f1b0b1b9bfca13cfff1c9ad85930340c27df469733bbb620938` | Release asset; shared build flags disable BZip2, PNG, HarfBuzz, and Brotli |
| GLFW | GLFW 3.4 | SHA-256 `a133ddc3d3c66143eba9035621db8e0bcf34dba1ee9514a9e23e96afd39fd57a` | Tag archive |
| GMP | SoftFever `OrcaSlicer_deps`, gmp-6.2.1 | SHA-256 `eae9326beb4158c386e39a356818031bd28f3124cf915f8c5b1dc4c7a36b4d7c` | Release asset; GCC15 patch applied on source-build path |
| JPEG | libjpeg-turbo 3.0.1 | SHA-256 `d6d99e693366bc03897677650e8b2dfa76b5d6c54e2c9e70c03f0af821b0a52f` | Built when not supplied by the selected package-discovery path |
| libnoise | SoftFever Orca-deps-libnoise tag 1.0 | SHA-256 `96ffd6cc47898dd8147aab53d7d1b1911b507d9dbaecd5613ca2649468afd8b6` | Forked source |
| MPFR | GNU MPFR 4.2.2 | SHA-256 `9ad62c7dc910303cd384ff8f1f4767a655124980bb6d8650fe62c815a231bb7b` | GNU archive; depends on GMP |
| NanoSVG | SoftFever nanosvg commit `863f6aa97ef62028126fa2c19bd4350394c2e15e` | SHA-256 `8d9c1624ad6518dd6dfa31e4f8dc7da9ec243d88bae595c7a037450617fec851` | Forked source archive |
| NLopt | stevengj/nlopt 2.5.0 | SHA-256 `c6dd7a5701fff8ad5ebb45a3dc8e757e61d52658de3918e38bab233e7fd3b4ae` | Archive |
| OCCT | Open-Cascade-SAS V7_6_0 | SHA-256 `28334f0e98f1b1629799783e9b4d21e05349d89e695809d7e6dfa45ea43e1dbc` | Local patch applied |
| OpenCSG | floriankirsch OpenCSG release `opencsg-1-4-2-release` | SHA-256 `51afe0db79af8386e2027d56d685177135581e0ee82ade9d7f2caff8deab5ec5` | Local CMakeLists replacement step |
| OpenCV | OpenCV 4.6.0 | SHA-256 `1ec1cba65f9f20fe5a41fda1586e01c70ea0c9a6d7b67c9e13edf0cfe2239277` | Platform-specific patch set |
| OpenEXR | AcademySoftwareFoundation v2.5.5 | SHA-256 `0307a3d7e1fa1e77e9d84d7e9a8694583fbbbfd50bdc6884e2c96b8ef6b902de` | Platform-specific patch behavior |
| OpenSSL | OpenSSL_1_1_1w | SHA-256 `2130E8C2FB3B79D1086186F78E59E8BC8D1A6AEDF17AB3907F4CB9AE20918C41` | Active declaration is 1.1.1w, not the commented 3.1.2 alternative |
| OpenVDB | tamasmeszaros/openvdb commit `a68fd58d0e2b85f01adeb8b13d7555183ab10aa5` | SHA-256 `f353e7b99bd0cbfc27ac9082de51acf32a8bc0b3e21ff9661ecca6f205ec1d81` | Fork plus local clang19 patch |
| PNG | libpng v1.6.35 | SHA-256 `3d22d46c566b1761a0e15ea397589b3a5f36ac09b7c785382e6470156c04247f` | Apple cross-compile branch uses Git tag instead of this archive path |
| Qhull | qhull v8.0.2 | SHA-256 `a378e9a39e718e289102c20d45632f873bfdc58a7a5f924246ea4b176e185f1e` | Added to dependency target except for MSVC |
| TBB | oneTBB v2021.5.0 | SHA-256 `83ea786c964a384dd72534f9854b419716f412f9d43c0be88d41874763e7bb47` | MinGW-specific workaround flag |
| wxWidgets | SoftFever Orca-deps-wxWidgets tag v3.3.2 | Shallow Git tag; no commit SHA in declaration | Linux GTK2/GTK3 selection; MSVC Edge WebView enabled |
| zlib | zlib v1.2.13 | SHA-256 `c2856951bbf30e30861ace3765595d86ba13f2cf01279d901f6c62258c57f4ff` | System package is probed first on Unix-like dependency path |
| curl | curl tag curl-7_75_0 | SHA-256 `a63ae025bb0a14f119e73250f2c923f4bf89aa93b8d4fafa4a9f5353a96a765a` | Configured with optional protocols/backends disabled; tied to OpenSSL |
| Blosc | tamasmeszaros/c-blosc branch v1.17.0_tm | SHA-256 `dcb48bf43a672fa3de6a4b1de2c4c238709dad5893d1e097b8374ad84b1fc3b3` | Fork branch archive; cross-compile Apple disables SSE2/AVX2 |

### Components not represented as ordinary pinned ExternalProjects

- **GLEW:** `deps/GLEW/GLEW.cmake` does not declare a normal downloaded ExternalProject in the reviewed file. Its actual provider and version need to be traced through the application build and platform package environment.
- **EXPAT:** if no acceptable package is found, the application build can compile the source under `src/expat`. This is a source-tree fallback, not the same acquisition path as the external archives above.
- **WebView2Loader:** Windows packaging copies architecture-specific loader DLLs from `deps/WebView2/lib/win-{x86,x64,arm64}`. The source, version, license, and notices for these binary files need a dedicated review.
- **GMP and MPFR on MSVC:** these are not built from the GNU source archives on that path. Headers, import libraries, and DLLs are copied from `deps/GMP/gmp` and `deps/MPFR/mpfr` architecture-specific directories. Their exact binary provenance is still unresolved.

## 3. Platform-by-platform matrix

| Area | Linux | macOS | MinGW | Windows / MSVC |
|---|---|---|---|---|
| Platform file | `deps-linux.cmake` | `deps-macos.cmake` | `deps-mingw.cmake` | `deps-windows.cmake` |
| Common dependency logic | Unix common | Unix common | Unix common | Shared component declarations; no Unix common include |
| Compiler/toolchain | Host toolchain | Apple Clang / selected SDK | GCC toolset | Visual Studio toolset; Clang-cl changes Boost toolset |
| Supported architecture details in dependency script | Host architecture; GMP has ARM-specific handling | Single architecture per dependency build; explicit cross-compile handling | `DEP_BITS=64` | x86, x64, ARM64 |
| Position-independent code | Enabled | Enabled | Enabled | Not set by platform file |
| ZLIB | System probe; build fallback if not found | System probe; build fallback if not found | System probe; build fallback if not found | Dependency fallback/package path |
| PNG | Shared archive path | Archive path; Apple patches; cross-compile uses Git tag and Apple ARM patch | Shared archive path | Shared archive path; Debug dependency build can be added |
| Blosc | Fork branch archive | Same fork; cross-compile disables SSE2/AVX2 | Shared fork archive | Shared fork archive; Debug dependency build can be added |
| OpenEXR | GCC13 patch | Cross-compile has architecture-specific build handling | Shared source; no Linux GCC patch branch | ARM64-specific SSE-disable patch; Debug dependency build can be added |
| GMP / MPFR | Build from source archives | Build from source; macOS architecture and cross-compile flags | Build from source path | Copy prebuilt headers/libs/DLLs from repository directories |
| FreeType | Shared release asset; static build; zlib integration enabled | Shared release asset; static build | Shared release asset; static build | Shared release asset; DLL build; Debug dependency build can be added |
| wxWidgets | GTK2 by default; GTK3 when `DEP_WX_GTK3` is enabled | Shared fork/tag; native macOS toolkit defaults | Shared fork/tag | Shared fork/tag; Edge WebView enabled; architecture-specific library directory |
| Qhull | Included | Included | Included | Omitted from `_dep_list` for MSVC |
| Windows runtime packaging | Not applicable to this packaging path | Not applicable to this packaging path | Not the MSVC DLL-copy path | Copies GMP, MPFR, WebView2Loader, OCCT, and FreeType DLLs |

This table is a source-level description, not a statement that all configurations have been built or tested.

## 4. Important conditional behavior

### 4.1 System packages and bundled fallbacks

The effective dependency set is not identical across build environments.

- Unix common logic probes for ZLIB. If not found, the dependency project builds its pinned zlib source.
- The dependency project conditionally builds PNG, EXPAT, OpenSSL, curl, JPEG, and FreeType based on package-discovery results. The `FLATPAK` path performs an explicit initial discovery pass for several of these packages.
- EXPAT can fall back to the source under `src/expat`.
- curl is built if either OpenSSL or curl is not found by the dependency project; its build is configured around OpenSSL.
- wxWidgets is always declared by the dependency project, but Flatpak handles it separately.
- Build scripts and package-discovery order must be captured in any future reproducible build profile. Do not infer that a package is bundled solely because a component CMake file exists.

### 4.2 Platform- and architecture-specific patches

The following conditions were visible in the source:

- **PNG:** Apple builds apply `PNG.patch` and `0002-clang19-macos.patch`; Apple cross-compilation instead checks out libpng v1.6.35 from Git and applies `macos-arm64.patch` plus the clang19 patch. Apple ARM disables the NEON extension.
- **Blosc:** Apple cross-compilation disables SSE2 and AVX2. Both branches use the same mutable fork-branch archive and declared hash.
- **OpenEXR:** Linux applies `0001-OpenEXR-GCC13.patch`; Windows ARM64 applies `patch_openexr_arm64.cmake` and disables SSE-related build options. Apple cross-compilation has special architecture handling for generated helper binaries.
- **OpenCV:** CMake declares `0001-vs.patch` and `0002-clang19-macos.patch`; exact conditions and patch content remain to be reviewed.
- **OCCT:** applies `0001-OCCT-fix.patch`.
- **OpenVDB:** applies `0001-clang19.patch`.
- **GMP:** applies `0001-GMP_GCC15.patch` on the source-build path.
- **OpenCSG:** copies a project-local `CMakeLists.txt.in` into the downloaded source tree.
- **TBB:** MinGW sets a `-flifetime-dse=1` workaround.

The presence of a patch is part of the dependency's effective source and must be represented in the provenance record and SBOM reconciliation.

### 4.3 Windows architecture and binary packaging

The MSVC dependency path explicitly recognizes x86, x64, and ARM64. It maps the active Visual Studio compiler version to a Boost toolset and selects the corresponding wxWidgets library directory. The main application packaging helper copies:

- GMP DLL and MPFR DLL for the selected architecture;
- WebView2Loader.dll for the selected architecture;
- OCCT runtime DLLs;
- FreeType DLL.

This is a separate binary-provenance and redistribution review, not covered by the source archive table. MinGW does not use the MSVC-specific prebuilt GMP/MPFR branch described above.

## 5. Reproducibility and audit gaps

| Gap | Why it matters | Required evidence |
|---|---|---|
| System-vs-bundled resolution | Different hosts can produce different dependency inventories | Per-platform configure logs, package versions, cache variables, and resolved link inputs |
| wxWidgets shallow tag | Tag declaration does not record immutable commit | Resolve v3.3.2 to commit and capture submodule state |
| Blosc branch archive | Branch name is mutable | Independently verify archive hash; retain immutable source commit/archive |
| FreeType/GMP/NanoSVG/libnoise fork sources | Non-canonical sources require origin and patch review | Compare source archives to upstream, document fork delta and release process |
| Windows GMP/MPFR/WebView2 binaries | Source archive review does not establish binary provenance | Hashes, version metadata, license/notice files, origin, and redistribution analysis |
| Platform patch behavior | Patch set changes effective source by target platform | Inspect every patch and record exact target conditions |
| Vendored source and assets | Not all code is acquired through ExternalProject | Inventory `deps_src`, `src` fallbacks, resources, fonts, models, and nested notices |
| Build execution | CMake declarations alone do not prove reproducibility | Clean build matrix with captured logs and artifact hashes |

## 6. Scope and confidence

- Source baseline and CMake paths were inspected remotely at the fixed v2.4.2 tag/commit.
- Platform selection and the listed active URLs, refs, hashes, and selected conditionals were read from those files.
- No local checkout or build was performed.
- No archive was downloaded or independently hash-verified.
- No binary was inspected.
- No complete fork diff, vendored-source scan, SBOM, or file-level license review was performed.
- The table is a dependency-source inventory, not a complete bill of materials. Transitive dependencies, toolchain/runtime libraries, operating-system packages, and all assets remain outside its coverage.

## 7. Next audit steps

- [ ] Resolve wxWidgets v3.3.2 to an immutable commit and record submodules.
- [ ] Independently download and verify all declared source archive hashes.
- [ ] Compare SoftFever FreeType, libnoise, NanoSVG, and GMP sources with their upstream equivalents; review Blosc/OpenVDB/wxWidgets findings from the preceding audit.
- [ ] Inspect all patches and record exact platform conditions, especially OpenCV, OCCT, PNG, OpenEXR, OpenVDB, GMP, and TBB.
- [ ] Inventory and hash Windows GMP/MPFR/WebView2 binaries and their notices.
- [ ] Trace GLEW and all system-provided dependencies to exact package/version sources.
- [ ] Inventory vendored `deps_src`, source fallbacks, profiles, fonts, models, certificates, and other assets.
- [ ] Produce per-platform configure/build evidence and reconcile an SBOM against the source inventory.
- [ ] Complete file-level license and redistribution review before importing source or assets.

## 8. Conclusion

The v2.4.2 build shares a broad dependency set across platforms, but it is not one uniform dependency graph. Platform selection changes compiler flags, source acquisition paths, patches, architecture handling, system-package substitution, and binary packaging. In particular, MSVC has a distinct prebuilt GMP/MPFR and DLL packaging path; macOS cross-compilation changes PNG and OpenEXR handling; Linux applies an OpenEXR GCC patch; and MinGW has its own compiler/TBB settings.

This matrix improves the source-level inventory but does not approve any dependency for import or settle the project's license. The next meaningful gate is independent archive/binary verification and a reproducible per-platform configure/build record.
