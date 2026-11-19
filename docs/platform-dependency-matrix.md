# OrcaSlicer 2.5.0 platform dependency matrix

> **Updated to 2.5.0** in slice D1 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55) (2026-11-19). Changed rows say what they were in v2.4.2; components removed in 2.5.0 are in §2.2. The full change list is the [2.4.2 → 2.5.0 dependency delta](dependency-delta-2.4.2-to-2.5.0.md); the v2.4.2 text is in Git history. **No dependency is approved by this document** ([AGENTS.md](../AGENTS.md) §6).

**Status:** CMake-source inventory; not a completed SBOM, license audit, or build validation  
**Baseline:** fork `baseline-2.5.0` `665552c1e4b950b32707953cbca67e178e219366` (no build-file differences from upstream [v2.5.0](https://github.com/OrcaSlicer/OrcaSlicer/tree/v2.5.0) `40ecc66f`); first written against [v2.4.2](https://github.com/OrcaSlicer/OrcaSlicer/tree/v2.4.2) `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**Reviewed:** 2026-11-03 (v2.4.2); 2026-11-19 (2.5.0 update)  
**Primary source files:** `deps/CMakeLists.txt`, `deps/deps-linux.cmake`, `deps/deps-macos.cmake`, `deps/deps-mingw.cmake`, `deps/deps-windows.cmake`, `deps/deps-unix-common.cmake`, and the component files under `deps/*/*.cmake`.

This document expands the earlier Linux-first inventory into a platform-selection matrix. It records active declarations visible in the 2.5.0 CMake source, including important conditionals. It does not establish that every dependency is built in every configuration: system-package discovery, `FLATPAK`, architecture, compiler, and cross-compilation options change the effective build.

## 1. Platform selection

The dependency project selects one platform file in this order:

| Build condition | Included file | Platform-specific behavior |
|---|---|---|
| `MSVC` | `deps/deps-windows.cmake` | Visual Studio toolset mapping; x86, x64, and ARM64 dependency bundles; optional Debug dependency builds; `DEP_LLD_FORCE_MULTIPLE` for clang-cl with Visual Studio (new in 2.5.0) |
| `APPLE` | `deps/deps-macos.cmake` | macOS deployment target (defaults to **12.0** in 2.5.0, `deps/CMakeLists.txt:31`; was 11.3), SDK/framework search behavior, availability warnings treated as errors, cross-architecture handling |
| `MINGW` | `deps/deps-mingw.cmake` | GCC Boost toolset, 64-bit dependency setting, TBB-related variable set (consumer unverified) |
| Otherwise | `deps/deps-linux.cmake` | Linux dependency path; position-independent code |

Linux and macOS include `deps/deps-unix-common.cmake`. MinGW also includes that common file. It probes for system ZLIB and warns if it is absent. The EXPAT probe in that common file is commented out, although the main dependency CMake later performs its own EXPAT discovery.

The platform files are primarily configuration overlays: most dependency source declarations live in shared component CMake files and are therefore reused across platforms, with selected platform-specific branches and patches described below.

## 2. Shared dependency source inventory

The following are active source declarations found in the 2.5.0 dependency CMake files. Hashes are copied from OrcaSlicer's build scripts. Every source-archive hash was also independently recalculated in slice A ([archive verification](archive-verification.md#250-verification-result)). Components added in 2.5.0 (Assimp, libdatachannel, FFmpeg, SLVS, CPython, wxInspector) are listed in [the delta §3](dependency-delta-2.4.2-to-2.5.0.md#3-added), with one review each; they are not repeated here.

| Component | Declared source / version | Declared integrity pin | Notes |
|---|---|---|---|
| Boost | boostorg/boost 1.84.0 release archive | SHA-256 `4d27e9efed0f6f152dc28db6430b9d3dfb40c0345da7342eaa5a987dde57bd95` | Selected components and build options are constrained in CMake |
| Cereal | USCiLab/cereal v1.3.0 | SHA-256 `71642cb54658e98c8f07a0f0d08bf9766f1c3771496936f6014169d3726d9657` | Archive |
| CGAL | CGAL **6.2.1** (was 5.6.3) | SHA-256 `eebd737d9b7f0199647ba5c1f9f6c7a3d0651aacef9c2fd4dedc52da6c25edbe` | Release archive; the app requires `CGAL 6.2`. [Review](cgal-6.2.1-package-license-review.md) |
| Draco | Google Draco 1.5.7 | SHA-256 `27b72ba2d5ff3d0a9814ad40d4cb88f8dc89a35491c0866d952473f8f9416b77` | Tag archive |
| Eigen | Eigen 5.0.1 | SHA-256 `0dbb1f9e3aaad66f352c03227d8c983f6f0b49e0b07e71a7300f4abcc01aee12` | GitLab archive |
| GLFW | GLFW 3.4 | SHA-256 `a133ddc3d3c66143eba9035621db8e0bcf34dba1ee9514a9e23e96afd39fd57a` | Tag archive |
| GMP | GNU `ftp.gnu.org` gmp-**6.3.0** first, SoftFever `OrcaSlicer_deps` gmp-6.3.0 second (was SoftFever gmp-6.2.1 only) | SHA-256 `a3c2b80201b89e68616f4ad30bc66aee4927c3ce50e33929ca819d5c43538898` | Non-MSVC only; GCC15 patch (edited in 2.5.0) applied. The comment says 6.3.0 is needed on Apple silicon. MSVC uses committed prebuilt binaries instead (below) |
| JPEG | libjpeg-turbo **3.2.0** (was 3.0.1) | SHA-256 `1b4c2cb6cba1ca5e53b9e85eeeab02154cab4b70894c96e97a9c747a26d19d63` | Built when not supplied by the selected package-discovery path; hidden visibility on Linux; installs into `lib` |
| libnoise | SoftFever Orca-deps-libnoise tag 1.0 | SHA-256 `96ffd6cc47898dd8147aab53d7d1b1911b507d9dbaecd5613ca2649468afd8b6` | Forked source |
| MPFR | GNU MPFR 4.2.2 | SHA-256 `9ad62c7dc910303cd384ff8f1f4767a655124980bb6d8650fe62c815a231bb7b` | GNU archive; depends on GMP |
| NanoSVG | SoftFever nanosvg commit `863f6aa97ef62028126fa2c19bd4350394c2e15e` | SHA-256 `8d9c1624ad6518dd6dfa31e4f8dc7da9ec243d88bae595c7a037450617fec851` | Forked source archive |
| NLopt | stevengj/nlopt 2.5.0 | SHA-256 `c6dd7a5701fff8ad5ebb45a3dc8e757e61d52658de3918e38bab233e7fd3b4ae` | Archive |
| OCCT | Open-Cascade-SAS **V8_0_1** (was V7_6_0) | SHA-256 `7c033d917ee8f040c0512d289dcc5f02c148889d5bac17c3e25639accb44f0da` | New local patch `0001-BRepMesh-seam-pcurve-at-edge-parameter.patch`; ModelingAlgorithms module when `SLIC3R_CAD` is ON; no FreeType. [License-file check](occt-8.0.1-license-file-check.md) |
| OpenCV | OpenCV **4.14.0** (was 4.6.0) | SHA-256 `ee8fb9b30eb60850431b4656447080e3737b56e45719c92b67f245950609f86e` | No patches (both v2.4.2 patches deleted); uses Orca's JPEG and PNG; IPP on MSVC x64/x86 only; carotene off for clang-cl ARM64 |
| OpenEXR | AcademySoftwareFoundation v2.5.5 | SHA-256 `0307a3d7e1fa1e77e9d84d7e9a8694583fbbbfd50bdc6884e2c96b8ef6b902de` | Platform-specific patch behavior |
| OpenSSL | OpenSSL_1_1_1w | SHA-256 `2130E8C2FB3B79D1086186F78E59E8BC8D1A6AEDF17AB3907F4CB9AE20918C41` | Active declaration is 1.1.1w, not the commented 3.1.2 alternative |
| OpenVDB | tamasmeszaros/openvdb commit `a68fd58d0e2b85f01adeb8b13d7555183ab10aa5` | SHA-256 `f353e7b99bd0cbfc27ac9082de51acf32a8bc0b3e21ff9661ecca6f205ec1d81` | Fork plus local clang19 patch |
| PNG | libpng **v1.6.59** (was v1.6.35) | SHA-256 `6fd97a1e5e2ac55cec0a538a9800a351eb3844086736291844ebd12db72ba433` | One archive path for every platform; no patches (the v2.4.2 Apple Git checkout and three patches are gone) |
| Qhull | qhull v8.0.2 | SHA-256 `a378e9a39e718e289102c20d45632f873bfdc58a7a5f924246ea4b176e185f1e` | Added to dependency target except for MSVC |
| TBB | oneTBB v2021.5.0 | SHA-256 `83ea786c964a384dd72534f9854b419716f412f9d43c0be88d41874763e7bb47` | MinGW-specific workaround variable is set; consumption not verified. On MSVC, 2.5.0 copies `deps/TBB/MSVC.cmake` over upstream's (new) |
| wxWidgets | **OrcaSlicer**/Orca-deps-wxWidgets commit **`b44c39c100975a0ac0e46f937aa3f3eae5e18631`**; submodules `3rdparty/catch`, `3rdparty/pcre`, `3rdparty/libwebp` (was SoftFever, shallow branch `v3.3.2`, all submodules) | Git commit ID; no archive hash | Linux GTK2/GTK3 selection; MSVC Edge WebView enabled; PCRE2 and libwebp built in. [Fork review §0](wxwidgets-3.3.2-fork-provenance-review.md#0-orcaslicer-250-update-slice-d2-reviewed-2026-11-19) |
| zlib | zlib v1.2.13 | SHA-256 `c2856951bbf30e30861ace3765595d86ba13f2cf01279d901f6c62258c57f4ff` | System package is probed first on Unix-like dependency path |
| curl | curl tag curl-7_75_0 | SHA-256 `a63ae025bb0a14f119e73250f2c923f4bf89aa93b8d4fafa4a9f5353a96a765a` | Configured with optional protocols/backends disabled; tied to OpenSSL |
| Blosc | tamasmeszaros/c-blosc branch v1.17.0_tm | SHA-256 `dcb48bf43a672fa3de6a4b1de2c4c238709dad5893d1e097b8374ad84b1fc3b3` | Fork branch archive; cross-compile Apple disables SSE2/AVX2 |

Build flags changed in 2.5.0 for Boost, curl, Draco, Eigen, NLopt and OpenSSL with the same pins ([delta §2.2](dependency-delta-2.4.2-to-2.5.0.md#22-build-flags-or-patch-files-only-source-pin-unchanged)). EXPAT's in-tree CMake lost a stale comment only.

### Components not represented as ordinary pinned ExternalProjects

- **EXPAT:** if no acceptable package is found, the application build can compile the source under `src/expat`. This is a source-tree fallback, not the same acquisition path as the external archives above.
- **WebView2Loader:** Windows packaging copies architecture-specific loader DLLs from `deps/WebView2/lib/win-{x86,x64,arm64}`. The source, version, license, and notices for these binary files need a dedicated review.
- **GMP and MPFR on MSVC:** these are not built from the GNU source archives on that path. Headers, import libraries, and DLLs are copied from `deps/GMP/gmp` and `deps/MPFR/mpfr` architecture-specific directories, unchanged since v2.4.2. **Their versions differ from every other platform:** x64 and x86 are **GMP 5.0.1 / MPFR 3.0.0**, ARM64 is GMP 6.3.0 / MPFR 4.2.2, and the one shared header pair is 5.0.1 / 3.0.0. Linux, macOS and MinGW build GMP 6.3.0 / MPFR 4.2.2 from source. How the six DLLs were built is undocumented. See [Windows binary provenance](windows-binary-provenance.md).

### 2.2 Removed in 2.5.0

Kept as the v2.4.2 record. None of these is declared in the 2.5.0 `deps/` tree.

| Component | v2.4.2 declaration | v2.4.2 notes | 2.5.0 |
|---|---|---|---|
| OpenCSG | floriankirsch OpenCSG release `opencsg-1-4-2-release`, SHA-256 `51afe0db79af8386e2027d56d685177135581e0ee82ade9d7f2caff8deab5ec5` | Local CMakeLists replacement step | `deps/OpenCSG/` deleted |
| GLEW | `deps/GLEW/GLEW.cmake` declared no downloaded ExternalProject; source vendored under `deps/GLEW/glew` | Provider and version were never traced | `deps/GLEW/` deleted |
| FreeType | SoftFever `orca_deps` release 2.12.1, SHA-256 `efe71fd4b8246f1b0b1b9bfca13cfff1c9ad85930340c27df469733bbb620938` | Static on Linux/macOS, DLL on Windows and MinGW (`WIN32`); BZip2, PNG, HarfBuzz, Brotli off; Windows copied `freetype.dll` | `deps/FREETYPE/` deleted; OCCT `USE_FREETYPE=OFF`; no `freetype.dll` copy |

## 3. Platform-by-platform matrix

| Area | Linux | macOS | MinGW | Windows / MSVC |
|---|---|---|---|---|
| Platform file | `deps-linux.cmake` | `deps-macos.cmake` | `deps-mingw.cmake` | `deps-windows.cmake` |
| Common dependency logic | Unix common | Unix common | Unix common | Shared component declarations; no Unix common include |
| Compiler/toolchain | Host toolchain | Apple Clang / selected SDK | GCC toolset | Visual Studio toolset; Clang-cl changes Boost toolset |
| Supported architecture details in dependency script | Host architecture; GMP has ARM-specific handling | Single architecture per dependency build; explicit cross-compile handling; deployment target 12.0 (was 11.3) | `DEP_BITS=64` | x86, x64, ARM64 |
| Position-independent code | Enabled | Enabled | Enabled | Not set by platform file |
| ZLIB | System probe; build fallback if not found | System probe; build fallback if not found | System probe; build fallback if not found | Dependency fallback/package path |
| PNG | Shared archive path (v1.6.59) | Shared archive path; no patches (v2.4.2 had Apple patches and a Git-tag cross-compile path) | Shared archive path | Shared archive path; Debug dependency build can be added |
| Blosc | Fork branch archive | Same fork; cross-compile disables SSE2/AVX2 | Shared fork archive | Shared fork archive; Debug dependency build can be added |
| OpenEXR | GCC13 patch | Cross-compile has architecture-specific build handling | Shared source; no Linux GCC patch branch | ARM64-specific SSE-disable patch; Debug dependency build can be added |
| GMP / MPFR | Build from source archives (6.3.0 / 4.2.2) | Build from source (6.3.0 / 4.2.2); macOS architecture and cross-compile flags | Build from source path (6.3.0 / 4.2.2) | Copy prebuilt headers/libs/DLLs from repository directories: **5.0.1 / 3.0.0 on x64 and x86**, 6.3.0 / 4.2.2 on ARM64 |
| wxWidgets | GTK2 by default; GTK3 when `DEP_WX_GTK3` is enabled | Shared fork commit; native macOS toolkit defaults | Shared fork commit | Shared fork commit; Edge WebView enabled; precompiled headers off with clang-cl; architecture-specific library directory |
| OCCT | Static | Static | Shared (`WIN32`) | Shared; ARM64 with clang-cl builds OCCT with `cl` |
| Qhull | Included | Included | Included | Omitted from `_dep_list` for MSVC |
| Windows runtime packaging | Not applicable to this packaging path | Not applicable to this packaging path | Not the MSVC DLL-copy path | Copies GMP, MPFR, WebView2Loader, the OCCT toolkit DLLs libslic3r links (`OCCT_LIBS`, + TKFillet/TKOffset/TKBool with `SLIC3R_CAD`), and five FFmpeg DLLs. No FreeType (was copied in v2.4.2) |

This table is a source-level description, not a statement that all configurations have been built or tested.

## 4. Important conditional behavior

### 4.1 System packages and bundled fallbacks

The effective dependency set is not identical across build environments.

- Unix common logic probes for ZLIB. If not found, the dependency project builds its pinned zlib source.
- The dependency project conditionally builds PNG, EXPAT, OpenSSL, curl, and JPEG based on package-discovery results (v2.4.2 also FreeType). The `FLATPAK` path performs an explicit initial discovery pass for several of these packages.
- EXPAT can fall back to the source under `src/expat`.
- curl is built if either OpenSSL or curl is not found by the dependency project; its build is configured around OpenSSL.
- wxWidgets is always declared by the dependency project, but Flatpak handles it separately.
- Build scripts and package-discovery order must be captured in any future reproducible build profile. Do not infer that a package is bundled solely because a component CMake file exists.

### 4.2 Platform- and architecture-specific patches

The following conditions were visible in the source:

- **PNG:** no patches and no platform branch in 2.5.0. (v2.4.2: Apple builds applied `PNG.patch` and `0002-clang19-macos.patch`; Apple cross-compilation checked out libpng v1.6.35 from Git and applied `macos-arm64.patch`; Apple ARM disabled NEON.)
- **Blosc:** Apple cross-compilation disables SSE2 and AVX2. Both branches use the same mutable fork-branch archive and declared hash.
- **OpenEXR:** Linux applies `0001-OpenEXR-GCC13.patch`; Windows ARM64 applies `patch_openexr_arm64.cmake` and disables SSE-related build options. Apple cross-compilation has special architecture handling for generated helper binaries.
- **OpenCV:** no patches in 2.5.0 (v2.4.2 declared `0001-vs.patch` and `0002-clang19-macos.patch`). IPP is on only for MSVC x64/x86; carotene is off for clang-cl ARM64; a clang-cl template-parsing flag is added on MSVC.
- **OCCT:** applies `0001-BRepMesh-seam-pcurve-at-edge-parameter.patch` (28 lines, Open-Cascade-SAS/OCCT#572) on every platform. v2.4.2 applied `0001-OCCT-fix.patch` (deleted).
- **OpenVDB:** applies `0001-clang19.patch`.
- **GMP:** applies `0001-GMP_GCC15.patch` on the source-build path (edited in 2.5.0: unnamed parameters became named).
- **TBB:** on MSVC, copies `deps/TBB/MSVC.cmake` over upstream's `cmake/compilers/MSVC.cmake` (new in 2.5.0; a Flatpak GCC branch copies `GNU.cmake`). MinGW sets `TBB_MINGW_WORKAROUND=-flifetime-dse=1` in `deps-unix-common.cmake`; this pass did not establish where (or whether) that variable is consumed.

The presence of a patch is part of the dependency's effective source and must be represented in the provenance record and SBOM reconciliation.

### 4.3 Windows architecture and binary packaging

The MSVC dependency path explicitly recognizes x86, x64, and ARM64. OCCT's component CMake uses the broader `WIN32` condition for shared-library output (`deps/OCCT/OCCT.cmake:8-12`), so it also builds DLLs on MinGW. (In v2.4.2 FreeType did the same.) It maps the active Visual Studio compiler version to a Boost toolset and selects the corresponding wxWidgets library directory. The main application packaging helper (root `CMakeLists.txt:1111-1160`) copies:

- GMP DLL and MPFR DLL for the selected architecture (GMP 5.0.1 / MPFR 3.0.0 on x64 and x86; 6.3.0 / 4.2.2 on ARM64);
- WebView2Loader.dll for the selected architecture;
- the OCCT toolkit DLLs listed in `OCCT_LIBS` (`src/libslic3r/CMakeLists.txt:693-741`), failing the configure if one is missing;
- five FFmpeg DLLs from the prebuilt zips ([C1](ffmpeg-windows-prebuilt-review.md)).

v2.4.2 also copied the FreeType DLL; 2.5.0 does not.

This is a separate binary-provenance and redistribution review, not covered by the source archive table. MinGW does not use the MSVC-specific prebuilt GMP/MPFR branch described above.

## 5. Reproducibility and audit gaps

| Gap | Why it matters | Required evidence |
|---|---|---|
| System-vs-bundled resolution | Different hosts can produce different dependency inventories | Per-platform configure logs, package versions, cache variables, and resolved link inputs |
| wxWidgets source | 2.5.0 pins commit `b44c39c1` and three submodules; no archive hash | Resolved for 2.5.0 ([fork review §0](wxwidgets-3.3.2-fork-provenance-review.md#0-orcaslicer-250-update-slice-d2-reviewed-2026-11-19)); the v2.4.2 build commit stays unknown |
| Blosc branch archive | Branch name is mutable | Independently verify archive hash; retain immutable source commit/archive |
| NanoSVG/libnoise fork sources | Non-canonical sources require origin and patch review | Compare source archives to upstream, document fork delta and release process. (FreeType removed in 2.5.0; GMP's source build now verifies against the GNU URL) |
| Windows GMP/MPFR/WebView2 binaries | Source archive review does not establish binary provenance; x64/x86 GMP/MPFR are older major versions than every other platform | Hashed and version-read in [Windows binary provenance](windows-binary-provenance.md); build origin and GMP's `COPYING.LIB` still missing |
| Platform patch behavior | Patch set changes effective source by target platform | Inspect every patch and record exact target conditions |
| Vendored source and assets | Not all code is acquired through ExternalProject | Inventory `deps_src`, `src` fallbacks, resources, fonts, models, and nested notices |
| Build execution | CMake declarations alone do not prove reproducibility | Clean build matrix with captured logs and artifact hashes |

## 6. Scope and confidence

- Source baseline and CMake paths were inspected at the fixed v2.4.2 commit, and again at `665552c1` for the 2.5.0 update (`git show` on a local clone).
- Platform selection and the listed active URLs, refs, hashes, and selected conditionals were read from those files.
- No build was performed for this document.
- Archive hashes were verified separately ([archive verification](archive-verification.md)); Windows binaries in [Windows binary provenance](windows-binary-provenance.md).
- No complete fork diff, vendored-source scan, SBOM, or file-level license review was performed.
- The table is a dependency-source inventory, not a complete bill of materials. Transitive dependencies, toolchain/runtime libraries, operating-system packages, and all assets remain outside its coverage.

## 7. Next audit steps

- [x] Resolve wxWidgets to an immutable commit and record submodules (2.5.0 declares both; [fork review §0](wxwidgets-3.3.2-fork-provenance-review.md#0-orcaslicer-250-update-slice-d2-reviewed-2026-11-19)).
- [x] Independently download and verify all declared source archive hashes ([archive verification](archive-verification.md)).
- [ ] Compare SoftFever libnoise and NanoSVG sources with their upstream equivalents; review Blosc/OpenVDB findings from the preceding audit.
- [ ] Inspect all patches and record exact platform conditions, especially OCCT, OpenEXR, OpenVDB, GMP, and TBB (OpenCV and PNG have none in 2.5.0).
- [x] Inventory and hash Windows GMP/MPFR/WebView2 binaries and their notices ([Windows binary provenance](windows-binary-provenance.md)).
- [ ] Trace all system-provided dependencies to exact package/version sources.
- [ ] Inventory vendored `deps_src`, source fallbacks, profiles, fonts, models, certificates, and other assets.
- [ ] Produce per-platform configure/build evidence and reconcile an SBOM against the source inventory.
- [ ] Complete file-level license and redistribution review before importing source or assets.

## 8. Conclusion

The 2.5.0 build shares a broad dependency set across platforms, but it is not one uniform dependency graph. Platform selection changes compiler flags, source acquisition paths, patches, architecture handling, system-package substitution, and binary packaging. In particular, MSVC has a distinct prebuilt GMP/MPFR (older on x64/x86) and DLL packaging path and replaces a oneTBB build file; macOS cross-compilation changes OpenEXR handling; Linux applies an OpenEXR GCC patch; and MinGW sets a TBB-related variable whose consumption remains unverified. 2.5.0 removed the PNG and OpenCV platform patches, and FreeType, OpenCSG and GLEW altogether.

This matrix improves the source-level inventory but does not approve any dependency for import or settle the project's license. The next meaningful gate is independent archive/binary verification and a reproducible per-platform configure/build record.
