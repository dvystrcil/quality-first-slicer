# OrcaSlicer 2.5.0 dependency provenance

> **Updated to 2.5.0** in slice D1 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55) (2026-11-19). The declarations in §2 are now the 2.5.0 ones; each changed row keeps its v2.4.2 value, and components removed in 2.5.0 are in §2.3. The full change list is the [2.4.2 → 2.5.0 dependency delta](dependency-delta-2.4.2-to-2.5.0.md). The v2.4.2 text of this document is in Git history. **No dependency is approved by this document** ([AGENTS.md](../AGENTS.md) §6).

**Status:** Partial source audit; not a complete SBOM or license review  
**Reviewed revision:** fork `baseline-2.5.0` `665552c1e4b950b32707953cbca67e178e219366` (no build-file differences from upstream v2.5.0 `40ecc66f`); first pass at v2.4.2 `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**Scope:** Linux dependency path plus selected cross-platform dependency declarations  
**Source files:** `deps/CMakeLists.txt`, `deps/deps-linux.cmake`, `deps/deps-unix-common.cmake`, selected files under `deps/*/*.cmake`, and root `CMakeLists.txt`

This document records what the checked-in build scripts declare. Archive bytes are verified separately ([archive verification](archive-verification.md): every 2.5.0 source archive below matches its declared SHA-256). It does not establish upstream release authenticity, licenses, or a successful build, except where a linked review says so.

## 1. Build-system observations

- `deps/CMakeLists.txt` uses CMake `ExternalProject_Add` for a number of dependencies. Downloads are placed under a build-local cache directory; build/install options are passed to child projects.
- Linux includes `deps/deps-linux.cmake`, which includes `deps/deps-unix-common.cmake`. That common file probes for system ZLIB and leaves the bundled ZLIB path conditional. The top-level dependency file similarly probes for selected system packages in some configurations.
- The actual dependency set is therefore configuration- and platform-dependent. A single flat list of names is not an accurate build manifest.
- Some source-level `find_package` calls express minimum versions, while the dependency scripts may build a different, exact version. For example, the application CMake requests Boost 1.83.0 or newer while the bundled Boost project is 1.84.0. In 2.5.0 the application asks for `CGAL 6.2` (`src/libslic3r/CMakeLists.txt:627`), where v2.4.2 asked for any version.
- 2.5.0 adds the superbuild option `SLIC3R_CAD` (default ON, `deps/CMakeLists.txt:66`). It controls SLVS and OCCT's ModelingAlgorithms module, and must match the application's own `SLIC3R_CAD` (root `CMakeLists.txt:113`).
- The project has platform-specific dependency scripts for Linux, macOS, MinGW, and Windows. This first pass is not a full cross-platform dependency matrix.

## 2. Exact declarations observed

The versions, URLs, hashes, and tags below are transcribed from the named 2.5.0 CMake files. Every SHA-256 below was also independently re-calculated from the downloaded archive in slice A ([2.5.0 verification result](archive-verification.md#250-verification-result)). Components added in 2.5.0 (Assimp, libdatachannel, FFmpeg, SLVS, CPython, wxInspector, `uv`) are not repeated here; they are in [the delta §3](dependency-delta-2.4.2-to-2.5.0.md#3-added) with one review each.

### 2.1 Declarations (2.5.0)

| Component | Declared source/version (2.5.0) | Pin/integrity mechanism | Build-script location | Change from v2.4.2 |
|---|---|---|---|---|
| Boost | boostorg/boost release archive, 1.84.0 | SHA-256 `4d27e9efed0f6f152dc28db6430b9d3dfb40c0345da7342eaa5a987dde57bd95` | `deps/Boost/Boost.cmake` | flags only (§2.2) |
| Eigen | GitLab archive, 5.0.1 | SHA-256 `0dbb1f9e3aaad66f352c03227d8c983f6f0b49e0b07e71a7300f4abcc01aee12` | `deps/Eigen/Eigen.cmake` | flags only (§2.2) |
| CGAL | CGAL release archive, **6.2.1** (tag commit `28811b67`) | SHA-256 `eebd737d9b7f0199647ba5c1f9f6c7a3d0651aacef9c2fd4dedc52da6c25edbe` | `deps/CGAL/CGAL.cmake:10-11` | **was 5.6.3**, `5d577acb…`. See the [CGAL 6.2.1 review](cgal-6.2.1-package-license-review.md) |
| OpenSSL | OpenSSL_1_1_1w archive | SHA-256 `2130E8C2FB3B79D1086186F78E59E8BC8D1A6AEDF17AB3907F4CB9AE20918C41` | `deps/OpenSSL/OpenSSL.cmake:88-89` | flags only (§2.2) |
| curl | curl-7_75_0 tag archive | SHA-256 `a63ae025bb0a14f119e73250f2c923f4bf89aa93b8d4fafa4a9f5353a96a765a` | `deps/CURL/CURL.cmake` | flags only (§2.2) |
| wxWidgets | **OrcaSlicer**/Orca-deps-wxWidgets, **commit `b44c39c100975a0ac0e46f937aa3f3eae5e18631`**, shallow; submodules `3rdparty/catch`, `3rdparty/pcre`, `3rdparty/libwebp` | Git commit ID; no archive hash | `deps/wxWidgets/wxWidgets.cmake:34-37` | **was** SoftFever/Orca-deps-wxWidgets, shallow branch `v3.3.2`, all submodules. `b44c39c` is upstream wxWidgets v3.3.2 plus four fork commits. See the [wxWidgets fork review §0](wxwidgets-3.3.2-fork-provenance-review.md#0-orcaslicer-250-update-slice-d2-reviewed-2026-11-19) |
| OpenVDB | tamasmeszaros/openvdb archive at commit `a68fd58d0e2b85f01adeb8b13d7555183ab10aa5` | SHA-256 `f353e7b99bd0cbfc27ac9082de51acf32a8bc0b3e21ff9661ecca6f205ec1d81` | `deps/OpenVDB/OpenVDB.cmake` | unchanged |
| Open CASCADE (OCCT) | Open-Cascade-SAS/OCCT tag **`V8_0_1`** (tag commit `b8f597c6`); patch `0001-BRepMesh-seam-pcurve-at-edge-parameter.patch`; ModelingAlgorithms module = `${SLIC3R_CAD}` | SHA-256 `7c033d917ee8f040c0512d289dcc5f02c148889d5bac17c3e25639accb44f0da` | `deps/OCCT/OCCT.cmake:33-37`, `:59` | **was `V7_6_0`**, `28334f0e…`, patch `0001-OCCT-fix.patch` (deleted). FreeType dependency dropped (`USE_FREETYPE=OFF`). See the [OCCT 8.0.1 license-file check](occt-8.0.1-license-file-check.md) |
| Draco | Google Draco tag `1.5.7` | SHA-256 `27b72ba2d5ff3d0a9814ad40d4cb88f8dc89a35491c0866d952473f8f9416b77` | `deps/Draco/Draco.cmake` | flags only (§2.2) |
| OpenEXR | AcademySoftwareFoundation tag `v2.5.5` | SHA-256 `0307a3d7e1fa1e77e9d84d7e9a8694583fbbbfd50bdc6884e2c96b8ef6b902de` | `deps/OpenEXR/OpenEXR.cmake` | unchanged |
| oneTBB | oneapi-src tag `v2021.5.0` | SHA-256 `83ea786c964a384dd72534f9854b419716f412f9d43c0be88d41874763e7bb47` | `deps/TBB/TBB.cmake` | MSVC source replacement and flags (§2.2) |
| NLopt | stevengj/nlopt archive, 2.5.0 | SHA-256 `c6dd7a5701fff8ad5ebb45a3dc8e757e61d52658de3918e38bab233e7fd3b4ae` | `deps/NLopt/NLopt.cmake` | flags only (§2.2) |
| GMP | **GNU** `https://ftp.gnu.org/gnu/gmp/gmp-6.3.0.tar.xz` first, SoftFever/OrcaSlicer_deps release `gmp-6.3.0` second; **6.3.0** | SHA-256 `a3c2b80201b89e68616f4ad30bc66aee4927c3ce50e33929ca819d5c43538898` | `deps/GMP/GMP.cmake:65-68` | **was 6.2.1** from the SoftFever release asset only, `eae9326b…`. The GNU URL passed verification; the SoftFever mirror was not downloaded (the tool stops at the first match). `0001-GMP_GCC15.patch` edited. Non-MSVC only: MSVC still copies the committed prebuilt GMP (§3) |
| MPFR | GNU/MPFR archive, 4.2.2 | SHA-256 `9ad62c7dc910303cd384ff8f1f4767a655124980bb6d8650fe62c815a231bb7b` | `deps/MPFR/MPFR.cmake` | unchanged |
| Blosc | tamasmeszaros/c-blosc branch archive `v1.17.0_tm` | SHA-256 `dcb48bf43a672fa3de6a4b1de2c4c238709dad5893d1e097b8374ad84b1fc3b3` | `deps/Blosc/Blosc.cmake` | unchanged |
| libjpeg-turbo | GitHub tag archive **3.2.0** | SHA-256 `1b4c2cb6cba1ca5e53b9e85eeeab02154cab4b70894c96e97a9c747a26d19d63` | `deps/JPEG/JPEG.cmake:16-17` | **was 3.0.1**, `d6d99e69…`. `JPEG_VERSION` switch gone; `CMAKE_INSTALL_LIBDIR=lib`; hidden visibility on Linux (`:5-13`). Its `LICENSE.md` changed wording between the tags: "three" licenses became "two" (IJG and Modified BSD), with the zlib License now under "Component Licenses". Recorded, not reviewed |
| OpenCV | GitHub tag archive **4.14.0** | SHA-256 `ee8fb9b30eb60850431b4656447080e3737b56e45719c92b67f245950609f86e` | `deps/OpenCV/OpenCV.cmake:29-30` | **was 4.6.0**, `1ec1cba6…`, with patches `0001-vs.patch` and `0002-clang19-macos.patch` (both deleted). Now uses Orca's libjpeg-turbo and libpng (`BUILD_JPEG/BUILD_PNG=OFF`, `WITH_JPEG=ON`, `DEPENDS`, `:31`, `:40-42`, `:74-75`). AVIF, GIF and KleidiCV off (`:79-83`). Root `LICENSE` is the same blob at both tags (Apache-2.0) |
| libpng | glennrp/libpng tag archive **v1.6.59**, one path for all platforms | SHA-256 `6fd97a1e5e2ac55cec0a538a9800a351eb3844086736291844ebd12db72ba433` | `deps/PNG/PNG.cmake:2-3` | **was v1.6.35** (`3d22d46c…`) plus a Git checkout for Apple cross-compiles and three patches (all deleted). `LICENSE` changed from the "libpng license" (1.6.35) to "PNG Reference Library License version 2" (1.6.59). Recorded, not reviewed |

### 2.2 Build flags or patch files only (source pin unchanged)

Same archive URL and SHA-256 as v2.4.2. Details and line references are in [the delta §2.2](dependency-delta-2.4.2-to-2.5.0.md#22-build-flags-or-patch-files-only-source-pin-unchanged).

| Component | What changed in 2.5.0 |
|---|---|
| Boost 1.84.0 | clang-cl warning flag; `FORWARD_CONFIG` in MSVC debug |
| curl 7.75.0 | clang-cl C flags; two `ioctlsocket` probe overrides |
| Draco 1.5.7 | `FORWARD_CONFIG`; `DEP_LLD_FORCE_MULTIPLE` (clang-cl with Visual Studio) |
| Eigen 5.0.1 | testing, BLAS and LAPACK off |
| NLopt 2.5.0 | `DEP_LLD_FORCE_MULTIPLE` |
| OpenSSL 1.1.1w | hidden visibility on Linux (so the bundled CPython's `_ssl` does not mix with a system OpenSSL 3.x); `--libdir=lib`; `--openssldir=/etc/ssl` on macOS; MSVC toolchain pinning |
| oneTBB 2021.5.0 | **new `deps/TBB/MSVC.cmake`** (98 lines) copied over upstream's `cmake/compilers/MSVC.cmake` on MSVC (`deps/TBB/TBB.cmake:1-2`). This replaces an upstream source file, so it is part of the effective source; hwloc search and IPO off |
| EXPAT (in-tree `deps/EXPAT/expat`) | stale comment removed; no functional change |

### 2.3 Removed in 2.5.0

These are no longer declared in `deps/`. They are kept here as the v2.4.2 record.

| Component | v2.4.2 declaration | v2.4.2 location | 2.5.0 |
|---|---|---|---|
| OpenCSG | floriankirsch OpenCSG `opencsg-1-4-2-release`, SHA-256 `51afe0db79af8386e2027d56d685177135581e0ee82ade9d7f2caff8deab5ec5`, local `CMakeLists.txt.in` replacement | `deps/OpenCSG/OpenCSG.cmake:5-7`, included at `deps/CMakeLists.txt:344` | directory deleted |
| GLEW | vendored source under `deps/GLEW/glew`, no download | included at `deps/CMakeLists.txt:341` | directory deleted |
| FreeType | SoftFever `orca_deps` release 2.12.1, SHA-256 `efe71fd4b8246f1b0b1b9bfca13cfff1c9ad85930340c27df469733bbb620938`; the application did `find_package(Freetype REQUIRED)` and Windows copied `freetype.dll` | `deps/FREETYPE/FREETYPE.cmake:14-15`, included at `deps/CMakeLists.txt:397`; root `CMakeLists.txt:634`, `:839`, `:874` | directory deleted; no `find_package(Freetype)` in 2.5.0; OCCT built with `USE_FREETYPE=OFF` |

### Notes on interpretation

- The Boost declaration excludes several components and disables optional integrations; those build flags are part of the effective dependency definition.
- OpenSSL is built from the 1.1.1w source archive in this file. A commented-out 3.1.2 URL/hash is not the active declaration.
- curl is configured with several protocols and optional backends disabled and is configured to use OpenSSL.
- wxWidgets is sourced from an OrcaSlicer-maintained fork, not the canonical wxWidgets repository. In v2.4.2 the declaration followed a mutable branch name. **2.5.0 pins commit `b44c39c1` and names its three submodules**; the [fork review §0](wxwidgets-3.3.2-fork-provenance-review.md#0-orcaslicer-250-update-slice-d2-reviewed-2026-11-19) records the four-commit delta from upstream v3.3.2 and that PCRE2 10.47 and libwebp 1.6.0 are compiled into wxWidgets from those submodules.
- OpenVDB and Blosc use non-canonical fork/archive sources. Blosc's active source URL is a branch archive rather than a release tag or immutable commit URL, even though a checksum is declared. The checksum gives content integrity for the archive that was reviewed, but the branch name itself is mutable.
- GMP: in v2.4.2 it came only from a SoftFever release asset. In 2.5.0 the first URL is GNU's `ftp.gnu.org`, and the declared hash matched the bytes downloaded from it, so the source build now uses the canonical GNU 6.3.0 tarball. The local `0001-GMP_GCC15.patch` still applies. The MSVC build does not use this tarball at all (§3 and [Windows binary provenance](windows-binary-provenance.md)).
- OCCT, OpenEXR, OpenVDB and GMP include local patch steps, and oneTBB replaces one upstream file on MSVC. Those files are part of the effective source and must be retained, reviewed, and included in SBOM/provenance.
- Windows build logic copies GMP, MPFR, WebView2 loader, the OCCT toolkit DLLs that libslic3r links, and five FFmpeg DLLs into the application output (root `CMakeLists.txt:1111-1160`). FreeType is no longer copied. The binary and redistribution review must include those copied artifacts.

## 3. System dependencies and conditional behavior

The Linux path probes for system ZLIB. The root build also uses `find_package` for packages including Boost, Eigen, TBB, OpenSSL, curl, ZLIB, EXPAT, PNG, OpenGL, GLFW, cereal, NLopt, and OpenVDB (v2.4.2 also required FreeType; 2.5.0 does not). Some components can be built from the dependency scripts when not found; others are required from the configured prefix or system environment.

This means the eventual build manifest must record, per platform and build profile:

1. Whether a dependency came from the system, a vendored source directory, a downloaded ExternalProject, or a bundled binary.
2. The exact resolved version/revision and content hash.
3. The CMake options and local patches applied.
4. Whether it is linked statically or dynamically and whether it is redistributed.
5. Its license and required notices.

A successful build on one Linux distribution would not establish the same dependency set or licensing outcome for Windows/macOS.

## 4. High-priority provenance and reproducibility findings

1. **Mutable or non-canonical source references:** Blosc uses a branch archive from a fork. wxWidgets is now pinned to a commit in 2.5.0, but there is no archive hash for it. Resolve and record immutable commit IDs, retain archive hashes, and review the fork diffs against canonical upstream.
2. **Vendor-maintained dependency forks:** wxWidgets, OpenVDB and Blosc require an explicit origin/patch/maintenance rationale and file-level license review. GMP's source build now comes from GNU (§2.1). Do not assume fork ownership changes the upstream license, or that every fork modification has been separately documented.
3. **Local patches:** OCCT (a new patch in 2.5.0), OpenVDB and GMP patch files are applied during dependency builds; OpenEXR has platform-specific patch behavior; oneTBB replaces `MSVC.cmake` on MSVC. The OpenCV and libpng patches are gone in 2.5.0. Inventory patch contents and include modifications in SBOM/provenance.
4. **Binary redistribution:** Windows packaging copies multiple dependency DLLs, including WebView2Loader and FFmpeg. Trace each binary to its exact source/version/license and determine redistribution obligations. The Windows x64/x86 GMP and MPFR DLLs are **GMP 5.0.1 / MPFR 3.0.0**, not the 6.3.0 / 4.2.2 that every other platform builds ([Windows binary provenance](windows-binary-provenance.md)).
5. **License notices in third-party archives (new in 2.5.0):** OCCT 8.0.1 contains eight `TKGeomBase` files whose header calls them "commercial software" that "may not be provided … to any third party" ([OCCT check §3](occt-8.0.1-license-file-check.md#3-source-file-headers); upstream issue [Open-Cascade-SAS/OCCT#1564](https://github.com/Open-Cascade-SAS/OCCT/issues/1564) is open). CGAL 6.2.1's default mesh-segmentation path includes a GPL-3.0-or-later file with no commercial alternative ([CGAL 6.2.1 review §3.1](cgal-6.2.1-package-license-review.md#31-a-segmentation-header-without-the-commercial-option)).
6. **System-vs-bundled drift:** system package selection can change the effective binary and license inventory across machines. Define supported, reproducible build profiles rather than leaving the dependency source ambiguous.
7. **Version drift between declarations:** compare the versions required by the main source CMake against the versions actually built by dependency scripts and document any intentional mismatch.

## 5. Next audit work

- [x] Complete the first source-level dependency matrix for Linux, macOS, MinGW, and Windows; see [platform dependency matrix](platform-dependency-matrix.md). This is not a completed SBOM, independent hash verification, or build validation.
- [ ] Extract every active URL, Git repository/tag, commit, hash, patch, and conditional from all dependency CMake files.
- [ ] Resolve Git tags and branch archives to immutable commits; inspect the SoftFever-maintained dependency forks against their upstreams. (2.5.0: wxWidgets resolved, see [§0 of its review](wxwidgets-3.3.2-fork-provenance-review.md#0-orcaslicer-250-update-slice-d2-reviewed-2026-11-19); libdatachannel's tag resolved in its [review](libdatachannel-provenance-license-review.md); Blosc open.)
- [ ] Inspect the 26 third-party `deps_src` components and all nested license/notice files; the [MCUT/libigl license review](mcut-libigl-license-review.md), [CGAL license review](cgal-license-review.md), and [selected vendored source-header review](deps-src-license-header-review.md) document active use and remaining license/provenance questions. The `hints` subdirectory is an internal utility traced in the [hints provenance review](hints-utility-provenance.md), not a third-party dependency.
- [ ] Inspect the local patches and platform binary bundles; the first Windows GMP/MPFR/WebView2 binary inventory is documented in [Windows binary provenance](windows-binary-provenance.md).
- [x] 2.5.0: all 33 source-archive pins byte-verified, and the 12 hashed binary pins in a separate manifest ([archive verification](archive-verification.md)).
- [x] v2.4.2: Independently verify all 25 source archive entries against their recorded SHA-256 values. NanoSVG's former mismatch was traced to GitHub's repository rename redirect; all 16 files in the preserved archive match the exact pinned Git tree. The manifest now records the canonical URL and corrected archive digest. See [the verification procedure](archive-verification.md), [source archive manifest](../audit/orcaslicer-v2.4.2-source-archives.json), and [verification script](../tools/verify-source-archives.py).
- [x] Map dependency use from the real CMake target graph and per-TU preprocessor closure for the Linux x86_64 CI configuration; see [dependency/use map](dependency-use-map.md). Windows/macOS configurations remain unmapped.
- [ ] Generate an SBOM from the exact checked-out source/build configuration, then manually reconcile it with the CMake declarations.
- [ ] Complete license and notice review before importing any source or assets.

## 6. Current conclusion

The 2.5.0 build, like v2.4.2, is not a simple list of upstream packages. It combines system package discovery, vendored code, pinned archives, forked dependency sources, local patches, and platform-specific binary redistribution. A reproducible and legally reviewable fork baseline therefore needs a platform-specific dependency manifest and a provenance review of the maintained forks and copied binaries.

**No dependencies are approved for import by this document.** No SBOM generation, full build, or legal review has been performed for it. Archive verification has byte-level matches for every 2.5.0 source-archive pin (and for all 25 v2.4.2 entries before that). This remains distinct from authenticity, license, build, and legal review.
