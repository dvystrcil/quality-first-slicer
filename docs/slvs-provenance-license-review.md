# SLVS (SolveSpace solver) provenance and license review (OrcaSlicer 2.5.0)

**Status:** Source and license-file review. Not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off. The keep/optionalize question is [goals Q17](goals.md) and is not answered here.
**Slice:** B4 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (build files identical to upstream v2.5.0 `40ecc66f`)
**Method:** read `deps/SLVS/SLVS.cmake` and `deps/SLVS/CMakeLists.txt.in`; extracted the hash-verified archive; read every file's header; GitHub API for repository and commit metadata.
**Reviewed:** 2026-11-09

## 1. Source and pin

| | |
|---|---|
| URL | `https://github.com/JacobStoren/SolveSpaceLib/archive/4d8704523e4bf212fadf5189f92484244f670fea.zip` (`deps/SLVS/SLVS.cmake:6`) |
| SHA-256 (declared and verified) | `1c4bdde9c3c6ef20ea4b50b73601de56769f2eb131b36927d7c6489f102e6c30` (`:7`) |
| Commit | `4d870452…`, author Jacob Støren, 2018-10-16, message "Small adjustments from ResInsight", signature: unsigned. It is the HEAD of `master` (23 commits); the last push was 2018-10-16 |
| Repository | `JacobStoren/SolveSpaceLib`: a user account, **not** a GitHub fork (no parent), not archived; GitHub license detection: `GPL-3.0` |
| Built only with | `SLIC3R_CAD=ON`, the default (`deps/CMakeLists.txt:383-387`) |

The upstream `CMakeLists.txt` is replaced at patch time by OrcaSlicer's own `deps/SLVS/CMakeLists.txt.in` (`SLVS.cmake:8`), which compiles eight files (`constrainteq.cpp`, `entity.cpp`, `expr.cpp`, `system.cpp`, `util.cpp`, `platform/unixutil.cpp`, `lib.cpp`, `SolveSpaceSystem.cpp`) with `-DLIBRARY`, and installs `slvs.h` and `SolveSpaceSystem.h`. No source file is patched. The in-tree comment says the sources are "taken verbatim".

## 2. Lineage, as the files describe it

- `README.md`: "An insolated version of the geometric constraint solver from SolveSpace: libslvs. See http://solvespace.com and https://github.com/solvespace/solvespace … This repository only contains the neccessary code."
- Which `solvespace/solvespace` revision the files were taken from is **not recorded** in the repository. The commit message points to ResInsight, a separate project, as the source of the last adjustments.
- This review did not compare the files with any `solvespace/solvespace` revision.

## 3. License evidence

| File(s) | What it says |
|---|---|
| `LICENSE` and `libslvs/LICENSE` | Byte-identical; the full GNU General Public License **version 3** text |
| `README.md` § License | "SolveSpace and thus SolveSpaceLib is distributed under the terms of the GPL3 license." |
| Solver sources (`constrainteq.cpp`, `entity.cpp`, `expr.cpp`, `system.cpp`, `util.cpp`, `lib.cpp`, `solvespace.h`, …) | "Copyright 2008-2013 Jonathan Westhues." No license or version statement in the header |
| `include/slvs.h` | "Copyright 2009-2013 Jonathan Westhues." |
| `platform/unixutil.cpp` | Westhues, plus "Copyright 2013 Daniel Richard G." |
| `SolveSpaceSystem.cpp`, `include/SolveSpaceSystem.h` | **No copyright or license notice.** These two files are compiled and installed |

**The in-tree claim.** `deps/SLVS/SLVS.cmake:4` says "GPLv3, compatible with this fork's licence." The license files support the "GPLv3" part. Whether the files permit "version 3 or any later version" is not stated in any header, and only the bare GPL-3.0 text is present. Compatibility with this project's license is a legal question and is recorded as a claim, not checked.

## 4. Open questions

1. Authorship and license of `SolveSpaceSystem.{h,cpp}`, which carry no notice. The commit history would show who added them.
2. The source revision in `solvespace/solvespace` and the diff from it.
3. GPL-3.0-only versus "or later" is not stated in the source headers.
4. Notice staging: neither `LICENSE` file is installed by `CMakeLists.txt.in`.

## 5. Approval

**Not approved.** This records what the files say. A maintainer sign-off, and the Q17 decision on the CAD tab, are still needed.
