# Dependency delta: OrcaSlicer v2.4.2 → 2.5.0

**Status:** Inventory only ([0002](decisions/0002-base-on-orcaslicer-2.5.0.md) step 3, slice A of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)). It lists what changed in the dependency build files and says which slice of #55 reviews each change. It reviews nothing, approves nothing, and draws no legal conclusions. **No component added in 2.5.0 is approved** ([AGENTS.md](../AGENTS.md) §6) until its slice is done and the maintainer signs off.
**From:** upstream `v2.4.2` = [`8500fcdccaa10b5099ac20d252af3a7c560046f1`](https://github.com/OrcaSlicer/OrcaSlicer/tree/8500fcdccaa10b5099ac20d252af3a7c560046f1)
**To:** fork `baseline-2.5.0` = [`665552c1e4b950b32707953cbca67e178e219366`](https://github.com/dvystrcil/OrcaSlicer/commit/665552c1e4b950b32707953cbca67e178e219366). It has no differences from upstream `v2.5.0` (`40ecc66f78ed72dc368e0c1ebe40d77f00cc8a19`) under `deps/`, `deps_src/`, `cmake/`, the root `CMakeLists.txt` or `src/CMakeLists.txt` (`git diff --stat v2.5.0 665552c1 -- …` is empty), so every line reference below is also valid for upstream v2.5.0.
**Method:** `git diff --name-status 8500fcdc 665552c1 -- deps deps_src`, then reading each changed build file. Line numbers are 2.5.0 unless marked "2.4.2". Pins were cross-checked by [`tools/check-archive-manifest-coverage.py`](../tools/check-archive-manifest-coverage.py) (section 5).
**Machine-readable pins:** [`audit/orcaslicer-v2.5.0-source-archives.json`](../audit/orcaslicer-v2.5.0-source-archives.json)
**Reviewed:** 2026-11-08

## 1. Summary

`git diff --stat` reports 148 files changed under `deps/` and `deps_src/` (27,848 insertions, 71,039 deletions; most of the deletions are vendored GLEW and legacy Clipper).

| Class | Components | Reviewed in |
|---|---|---|
| **Source pin changed** | CGAL, GMP, libjpeg-turbo, OCCT, OpenCV, libpng, wxWidgets | slice D |
| **Build flags or patches only** (same source pin) | Boost, curl, Draco, Eigen, NLopt, OpenSSL, oneTBB, EXPAT (comment only) | slice D |
| **Added: source** | Assimp, libdatachannel, FFmpeg (source build), SLVS, CPython 3.12.13 (+ Windows build externals), pybind11 (`deps_src`), wxInspector | slice B: reviewed, **not approved** (links in §3) |
| **Added: binary** | FFmpeg Windows prebuilt zips, CPython Windows `bin-deps`, nuget host Python (build-time), `uv` 0.11.21 (root `CMakeLists.txt`) | slice C |
| **Removed** | OpenCSG, GLEW, FreeType (`deps/`), legacy Clipper (`deps_src/clipper`) | historical banners here (A6); tables in slice D |
| **Vendored source changed** | clipper2 1.5.2 → 2.0.1, libigl, libnest2d, imgui, imguizmo, admesh, mcut, miniz, qhull, semver | slice D4 |
| **Unchanged pins** | Blosc, Cereal, GLFW, MPFR, NanoSVG (not built), OpenEXR, OpenVDB, Qhull, zlib, libnoise | none; still covered by the existing reviews |

## 2. Changed dependency declarations (`deps/`)

### 2.1 Source pin changed

| Component | v2.4.2 | 2.5.0 | Evidence | Notes from the files |
|---|---|---|---|---|
| CGAL | 5.6.3 release zip, SHA-256 `5d577acb…` | **6.2.1** release zip, SHA-256 `eebd737d…` | `deps/CGAL/CGAL.cmake:10-11` (2.4.2: same lines) | Major version. The commented `GIT_TAG` now names `28811b67` "# v6.2.1". The [CGAL 5.6.3 package review](cgal-5.6.3-package-license-review.md) does not apply to 6.2.1 as is |
| GMP | 6.2.1 `.tar.bz2`, SoftFever release asset only, `eae9326b…` | **6.3.0** `.tar.xz`, `ftp.gnu.org` first, SoftFever release asset second, `a3c2b802…` | `deps/GMP/GMP.cmake:66-68` (2.4.2: `:63-64`) | The comment at `:62-64` says 6.3.0 is needed for Apple silicon. The canonical GNU URL is now the primary source. `0001-GMP_GCC15.patch` changed: unnamed parameters became named (`deps/GMP/0001-GMP_GCC15.patch`, 3 hunks). The MSVC prebuilt GMP is unchanged in kind (slice C4) |
| libjpeg-turbo | 3.0.1, `d6d99e69…` | **3.2.0**, `1b4c2cb6…` | `deps/JPEG/JPEG.cmake:16-17` (2.4.2: `:15-16`) | The `JPEG_VERSION` 6/7/8 API switch is gone; hidden visibility on Linux; `CMAKE_INSTALL_LIBDIR=lib` |
| OCCT | `V7_6_0`, `28334f0e…`, patch `0001-OCCT-fix.patch` | **`V8_0_1`**, `7c033d91…`, patch `0001-BRepMesh-seam-pcurve-at-edge-parameter.patch` | `deps/OCCT/OCCT.cmake:33-37` (2.4.2: `:12-15`) | Major version. The old 221-line patch was deleted; the new 28-line patch refers to Open-Cascade-SAS/OCCT#572. `BUILD_MODULE_ModelingAlgorithms=${SLIC3R_CAD}` (`:59`). The comment at `:14-26` says this builds TKFillet and TKOffset (used) plus TKFeat, TKHelix, TKXMesh and TKExpress (unreferenced), and that Windows then ships the TKFillet, TKOffset and TKBool DLLs. FreeType dependency dropped; `USE_FREETYPE=OFF` |
| OpenCV | 4.6.0, `1ec1cba6…`, patches `0001-vs.patch`, `0002-clang19-macos.patch` | **4.14.0**, `ee8fb9b3…`, no patches | `deps/OpenCV/OpenCV.cmake:29-30` (2.4.2: `:14-16`) | Both patch files deleted. `BUILD_JPEG/BUILD_PNG=OFF` and `WITH_JPEG=ON`: OpenCV now uses Orca's libjpeg-turbo and libpng (`:40-42`, `:74-75`). New codecs/HALs explicitly off: AVIF, GIF, KleidiCV (`:79-83`, the comment says KleidiCV "is downloaded at configure time") |
| libpng | v1.6.35 zip `3d22d46c…`; Apple cross-compile used a Git checkout of tag v1.6.35; three patches | **v1.6.59** zip, `6fd97a1e…`, one path for all platforms, no patches | `deps/PNG/PNG.cmake:2-3` (2.4.2: `:11-14`, `:27`, `:32-33`) | `PNG.patch`, `0002-clang19-macos.patch` and `macos-arm64.patch` deleted; the Git path and its excluded pin `png-apple-cross` are gone |
| wxWidgets | `SoftFever/Orca-deps-wxWidgets`, `GIT_TAG v3.3.2`, shallow | **`OrcaSlicer/Orca-deps-wxWidgets`**, `GIT_TAG b44c39c100975a0ac0e46f937aa3f3eae5e18631`, shallow, `GIT_SUBMODULES 3rdparty/catch 3rdparty/pcre 3rdparty/libwebp` | `deps/wxWidgets/wxWidgets.cmake:34-37` (2.4.2: `:26-27`) | The repository moved organisations and the pin is now a **commit**, which addresses the "no commit SHA" finding in the [provenance audit](dependency-provenance-audit.md) §4. The submodule list is now explicit. Whether `b44c39c` is the v3.3.2 tag commit is not checked here (slice D2). `wxBUILD_PRECOMP` is off with clang-cl (`:24-30`) |

### 2.2 Build flags or patch files only (source pin unchanged)

Decision 0002 lists these as "modified". The archive URL and SHA-256 are the same as in v2.4.2 for each one; only how they are built changed.

| Component | What changed | Evidence |
|---|---|---|
| Boost 1.84.0 | `-Wno-incompatible-pointer-types` for clang-cl; `FORWARD_CONFIG` in MSVC debug | `deps/Boost/Boost.cmake:27-56` |
| curl 7.75.0 | clang-cl C flags and two `ioctlsocket` probe overrides | `deps/CURL/CURL.cmake:59-85` |
| Draco 1.5.7 | `FORWARD_CONFIG` in MSVC debug; `DEP_LLD_FORCE_MULTIPLE` | `deps/Draco/Draco.cmake:1-12` |
| Eigen 5.0.1 | `EIGEN_BUILD_TESTING/BLAS/LAPACK=OFF` | `deps/Eigen/Eigen.cmake:10-24` |
| NLopt 2.5.0 | `DEP_LLD_FORCE_MULTIPLE` | `deps/NLopt/NLopt.cmake:11-12` |
| OpenSSL 1.1.1w | `-fvisibility=hidden` on Linux; `--libdir=lib`; `--openssldir=/etc/ssl` on macOS; MSVC toolchain pinning; an object-clean step. The comment at `:57-67` says the visibility change keeps the bundled CPython's `_ssl`/`_hashlib` from mixing with the system OpenSSL 3.x | `deps/OpenSSL/OpenSSL.cmake` |
| oneTBB 2021.5.0 | New `deps/TBB/MSVC.cmake` copied over upstream's on MSVC (a source replacement, 98 lines); hwloc search and IPO off | `deps/TBB/TBB.cmake:1-6`, `:18-20` |
| EXPAT (in-tree `deps/EXPAT/expat`) | A stale GLEW comment removed; no functional change | `deps/EXPAT/EXPAT.cmake` |
| Superbuild | CMake minimum 3.10; macOS deployment target 11.3 → 12.0; new option `SLIC3R_CAD` (default ON); `FORWARD_CONFIG` and `SOURCE_DIR` support in `orcaslicer_add_cmake_project`; `DEP_LLD_FORCE_MULTIPLE` in `deps-windows.cmake` | `deps/CMakeLists.txt`, `deps/deps-windows.cmake` |

## 3. Added

### 3.1 New `deps/` projects

All are in `_dep_list` (`deps/CMakeLists.txt:462-496`). Consumers and link mode are in the [use map §3.2](dependency-use-map.md#32-the-six-dependency-projects-added-in-250).

| Project | Pin as declared | Integrity | Evidence | Slice |
|---|---|---|---|---|
| Assimp | `assimp/assimp` tag archive **v5.4.3** (`66dfbaee…`); **v5.3.1** (`a07666be…`) when CMake < 3.22 | SHA-256 | `deps/Assimp/Assimp.cmake:1-7`; included at `deps/CMakeLists.txt:416` | [B1](assimp-provenance-license-review.md) |
| ↳ Assimp `contrib/zlib` | Built on non-Apple platforms (`ASSIMP_BUILD_ZLIB=ON`, `:14-18`). The use map found the Linux app's zlib resolves to it (1.2.13) | inside the Assimp archive | [use map §3.4](dependency-use-map.md#34-system-libraries-duplicates-and-new-provenance-observations) | [B1](assimp-provenance-license-review.md) |
| libdatachannel | `paullouisageneau/libdatachannel.git` **tag v0.24.5**, `GIT_SHALLOW`, `GIT_SUBMODULES_RECURSE` (the comment names plog, usrsctp, libjuice) | **none**: Git tag, no commit or hash | `deps/DataChannel/DataChannel.cmake:11-22`; `deps/CMakeLists.txt:418` | [B2](libdatachannel-provenance-license-review.md) |
| FFmpeg (source) | `FFmpeg/FFmpeg` tag archive **n7.0.3** (`deedcabe…`), non-MSVC | SHA-256 | `deps/FFMPEG/FFMPEG.cmake:70-71`; configure flags `:73-97` (neither `--enable-gpl`, `--enable-version3` nor `--enable-nonfree` appears in the file) | [B3](ffmpeg-source-build-license-review.md) |
| FFmpeg (Windows) | Prebuilt **shared** zips from `Noisyfox/FFmpeg-Builds-Orca` release `autobuild-2026-09-18-16-50`, x64 and arm64 | SHA-256 | `deps/FFMPEG/FFMPEG.cmake:14-33` | **C1** |
| SLVS | `JacobStoren/SolveSpaceLib` **commit archive `4d870452…`** (`1c4bdde9…`); upstream CMakeLists replaced by `deps/SLVS/CMakeLists.txt.in` | SHA-256 | `deps/SLVS/SLVS.cmake:1-9`; only with `SLIC3R_CAD` (`deps/CMakeLists.txt:383-387`). The file's comment says "GPLv3, compatible with this fork's licence" — recorded as the file's claim, not checked | [B4](slvs-provenance-license-review.md) |
| CPython | `python.org` **Python-3.12.13.tar.xz** (`c08bc65a…`), all platforms | SHA-256 | `deps/python3/python3.cmake:4-8`, `:349-351` | [B5](cpython-pybind11-provenance-license-review.md) |
| ↳ CPython Windows `source-deps` | `python/cpython-source-deps` commit archives: bzip2-1.0.8, sqlite-3.49.1.0, xz-5.2.5, zlib-1.3.1 | SHA-256 | `deps/python3/python3.cmake:93-98`, `:113-122` | C3 |
| ↳ CPython Windows `bin-deps` | `python/cpython-bin-deps` commit archives: **libffi-3.4.4**, **openssl-bin-3.0.16.2** (prebuilt libraries) | SHA-256 | `deps/python3/python3.cmake:99-100` | **C3** |
| ↳ Windows host Python | nuget.org `pythonx86`/`pythonarm64` **3.13.16** `.nupkg`, build-time only, skipped if `DEP_PYTHON_HOST` is set | SHA-256 | `deps/python3/python3.cmake:11-46` | C3 |
| wxInspector | `Noisyfox/wxInspector` tag archive **v1.0.0** (`0ba16395…`) | SHA-256 | `deps/wxInspector/wxInspector.cmake:24-33`; `deps/CMakeLists.txt:460` | [B6](wxinspector-provenance-license-review.md) |

### 3.2 New vendored source (`deps_src/`)

| Component | What the tree holds | Evidence | Slice |
|---|---|---|---|
| pybind11 | 54 files: `LICENSE`, `README.rst`, `include/`. Header reports **3.0.1** (`PYBIND11_VERSION_MAJOR/MINOR/MICRO` = 3/0/1, final) | `deps_src/pybind11/include/pybind11/detail/common.h:20-28`; consumed via a minimal `pybind11::embed` target in the root `CMakeLists.txt:1041-1044` | [B5](cpython-pybind11-provenance-license-review.md) |

### 3.3 Binary pin outside `deps/`

| Item | Pin | Evidence | Slice |
|---|---|---|---|
| `uv` 0.11.21 | Release archives for six triples from `astral-sh/uv`, one SHA-256 each; downloaded at configure time unless `ORCA_BUNDLED_UV_EXECUTABLE` is set; installed into the app | root `CMakeLists.txt:128-141` (comment, version, hashes), download logic `:143-242`, URL at `:201`; install lines in [use map §3.4](dependency-use-map.md#34-system-libraries-duplicates-and-new-provenance-observations) | C2 |
| Flatpak manifest | `scripts/flatpak/com.orcaslicer.OrcaSlicer.yml` pins its own sources (31 `sha256` lines), including uv per the root `CMakeLists.txt:133-134` comment | not scanned: Flatpak is not a target platform in [0001](decisions/0001-supported-platforms.md) | none |

## 4. Removed

Removed components are not deleted from this repository's history. Their reviews stay as history.

| Component | v2.4.2 evidence | Existing review | Action |
|---|---|---|---|
| OpenCSG 1.4.2 | `deps/OpenCSG/OpenCSG.cmake:5-7`, included at 2.4.2 `deps/CMakeLists.txt:344` | none dedicated; rows in the [provenance audit](dependency-provenance-audit.md), [platform matrix](platform-dependency-matrix.md) | slice D1 moves the rows to a "removed in 2.5.0" section |
| GLEW (vendored under `deps/GLEW/glew`) | included at 2.4.2 `deps/CMakeLists.txt:341` | none dedicated; rows in the matrix and [vendored inventory](vendored-source-and-patch-inventory.md) | slice D1/D4 |
| FreeType 2.12.1 | `deps/FREETYPE/FREETYPE.cmake:14-15`, included at 2.4.2 `deps/CMakeLists.txt:397` | rows in the audit, matrix and [Windows binary inventory](windows-binary-provenance.md) (FreeType DLL copy) | slice D1/C4 |
| Legacy Clipper 6.x (`deps_src/clipper`) | 2.4.2 `deps_src/CMakeLists.txt:18` | [clipper-legacy-license-use-review.md](clipper-legacy-license-use-review.md) | **historical banner added in this change** |

## 5. Pin coverage check

`tools/check-archive-manifest-coverage.py` reads every git-tracked `*.cmake` and `CMakeLists.txt` in a checkout. It reports any SHA-256 literal or `GIT_REPOSITORY` on a non-comment line that the manifest does not account for, and any manifest entry whose hash or repository no longer occurs in the tree. It does not evaluate CMake, so it cannot tell whether a pin is reachable in a given configuration; it only proves that nothing declared is missing from the manifest.

| Run | Result |
|---|---|
| 2.5.0 tree `665552c1` + `audit/orcaslicer-v2.5.0-source-archives.json` | **45 SHA-256 literals, 4 Git repositories: 0 uncovered, 0 stale** (exit 0) |
| Baseline: v2.4.2 tree `8500fcdc` + `audit/orcaslicer-v2.4.2-source-archives.json` (unchanged) | 25 SHA-256 literals, 4 Git repositories: 5 uncovered, 1 stale (exit 1). All six are already-known gaps in how that manifest is written, not missing archives: NanoSVG's declared hash (the manifest records only the corrected digest, so the corrected digest also shows as stale); the wxWidgets and libpng Git pins (excluded only as text); and two `FetchContent` repositories in `deps_src/mcut/CMakeLists.txt` (below). Every other v2.4.2 hash is covered |

The 2.5.0 manifest records these cases in machine-readable form: `declared_sha256` on the NanoSVG artifact, and `sha256` lists and `git_repository` fields on the excluded pins. The 2.4.2 manifest is left unchanged as the record of that audit.

**Found by the check, present in both versions:** `deps_src/mcut/CMakeLists.txt` declares `FetchContent` Git downloads of libigl v2.3.0 and Eigen inside `if(MCUT_BUILD_TESTS OR MCUT_BUILD_TUTORIALS)` (block from line 218). Those options default ON only when MCUT is the top-level project (`:112-118`). OrcaSlicer adds it with `add_subdirectory(mcut)` (`deps_src/CMakeLists.txt:27`), so by the file's logic they do not run in the OrcaSlicer build. Recorded as excluded pins `mcut-tests-libigl` and `mcut-tests-eigen`, not verified by a configure run.

**Also recorded:** `deps/NanoSVG/NanoSVG.cmake` is not included by `deps/CMakeLists.txt` in v2.4.2 or 2.5.0, so that pin is never built; the application uses `deps_src/nanosvg`. 2.5.0 still declares the pre-rename URL and digest that [archive-verification.md](archive-verification.md) found to redirect.

## 6. What this inventory does not cover

- Reachability per platform: which pins a Windows or macOS configure actually uses. The Linux x86_64 answer is in the [use map](dependency-use-map.md).
- Contents of any archive: licenses, nested third-party code and patches inside an archive are slices B–D.
- Tag-to-commit resolution for libdatachannel (B2) and whether wxWidgets `b44c39c` matches its former tag (D2).
- Any keep/remove or optionalize decision (goals [Q17](goals.md), use-map O7/O8).
