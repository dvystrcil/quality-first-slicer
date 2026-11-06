# Vendored source license-header review — selected deps_src components

**Status:** Targeted source-header review; not a complete license/provenance audit  
**OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (v2.4.2)  
**Method:** Inspected the checked-in source headers, selected CMake files, component READMEs, and application include/link references at the fixed revision. No local build, complete upstream diff, binary review, or legal review.

## 1. Executive findings

This review resolves license evidence for a first group of components whose license-named files were not found in the initial tree scan. Several declare their license directly in source headers:

- Shiny: MIT.
- ADMesh: GNU GPL version 2 or, at the recipient's option, any later version (GPL-2.0-or-later); all seven target source/header files preserve the notice, but the vendored subset omits upstream `COPYING` and the referenced `AUTHORS` file. No ADMesh-specific linking exception was found; see [ADMesh GPL notice review](admesh-gpl-notice-review.md).
- Clipper and Clipper2: Boost Software License 1.0.
- fast_float: MIT.
- GLU tessellator subset: SGI Free Software License B, version 2.0.
- NanoSVG: its own permissive three-condition license; source headers also attribute upstream-derived code.
- nlohmann/json: MIT.
- QOI: MIT.
- semver: MIT.
- stb_dxt: BSD 2-Clause.

**HIDAPI remains unresolved.** Its checked-in headers identify three alternative license elections (GPLv3, BSD-style, or the original HIDAPI license), while the vendored subset omits the selection guide and all three license texts. The upstream source distribution confirms the three choices are at the user's discretion, but neither the source headers nor the downstream CMake build record which choice OrcaSlicer made. The source identity, omitted documents, and active platform-specific GUI integration are documented in [HIDAPI provenance and license-election review](hidapi-provenance-license-election.md).

This review also found two provenance issues:
- The `hints` utility is not an external third-party library: Git history traces it to the initial BambuStudio 1.0.10 source import. Its file has no individual copyright/license header, so file-level attribution and the precise relationship to the repository-level AGPLv3 notice remain to be documented.

## 2. Component findings

| Component | Source-level license evidence | Use evidence / status |
|---|---|---|
| Shiny | `Shiny.h` embeds the MIT license and copyright notice for Aidin Abedi. | `GCodeReader.cpp` includes `Shiny/Shiny.h`; active source use. |
| ADMesh | All seven files in the static target preserve the GPL-2-or-later notice; full upstream `COPYING` and referenced `AUTHORS` are absent from the vendored subset. | Active use is confirmed: linked into `libslic3r` and `libslic3r_cgal`; `TriangleMesh.cpp` calls ADMesh APIs. No component-specific linking exception found. See [ADMesh GPL notice review](admesh-gpl-notice-review.md). |
| Clipper (legacy) | `clipper.hpp` identifies Boost Software License 1.0. | CMake comments out `clipper.cpp`/`clipper.hpp` in this target but builds `clipper_z.cpp`; inspect consumers and actual link use before treating the full legacy source set as compiled. |
| Clipper2 | Checked-in implementation/header notices identify Boost Software License 1.0. | `Clipper2` is linked by `libslic3r`. Both local CMake (`project(Clipper2 VERSION 1.5.2)`) and `clipper.version.h` (`CLIPPER2_VERSION = "1.5.2"`) agree with upstream Clipper2 release commit `6901921c4be75126d1de60bfd24bd86a61319fd0`; the previously reported 2.0.1 discrepancy was incorrect. |
| fast_float | `fast_float.h` includes the MIT permission and disclaimer text. | README identifies source distribution as fast_float 2.0.0, commit `fe1ce58`; application files include its header. |
| GLU tessellator subset | Implementation files such as `src/tess.c` and `src/mesh.c` embed SGI Free Software License B (Version 2.0, Sept. 18, 2008). | `glu-libtess` is linked by `libslic3r`; `Tesselate.cpp` includes its API. README identifies Mesa GLU origin commit `0bf42e41c8b63fc2488dd8d41f696310b5a5a6a7`. |
| HIDAPI | Header says GPLv3, BSD-style, or original HIDAPI license are available, with texts in `LICENSE.txt`, `LICENSE-gpl3.txt`, `LICENSE-bsd.txt`, and `LICENSE-orig.txt`. Those files are absent from this vendored subset. | README identifies hidapi 0.9.0, upstream commit `7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f`; the vendored `hidapi.h` has the same Git blob SHA as the file at that upstream commit. Platform source is selected by CMake. The upstream release explicitly offers three license choices, but the OrcaSlicer subset omits the license texts and contains no selection record. Exact license selection and preservation of required terms remain unresolved. |
| NanoSVG | `nanosvg.h` and `nanosvgrast.h` include the project's custom permissive three-condition grant, including origin/alteration/notice requirements. Headers also acknowledge Anti-Grain Geometry and stb_truetype-derived portions. | Application includes NanoSVG headers. README identifies SoftFever fork, but the exact upstream commit/version is not recorded there. Attribution and derivative-code provenance need further review. |
| nlohmann/json | `json.hpp` embeds SPDX MIT and full MIT permission/disclaimer text. | Vendored header-only source; exact upstream version/commit not established by this review. |
| QOI | `qoi.h` embeds the MIT license and copyright notice. | `qoi` target is linked by `libslic3r`; `Thumbnails.cpp` includes QOI. `qoilib.c` notes a PrusaSlicer-specific integration change. |
| semver | `semver.c` identifies Tomas Aparicio and says MIT licensed. | `semver` target is linked by `libslic3r`; application has semver integration. |
| stb_dxt | `stb_dxt.h` embeds BSD 2-Clause terms and disclaimer, but no concrete copyright-holder/year line appears in the inspected text. | Exact RygsDXTc mirror snapshot pinned; Orca's header is a close derivative with a small wrapper delta and is byte-identical to the inspected BambuStudio header snapshot. Copyright notice/holder remains unresolved; see [stb_dxt provenance review](stb-dxt-provenance-review.md). |
| hints | No file-level license or copyright declaration in `HintsToPot.cpp`. | Internal translation-template utility, not a third-party library. Git history traces it to the BambuStudio 1.0.10 source import; subsequent changes are recorded under Zhaofeng Li. See [hints utility provenance review](hints-utility-provenance.md). Exact file-level copyright attribution remains unconfirmed. |

## 3. HIDAPI is a specific unresolved blocker

The vendored `hidapi/include/hidapi.h` has the same Git blob SHA (`1819f8de0912f225373f0390dbe582434d9c9dac`) as the canonical `libusb/hidapi` header at commit `7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f`. The OrcaSlicer README identifies the vendored source as hidapi 0.9.0 at that abbreviated commit.

The pinned upstream commit contains all four referenced files: `LICENSE.txt`, `LICENSE-gpl3.txt`, `LICENSE-bsd.txt`, and `LICENSE-orig.txt`. The selection guide says the user chooses among three alternatives; the upstream `Makefile.am` includes the guide and all three license texts in `dist_doc_DATA`. The BSD text identifies Alan Ott / Signal 11 Software (2010), the original license requires retaining the source-file copyright notice, and the GPLv3 text includes section 13's express permission for combination with an AGPLv3-covered work, subject to that section's terms. These facts describe the alternatives, not OrcaSlicer's election.

OrcaSlicer's vendored subset omits all four license files. Its CMake file creates a static `hidapi` target and selects `win/hid.c`, `mac/hid.c`, or `linux/hid.c` by platform. The GUI target links HIDAPI, and `Mouse3DController.cpp` consumes it. No license-selection metadata or explicit election appears in the CMake file. The source origin and active use are verified, but the selected license and omitted notice texts remain unresolved.

Required evidence:

1. Determine which alternative was elected using contemporaneous release/source-distribution metadata or written maintainer/rights-holder confirmation—not guesswork.
2. Confirm that the election applies to the complete platform source set.
3. Restore/preserve the selected license text and required notices in source distributions and release third-party notices.

Until resolved, mark HIDAPI licensing as unknown rather than assigning a convenient permissive license. The complete fixed-revision evidence and follow-up procedure are recorded in [HIDAPI provenance and license-election review](hidapi-provenance-license-election.md).

## 4. Version and provenance follow-up

- **NanoSVG:** its SoftFever source commit and both header comparisons are documented in [NanoSVG and nlohmann provenance](nanosvg-nlohmann-provenance.md). Embedded Anti-Grain Geometry, stb_truetype-derived rasterization, and FLTK modification attributions are assessed in [NanoSVG embedded-code attribution review](nanosvg-embedded-attribution-review.md); copied-code boundaries and license elections remain unresolved. The parser's local zero-initialization change is not visibly marked at its source location in the reviewed revision, leaving a concrete NanoSVG altered-source condition to address.
- **nlohmann/json:** all 41 vendored files match upstream release 3.10.4 by Git blob SHA; see [NanoSVG and nlohmann provenance](nanosvg-nlohmann-provenance.md).
- **stb_dxt:** the Cyan4973/RygsDXTc source snapshot is pinned and the small Orca wrapper delta is documented. The BSD-2-Clause text is present, but the concrete copyright notice/holder/year remains unresolved; see [stb_dxt provenance review](stb-dxt-provenance-review.md).
- **hints:** source origin is traced to the BambuStudio 1.0.10 import, but individual copyright attribution and the exact file-level licensing basis remain to be confirmed.
- **ADMesh:** all seven target files carry consistent GPL-2-or-later notices and active API use is confirmed. The vendored subset omits upstream `COPYING` and the referenced `AUTHORS` file; no ADMesh-specific linking exception was found. Restore/verify distribution notices and trace the local C++/Eigen delta; see [ADMesh GPL notice review](admesh-gpl-notice-review.md).
- **HIDAPI:** resolve the multi-license selection and restore the applicable notice text.

## 5. Fixed-revision evidence

OrcaSlicer source links below are pinned to commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`.

| Evidence | Source |
|---|---|
| Shiny MIT header | [`deps_src/Shiny/Shiny.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/Shiny/Shiny.h) |
| ADMesh GPL notice | [`deps_src/admesh/stl.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/admesh/stl.h) |
| Clipper license | [`deps_src/clipper/clipper.hpp`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/clipper/clipper.hpp) |
| Clipper2 version declarations | [`deps_src/clipper2/CMakeLists.txt`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/clipper2/CMakeLists.txt), [`clipper.version.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/clipper2/Clipper2Lib/include/clipper2/clipper.version.h), upstream release [`1.5.2`](https://github.com/AngusJohnson/Clipper2/commit/6901921c4be75126d1de60bfd24bd86a61319fd0) |
| fast_float MIT notice and version README | [`fast_float.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/fast_float/fast_float.h), [`README.md`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/fast_float/README.md) |
| GLU SGI license and source origin | [`src/tess.c`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/glu-libtess/src/tess.c), [`README`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/glu-libtess/README) |
| HIDAPI vendored header and version | [`hidapi.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hidapi/include/hidapi.h), [`README.md`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hidapi/README.md); canonical upstream [`LICENSE.txt`](https://github.com/libusb/hidapi/blob/7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f/LICENSE.txt), [`LICENSE-bsd.txt`](https://github.com/libusb/hidapi/blob/7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f/LICENSE-bsd.txt), [`LICENSE-gpl3.txt`](https://github.com/libusb/hidapi/blob/7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f/LICENSE-gpl3.txt), [`LICENSE-orig.txt`](https://github.com/libusb/hidapi/blob/7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f/LICENSE-orig.txt), and upstream [`Makefile.am`](https://github.com/libusb/hidapi/blob/7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f/Makefile.am) |
| NanoSVG custom license and upstream comparison | [`nanosvg.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/nanosvg/nanosvg.h), [`nanosvgrast.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/nanosvg/nanosvgrast.h); see [NanoSVG and nlohmann provenance](nanosvg-nlohmann-provenance.md) |
| nlohmann MIT/SPDX notice and exact source match | [`json.hpp`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/nlohmann/json.hpp); see [NanoSVG and nlohmann provenance](nanosvg-nlohmann-provenance.md) |
| QOI MIT notice | [`qoi.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/qoi/qoi.h) |
| semver MIT notice | [`semver.c`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/semver/semver.c) |
| stb_dxt BSD-2-Clause notice | [`stb_dxt.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/stb_dxt/stb_dxt.h) |
| hints utility source and history | [`HintsToPot.cpp`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hints/HintsToPot.cpp), initial BambuStudio source import [`1555904`](https://github.com/OrcaSlicer/OrcaSlicer/commit/1555904beffef41195003f184dec0af46b308eee), folder move [`883607e`](https://github.com/OrcaSlicer/OrcaSlicer/commit/883607e1d4a0b2bb719f2f4bcd9fd72f8c2174fa); see [hints utility provenance review](hints-utility-provenance.md) |

## 6. Limitations and conclusion

This is a targeted source-header review, not a complete license scan. It does not resolve all 26 third-party components and nested dependencies, all exact upstream commits, source modifications, platform build selection, or distribution obligations. The license text found in a source header is evidence for that file/component, but does not automatically settle the status of embedded third-party code or every file in a directory.

The main newly identified high-priority unresolved item is HIDAPI's missing selected license text. ADMesh's GPL-2.0-or-later notice is also material and must be considered alongside the project's intended AGPLv3 distribution. No legal compatibility conclusion is made.
