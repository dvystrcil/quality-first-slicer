# OrcaSlicer v2.4.2 dependency provenance — first pass

**Status:** Partial remote-source audit; not a complete SBOM or license review  
**Reviewed revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (`v2.4.2`)  
**Scope:** Linux dependency path plus selected cross-platform dependency declarations  
**Source files:** Upstream `deps/CMakeLists.txt`, `deps/deps-linux.cmake`, `deps/deps-unix-common.cmake`, selected files under `deps/*/*.cmake`, and root `CMakeLists.txt`

This document records what the checked-in build scripts declare. It does not independently verify remote archive contents, checksums, upstream release authenticity, licenses, or a successful build.

## 1. Build-system observations

- `deps/CMakeLists.txt` uses CMake `ExternalProject_Add` for a number of dependencies. Downloads are placed under a build-local cache directory; build/install options are passed to child projects.
- Linux includes `deps/deps-linux.cmake`, which includes `deps/deps-unix-common.cmake`. That common file probes for system ZLIB and leaves the bundled ZLIB path conditional. The top-level dependency file similarly probes for selected system packages in some configurations.
- The actual dependency set is therefore configuration- and platform-dependent. A single flat list of names is not an accurate build manifest.
- Some source-level `find_package` calls express minimum versions, while the dependency scripts may build a different, exact version. For example, the application CMake requests Boost 1.83.0 or newer while the bundled Boost project is 1.84.0.
- The project has platform-specific dependency scripts for Linux, macOS, MinGW, and Windows. This first pass is not a full cross-platform dependency matrix.

## 2. Exact declarations observed

The versions, URLs, hashes, and tags below are transcribed from the named v2.4.2 CMake files. SHA-256 values are upstream build-script declarations, not independently recalculated values.

| Component | Declared source/version | Pin/integrity mechanism | Build-script location |
|---|---|---|---|
| Boost | boostorg/boost release archive, 1.84.0 | SHA-256 `4d27e9efed0f6f152dc28db6430b9d3dfb40c0345da7342eaa5a987dde57bd95` | `deps/Boost/Boost.cmake` |
| Eigen | GitLab archive, 5.0.1 | SHA-256 `0dbb1f9e3aaad66f352c03227d8c983f6f0b49e0b07e71a7300f4abcc01aee12` | `deps/Eigen/Eigen.cmake` |
| CGAL | CGAL release archive, 5.6.3 | SHA-256 `5d577acb4a9918ccb960491482da7a3838f8d363aff47e14d703f19fd84733d4` | `deps/CGAL/CGAL.cmake` |
| OpenSSL | OpenSSL_1_1_1w archive | SHA-256 `2130E8C2FB3B79D1086186F78E59E8BC8D1A6AEDF17AB3907F4CB9AE20918C41` | `deps/OpenSSL/OpenSSL.cmake` |
| curl | curl-7_75_0 tag archive | SHA-256 `a63ae025bb0a14f119e73250f2c923f4bf89aa93b8d4fafa4a9f5353a96a765a` | `deps/CURL/CURL.cmake` |
| wxWidgets | SoftFever/Orca-deps-wxWidgets, tag `v3.3.2` | Shallow Git tag; no commit SHA or archive hash declared here | `deps/wxWidgets/wxWidgets.cmake` |
| OpenVDB | tamasmeszaros/openvdb archive at commit `a68fd58d0e2b85f01adeb8b13d7555183ab10aa5` | SHA-256 `f353e7b99bd0cbfc27ac9082de51acf32a8bc0b3e21ff9661ecca6f205ec1d81` | `deps/OpenVDB/OpenVDB.cmake` |
| Open CASCADE (OCCT) | Open-Cascade-SAS/OCCT tag `V7_6_0` | SHA-256 `28334f0e98f1b1629799783e9b4d21e05349d89e695809d7e6dfa45ea43e1dbc` | `deps/OCCT/OCCT.cmake` |
| Draco | Google Draco tag `1.5.7` | SHA-256 `27b72ba2d5ff3d0a9814ad40d4cb88f8dc89a35491c0866d952473f8f9416b77` | `deps/Draco/Draco.cmake` |
| OpenEXR | AcademySoftwareFoundation tag `v2.5.5` | SHA-256 `0307a3d7e1fa1e77e9d84d7e9a8694583fbbbfd50bdc6884e2c96b8ef6b902de` | `deps/OpenEXR/OpenEXR.cmake` |
| oneTBB | oneapi-src tag `v2021.5.0` | SHA-256 `83ea786c964a384dd72534f9854b419716f412f9d43c0be88d41874763e7bb47` | `deps/TBB/TBB.cmake` |
| NLopt | stevengj/nlopt archive, 2.5.0 | SHA-256 `c6dd7a5701fff8ad5ebb45a3dc8e757e61d52658de3918e38bab233e7fd3b4ae` | `deps/NLopt/NLopt.cmake` |
| GMP | SoftFever/OrcaSlicer_deps release, 6.2.1 | SHA-256 `eae9326beb4158c386e39a356818031bd28f3124cf915f8c5b1dc4c7a36b4d7c` | `deps/GMP/GMP.cmake` |
| MPFR | GNU/MPFR archive, 4.2.2 | SHA-256 `9ad62c7dc910303cd384ff8f1f4767a655124980bb6d8650fe62c815a231bb7b` | `deps/MPFR/MPFR.cmake` |
| Blosc | tamasmeszaros/c-blosc branch archive `v1.17.0_tm` | SHA-256 `dcb48bf43a672fa3de6a4b1de2c4c238709dad5893d1e097b8374ad84b1fc3b3` | `deps/Blosc/Blosc.cmake` |

### Notes on interpretation

- The Boost declaration excludes several components and disables optional integrations; those build flags are part of the effective dependency definition.
- OpenSSL is built from the 1.1.1w source archive in this file. A commented-out 3.1.2 URL/hash is not the active declaration.
- curl is configured with several protocols and optional backends disabled and is configured to use OpenSSL.
- wxWidgets is sourced from a SoftFever-maintained repository, not the canonical wxWidgets repository. The checked-in declaration uses a Git tag with shallow clone and does not record the resolved commit SHA. Treat this as a high-priority provenance and reproducibility item.
- OpenVDB and Blosc use non-canonical fork/archive sources. Blosc's active source URL is a branch archive rather than a release tag or immutable commit URL, even though a checksum is declared. The checksum gives content integrity for the archive that was reviewed, but the branch name itself is mutable.
- GMP is obtained from a SoftFever release asset rather than the GNU upstream URL. Its origin, patch, and release process need independent review.
- OCCT and OpenEXR include local patch steps. Those patch files are part of the effective source and must be retained, reviewed, and included in SBOM/provenance.
- Windows build logic also copies GMP, MPFR, WebView2 loader, OCCT, and FreeType DLLs into the application output. The binary and redistribution review must include those copied artifacts.

## 3. System dependencies and conditional behavior

The Linux path probes for system ZLIB. The root build also uses `find_package` for packages including Boost, Eigen, TBB, OpenSSL, curl, FreeType, ZLIB, EXPAT, PNG, OpenGL, GLFW, cereal, NLopt, and OpenVDB. Some components can be built from the dependency scripts when not found; others are required from the configured prefix or system environment.

This means the eventual build manifest must record, per platform and build profile:

1. Whether a dependency came from the system, a vendored source directory, a downloaded ExternalProject, or a bundled binary.
2. The exact resolved version/revision and content hash.
3. The CMake options and local patches applied.
4. Whether it is linked statically or dynamically and whether it is redistributed.
5. Its license and required notices.

A successful build on one Linux distribution would not establish the same dependency set or licensing outcome for Windows/macOS.

## 4. High-priority provenance and reproducibility findings

1. **Mutable or non-canonical source references:** wxWidgets uses a shallow tag from a SoftFever fork; Blosc uses a branch archive from a fork. Resolve and record immutable commit IDs, retain archive hashes, and review the fork diffs against canonical upstream.
2. **Vendor-maintained dependency forks:** wxWidgets, OpenVDB, Blosc, and GMP require an explicit origin/patch/maintenance rationale and file-level license review. Do not assume fork ownership changes the upstream license, or that every fork modification has been separately documented.
3. **Local patches:** OCCT and OpenVDB patch files are applied during dependency builds; OpenEXR has platform-specific patch behavior. Inventory patch contents and include modifications in SBOM/provenance.
4. **Binary redistribution:** Windows packaging copies multiple dependency DLLs, including WebView2Loader. Trace each binary to its exact source/version/license and determine redistribution obligations.
5. **System-vs-bundled drift:** system package selection can change the effective binary and license inventory across machines. Define supported, reproducible build profiles rather than leaving the dependency source ambiguous.
6. **Version drift between declarations:** compare the versions required by the main source CMake against the versions actually built by dependency scripts and document any intentional mismatch.

## 5. Next audit work

- [x] Complete the first source-level dependency matrix for Linux, macOS, MinGW, and Windows; see [platform dependency matrix](platform-dependency-matrix.md). This is not a completed SBOM, independent hash verification, or build validation.
- [ ] Extract every active URL, Git repository/tag, commit, hash, patch, and conditional from all dependency CMake files.
- [ ] Resolve Git tags and branch archives to immutable commits; inspect the SoftFever-maintained dependency forks against their upstreams.
- [ ] Inspect vendored `deps_src` projects and all nested license/notice files; the targeted [MCUT/libigl license review](mcut-libigl-license-review.md) confirms active use and identifies remaining transitive-license questions.
- [ ] Inspect the local patches and platform binary bundles; the first Windows GMP/MPFR/WebView2 binary inventory is documented in [Windows binary provenance](windows-binary-provenance.md).
- [x] Independently verify all 25 source archive entries against their recorded SHA-256 values. NanoSVG's former mismatch was traced to GitHub's repository rename redirect; all 16 files in the preserved archive match the exact pinned Git tree. The manifest now records the canonical URL and corrected archive digest. See [the verification procedure](archive-verification.md), [source archive manifest](../audit/orcaslicer-v2.4.2-source-archives.json), and [verification script](../tools/verify-source-archives.py).
- [ ] Generate an SBOM from the exact checked-out source/build configuration, then manually reconcile it with the CMake declarations.
- [ ] Complete license and notice review before importing any source or assets.

## 6. Current conclusion

The v2.4.2 build is not a simple list of upstream packages. It combines system package discovery, vendored code, pinned archives, forked dependency sources, local patches, and platform-specific binary redistribution. A reproducible and legally reviewable fork baseline therefore needs a platform-specific dependency manifest and a provenance review of the maintained forks and copied binaries.

**No dependencies are approved for import by this document.** No local source checkout, SBOM generation, build, or legal review has been performed. Archive verification now has byte-level matches for all 25 manifest entries, including the corrected NanoSVG archive pin. This remains distinct from authenticity, license, build, and legal review.
