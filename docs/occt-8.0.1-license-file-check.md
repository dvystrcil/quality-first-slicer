# OCCT 8.0.1 license-file check (OrcaSlicer 2.5.0)

**Status:** License-file and source-header check of the Open CASCADE Technology (OCCT) archive that OrcaSlicer 2.5.0 builds. Not a full OCCT review and not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off.
**Slice:** D3 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (build files identical to upstream v2.5.0 `40ecc66f`)
**Method:** downloaded `V8_0_1.zip` into an empty scratch directory and re-hashed it. Listed it and read its license files and the first 6 KB of every C/C++ file under `src/` with `python3 -I` (nothing extracted to disk, built or run). Compared the license files with OCCT `V7_6_0` (the v2.4.2 pin) by Git blob ID, using the GitHub API.
**Reviewed:** 2026-11-19

## 1. Pin and integrity

| Item | Value | Evidence |
|---|---|---|
| Declared archive | `https://github.com/Open-Cascade-SAS/OCCT/archive/refs/tags/V8_0_1.zip` | `deps/OCCT/OCCT.cmake:33` |
| Declared SHA-256 | `7c033d917ee8f040c0512d289dcc5f02c148889d5bac17c3e25639accb44f0da` | `:34` |
| Download (64,815,440 bytes) | **PASS**, same hash. Also PASS in slice A ([archive-verification.md](archive-verification.md#250-verification-result)) | re-hashed for this review |
| Tag `V8_0_1` | annotated tag `c5605924` → commit `b8f597c677811d1f9f4d8a97f5ae2825c0353a42` | GitHub API |
| Local patch | `0001-BRepMesh-seam-pcurve-at-edge-parameter.patch`, two hunks in `src/ModelingAlgorithms/TKMesh/BRepMesh/BRepMesh_ModelPreProcessor.cxx`: the seam pcurve is evaluated at the edge's first parameter instead of `FirstParameter()`. The comment at `:35-36` cites Open-Cascade-SAS/OCCT#572 | `:37`. The file has no license header of its own. It modifies an LGPL-2.1 OCCT file |
| Modules | ModelingAlgorithms = `${SLIC3R_CAD}` (default ON); ApplicationFramework, Draw, FoundationClasses, ModelingData, Visualization `OFF`; DataExchange default. `USE_FREETYPE/TK/TBB/FFMPEG/VTK=OFF` | `:39-61`. The comment at `:14-22` says module flags are all-or-nothing and that DataExchange pulls in the other module toolkits anyway |
| Link mode | Shared on Windows, static elsewhere | `:8-12` |
| Toolkits the app links | 23 toolkits, including `TKGeomBase`, plus `TKFillet TKOffset TKBool` when `SLIC3R_CAD` is ON. On Windows exactly these DLLs are copied next to the executable | `src/libslic3r/CMakeLists.txt:693-741`; root `CMakeLists.txt:1117-1160` |

## 2. License files

| File (archive root) | Bytes | Git blob | Same as `V7_6_0`? |
|---|---:|---|---|
| `LICENSE_LGPL_21.txt` (GNU LGPL v2.1) | 26,434 | `732811e4` | **identical** |
| `OCCT_LGPL_EXCEPTION.txt` ("Open CASCADE exception (version 1.0) to GNU LGPL version 2.1") | 663 | `263d14ef` | **identical** |
| `dox/license.md` (documentation copy) | 27,976 | `c120e7f3` | one-character change (a backtick replaced by an apostrophe in the LGPL sample text) |

`README.md` (`:6-10`) says OCCT is under LGPL 2.1 with the exception in `OCCT_LGPL_EXCEPTION.txt`, or alternatively under a commercial license. The exception lets object code that incorporates material from OCCT header files be distributed "under terms of your choice", provided supporting documentation gives "prominent notice" that the code uses OCCT. Recorded as text, not interpreted.

**So the license texts did not change between 7.6.0 and 8.0.1.**

**Install.** OCCT's `CMakeLists.txt:964-971` installs both files into `INSTALL_DIR_DOC`, which is `share/doc/opencascade` for the Unix layout (`:933-945`). OrcaSlicer sets `-DINSTALL_DIR_LAYOUT=Unix` (`deps/OCCT/OCCT.cmake:44`), so the files land in the dependency prefix. In OrcaSlicer 2.5.0, `git grep` for `OCCT_LGPL`, `LICENSE_LGPL_21` and `share/doc` across the root and `src/CMakeLists.txt`, `deps/` and `src/dev-utils` found **no step that copies them into a shipped app**, although Windows ships the OCCT DLLs. No release artifact was inspected.

## 3. Source-file headers

14,699 of the 14,718 C/C++ files under `src/` carry the standard LGPL 2.1 header that names `OCCT_LGPL_EXCEPTION.txt`. The other 19:

| Files | Header | Toolkit | In the build? |
|---|---|---|---|
| **`GeomConvert_CurveToAnaCurve.{cxx,hxx}`, `GeomConvert_SurfToAnaSurf.{cxx,hxx}`, `Geom2dConvert_ApproxArcsSegments.{cxx,hxx}`, `Geom2dConvert_PPoint.{cxx,hxx}`** (8 files) | **"This file is part of commercial software by OPEN CASCADE SAS, furnished in accordance with the terms and conditions of the contract … This file or any part thereof may not be provided or otherwise made available to any third party."** | `TKGeomBase` | **yes**: `TKGeomBase` is in the app's toolkit list and ships as a DLL on Windows |
| `BRepMesh/delabella.{cpp,pxx}` | MIT, "Copyright (C) 2018 GUMIX - Marcin Sokalski" | `TKMesh` | yes (`TKMesh` is linked) |
| `Standard/Standard_Strtod.cxx` | David M. Gay / Lucent Technologies permissive notice | `TKernel` | yes |
| `FlexLexer/FlexLexer.h` | Regents of the University of California (flex) | `TKernel` | yes |
| `StepFile/lex.step.cxx` | flex-generated | `TKDESTEP` | yes |
| `ExprIntrp/ExprIntrp.tab.{c,h}`, `lex.ExprIntrp.c` | Bison 3.7.4 / flex-generated (Bison's skeleton exception text not re-read) | `TKExpress` | built with `SLIC3R_CAD` (the OCCT.cmake comment says nothing references it) |
| `OpenGl_HaltonSampler.hxx`, `OpenGl_glext.h`, `OpenGl_khrplatform.h` | MIT-style (Gruenschloss; Khronos) | `TKOpenGl` | not in the app's toolkit list (whether it is built was not checked) |

**The eight "commercial software" headers are the main finding.** They contradict `LICENSE_LGPL_21.txt` as written. Upstream issue [Open-Cascade-SAS/OCCT#1564](https://github.com/Open-Cascade-SAS/OCCT/issues/1564), opened 2026-09-27, reports the same eight files in `V8_0_1` and asks OCCT to replace the headers or confirm the files are LGPL. It was **open with no reply** when checked on 2026-11-19. The issue says the files arrived in commit `b47b075a` (OCCT 7.7, 2022). That attribution was not checked here. What was checked: none of the files exists at `V7_6_0` (the GitHub API returns 404 for their 7.6 paths), so **v2.4.2's OCCT did not contain them and 2.5.0's does**.

The app does not call these classes directly (`git grep` on `src/` finds none of their names). Whether other OCCT toolkits reference them was not traced. On Linux and macOS, OCCT links statically, so whether their object code ends up in the binary depends on those references. On Windows the whole `TKGeomBase.dll` ships.

## 4. Open questions

1. The eight `TKGeomBase` files (§3): what is their license? Waiting on upstream #1564. The maintainer should decide what to do meanwhile. STEP import, which [0007](decisions/0007-remove-cad-tab.md) keeps, still links `TKGeomBase`; tracked as a release blocker in [#62](https://github.com/dvystrcil/quality-first-slicer/issues/62).
2. OCCT's LGPL text and exception notice are not staged into any app package by the build files read here. The exception's "prominent notice" condition is a packaging question.
3. The MIT (delabella) and Gay/Lucent notices in compiled toolkits will need third-party notice entries.
4. The ModelingAlgorithms module (`SLIC3R_CAD`) builds `TKExpress`, `TKFeat`, `TKHelix` and `TKXMesh`, which nothing references. Keeping or optionalizing the Design/CAD tab is a product decision (goals [Q17](goals.md)), not made here. Later decided: the tab is removed (`SLIC3R_CAD=OFF`, [0007](decisions/0007-remove-cad-tab.md)).

## 5. Approval

**Not approved.** This records what the archive, its license files and the build files say. A maintainer sign-off is still needed.
