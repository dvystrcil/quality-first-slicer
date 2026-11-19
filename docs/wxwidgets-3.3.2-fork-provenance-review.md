# wxWidgets 3.3.2 fork provenance and license review

**Status:** Updated for OrcaSlicer 2.5.0 in §0 (slice D2 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)). 2.5.0 pins a commit and names its three submodules, so the source pin and submodule questions are resolved for 2.5.0. Release notice packaging is still open. Sections 1–6 below are the v2.4.2 review, kept as history. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off.  
**OrcaSlicer baseline:** 2.5.0: fork `baseline-2.5.0` `665552c1` (build files identical to upstream v2.5.0 `40ecc66f`). §1–6: `v2.4.2`, commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**Build declaration:** `deps/wxWidgets/wxWidgets.cmake`  
**Method:** GitHub API inspection of the fixed OrcaSlicer CMake declaration, the fork branch/ref, upstream wxWidgets history, selected fork commits, source headers, license files, and the recursive Git tree. No local checkout/build, submodule initialization, archive hash, binary package, or legal review.

## 0. OrcaSlicer 2.5.0 update (slice D2, reviewed 2026-11-19)

**Method:** read `deps/wxWidgets/wxWidgets.cmake` at `665552c1`. Branch, tag, compare, `.gitmodules`, gitlink and file contents came from the GitHub API for `OrcaSlicer/Orca-deps-wxWidgets`, `wxWidgets/wxWidgets` and the three `wxWidgets/*` submodule repositories. Nothing was cloned, built or run.

### 0.1 The 2.5.0 declaration

`deps/wxWidgets/wxWidgets.cmake:32-37`:

| Field | v2.4.2 | 2.5.0 |
|---|---|---|
| `GIT_REPOSITORY` | `https://github.com/SoftFever/Orca-deps-wxWidgets` (redirects to the OrcaSlicer org) | `https://github.com/OrcaSlicer/Orca-deps-wxWidgets` |
| `GIT_TAG` | `v3.3.2` (a **branch** name, §1) | **`b44c39c100975a0ac0e46f937aa3f3eae5e18631`** (a commit) |
| `GIT_SHALLOW` | `ON` | `ON` |
| `GIT_SUBMODULES` | not set (all 12 submodules) | `3rdparty/catch 3rdparty/pcre 3rdparty/libwebp` |

2.5.0 fixes the source to one commit, which addresses the main v2.4.2 finding (a mutable branch). There is still no archive hash: integrity rests on Git's commit ID. The historical v2.4.2 build commit is still unknown (§5 item 1). That is a v2.4.2 question and does not affect 2.5.0.

### 0.2 What `b44c39c` is

| Check | Result |
|---|---|
| Is `b44c39c` on the fork? | Yes. It is still the tip of branch `v3.3.2` (`branches/v3.3.2` → `b44c39c1…`); compare `b44c39c…v3.3.2` = identical. It is the same commit §1 recorded as the tip on 2026-11-06. Commit date 2026-10-29, "Don't send unsupported Wayland release requests (#8)" |
| Is it upstream wxWidgets v3.3.2? | **No.** Upstream `wxWidgets/wxWidgets` compare `v3.3.2...b44c39c` = **ahead 4, behind 0**, changing the same four files as in §2 (`build/cmake/wxWidgetsConfig.cmake.in`, `src/gtk/wayland.cpp`, `src/msw/webview_edge.cpp`, `src/osx/cocoa/colour.mm`). So the delta in §2 is exactly what 2.5.0 builds |
| Fork tags | The fork has tags `orca-3.1.5`, `orca-3.1.5-1` and **`orca-3.3.2`**. `orca-3.3.2` points at `db1005db` (upstream v3.3.2), **not** at `b44c39c`. No tag names the commit 2.5.0 builds |

The license evidence in §3 was read at this same commit, so it applies to 2.5.0 unchanged. The fork's `build/cmake/install.cmake` installs no license file (only its own header comment says "wxWindows licence").

### 0.3 The three submodules

The gitlinks at `b44c39c` are **the same three commits as upstream wxWidgets `v3.3.2`** (contents API on both refs). The fork changes no submodule pin.

| Path | Repository (`.gitmodules`, branch `wx`) | Gitlink at `b44c39c` | Version and upstream lineage | License files at that commit | Compiled by the 2.5.0 build? |
|---|---|---|---|---|---|
| `3rdparty/pcre` | `wxWidgets/pcre` | `4f76619e6f20de93f77b5ef6213bf54e0399d166` (2025-12-03, "Update config files") | **PCRE2 10.47** (`configure.ac:11-14`, dated 2025-10-21). `README-WX.md` says it was cloned from `rurban/pcre`, a Git clone of the official PCRE2 repository. The upstream tag `pcre2-10.47` commit `f454e231` is an ancestor (behind 0). 30 paths differ from that tag: autotools files, `README-WX.md`, the added `src/wx/{config.h,pcre2.h}` and `src/pcre2_chartables.c`, the removed `deps/sljit`, and **six `src/pcre2_*.c` sources** (`compile`, `compile_class`, `convert`, `dfa_match`, `script_run`, `study`). The six source diffs were **not reviewed** | `LICENCE.md`: "SPDX-License-Identifier: BSD-3-Clause WITH PCRE2-exception"; library "Copyright (c) 1997-2007 University of Cambridge, Copyright (c) 2007-2024 Philip Hazel"; the JIT compiler is separately 2-clause BSD. Also `COPYING`, `AUTHORS.md` | **Yes.** `-DwxUSE_REGEX=builtin` (`wxWidgets.cmake:55`). `build/cmake/lib/regex.cmake:21-28` builds `wxregex` from `3rdparty/pcre/src/pcre2_*.c` |
| `3rdparty/libwebp` | `wxWidgets/libwebp` | `e83df81cc965a47c1ca7cc968d1ed99717c55ab7` (2025-12-05, "Increase MSVC version for AVX2") | **libwebp 1.6.0** (`NEWS`). Upstream `webmproject/libwebp` compare `v1.6.0...e83df81` = **ahead 5, behind 0**, changing `cmake/deps.cmake`, `src/dsp/cpu.h` and `wx/src/webp/config.h` (CMake minimum, an option to disable SIMD checks, the MSVC AVX2 version check) | `COPYING`: BSD-style, "Copyright (c) 2010, Google Inc."; `PATENTS`: "Additional IP Rights Grant (Patents)"; `AUTHORS` | **Yes.** `-DwxUSE_LIBWEBP=builtin` (`:64`). `build/cmake/lib/webp.cmake` builds it from `3rdparty/libwebp` with the tools off |
| `3rdparty/catch` | `wxWidgets/Catch` | `3a4a6a657d295d003e16bcdba45c2832e24b9dec` (2025-01-23) | **Catch2 2.13.10** (`CMakeLists.txt:19`). Upstream `catchorg/Catch2` compare `v2.13.10...3a4a6a6` = ahead 29, behind 0 (not reviewed) | `LICENSE.txt`: Boost Software License 1.0 | **Not by the build files read here.** It is test-only: `wxBUILD_TESTS` defaults to `OFF` (`build/cmake/options.cmake:15`) and `main.cmake:30-32` adds the tests only when it is set. OrcaSlicer does not set it. It is fetched, not compiled |

The other nine submodules (`src/zlib`, `src/png`, `src/expat`, `src/tiff`, `src/jpeg`, `3rdparty/nanosvg`, `src/stc/scintilla`, `src/stc/lexilla`, `3rdparty/lunasvg`) are not initialized in 2.5.0, so their source is not fetched. The matching options take the system or Orca copy or are off: `wxUSE_LIBPNG/ZLIB/LIBJPEG/EXPAT=sys`, `wxUSE_LIBTIFF=OFF`, `wxUSE_NANOSVG=OFF`, `wxUSE_STC=OFF` (`:58-66`). `wxUSE_LUNASVG` defaults to `OFF` (`build/cmake/options.cmake:150`) and OrcaSlicer does not set it.

### 0.4 What this changes and what is still open

| Item from §5 | Status for 2.5.0 |
|---|---|
| 1. Historical commit of each release | still unknown for v2.4.2; for 2.5.0 the commit is in the build file |
| 2. Replace the branch ref with an immutable commit | **done upstream** in 2.5.0 (commit, no archive hash) |
| 3. Which submodules are initialized and used | **resolved from the build files**: three are fetched, and pcre and libwebp are compiled into wx (§0.3). Not confirmed against a build log |
| 4. How notices reach the app | **open**, and now includes the PCRE2 (BSD-3-Clause with the PCRE2 exception) and libwebp (BSD + `PATENTS`) notices. Neither wx's install rules nor OrcaSlicer's copy them |
| 5. Are the four fork changes in the built source? | yes for 2.5.0 (§0.2) |

New: the six PCRE2 source files that differ from the 10.47 tag are not reviewed, and neither is the Catch2 delta (which is not compiled).

## 1. What OrcaSlicer asks the build to fetch

At the pinned OrcaSlicer revision, `deps/wxWidgets/wxWidgets.cmake` declares:

- Repository URL: `https://github.com/SoftFever/Orca-deps-wxWidgets`
- `GIT_TAG v3.3.2`
- `GIT_SHALLOW ON`
- No immutable commit SHA or source archive checksum.

The former `SoftFever/Orca-deps-wxWidgets` URL now resolves to `OrcaSlicer/Orca-deps-wxWidgets`. The name `v3.3.2` is a **branch**, not a tag, in the resolved repository: `refs/heads/v3.3.2` exists, while `refs/tags/v3.3.2` returned 404 in this review. Consequently the build declaration follows a mutable branch name, not an immutable release tag.

The current branch tip observed on 2026-11-06 is:

- `b44c39c100975a0ac0e46f937aa3f3eae5e18631`
- Subject: `Don't send unsupported Wayland release requests (#8)`
- Branch ref: `refs/heads/v3.3.2`

This identifies the current branch state, **not** the exact commit that an earlier v2.4.2 build fetched. The CMake declaration alone cannot reconstruct that historical checkout.

## 2. Upstream base and fork delta

The fork branch descends directly from upstream wxWidgets commit `db1005db3dea2c37a46fb455a9a02e37aa360751`. GitHub's compare endpoint reports that this commit is identical to upstream `wxWidgets/wxWidgets` ref `v3.3.2`. The fork branch is four commits ahead and zero behind that upstream base.

The four commits in the current branch history are:

| Commit | Recorded change | Net source effect |
|---|---|---|
| `4a671ff5ce797f99cf535b5ea3fc2f72bb0c9607` | Search the sibling compiler prefix for the install layout | Modifies `build/cmake/wxWidgetsConfig.cmake.in` so MSVC and clang-cl consumers can find compatible library layouts produced by the other compiler |
| `88f3483ca546fbf4ad732e1acd94cc930935077a` | Merge PR #7 | Merge of the preceding compiler-prefix fix |
| `5b7e8c0cde6b975d63613188d2ac6c1ab8769fbc` | Patches from OrcaSlicer | Net changes in `src/osx/cocoa/colour.mm` (use sRGB color components) and `src/msw/webview_edge.cpp` (keep WebView2 rasterization at monitor DPI); the same commit records reverts of private-header installation and build-option defaults |
| `b44c39c100975a0ac0e46f937aa3f3eae5e18631` | Don't send unsupported Wayland release requests | Modifies `src/gtk/wayland.cpp`: binds seats at protocol version 5 and supplies handlers for the v5 pointer events |

The resulting comparison from the upstream 3.3.2 base to the current fork branch lists four changed paths:

- `build/cmake/wxWidgetsConfig.cmake.in`
- `src/gtk/wayland.cpp`
- `src/msw/webview_edge.cpp`
- `src/osx/cocoa/colour.mm`

Each of the three modified source files retains its wxWidgets source header identifying the `wxWindows licence`. The Wayland commit message describes its change as a backport of the approach proposed in wxWidgets PR #27069 and says that PR was awaiting merge at the time of the fork commit; this review records the fork's commit description, not an independent finding about the later upstream PR state.

The OrcaSlicer dependency CMake also adds a post-install step that copies `include/wx/private`, `include/wx/generic/private`, and `include/wx/gtk/private` into the install prefix because OrcaSlicer uses these private accessibility headers. This is a consumer-side install customization separate from the four-file fork delta.

## 3. License and notice evidence

At the current fork branch tip:

- `docs/licence.txt` contains the **wxWindows Library Licence, Version 3.1**, including the copyright line for Julian Smart, Robert Roebling et al. The text describes the library as licensed under the GNU Library General Public Licence version 2 or (at the recipient's option) any later version, with a wxWidgets exception.
- The exception text expressly discusses using, copying, linking, modifying, and distributing binary object-code versions of works based on the library under the distributor's own terms. It also contains conditions for code copied from GPL/LGPL sources and for modifications where the modifier does not wish the exception to apply. Preserve the full, unmodified license text and file-level notices; this summary is not a legal interpretation.
- `docs/wine/COPYING.LIB` contains the GNU Library General Public License version 2 text. Its location under `docs/wine` is unusual for the main wxWidgets license reference, which says the LGPL text is usually supplied as `COPYING.LIB`; confirm the intended notice/package mapping rather than assuming the path alone resolves distribution requirements.
- `misc/languages/data/unicode/unicode-license.txt` is an additional license file in the source tree and should be included in the notice review if the associated Unicode data is shipped.
- The recursive tree contains 12 Git submodule entries. The source declaration inspected here does not explicitly list submodule revisions or a `GIT_SUBMODULES` setting. Their initialization and actual use in the dependency build remain to be verified.

The wxWidgets README describes its license as a modified LGPL that permits use in proprietary applications, including static linking. The exact terms to preserve are in the checked-in license text, not merely that README summary.

## 4. Pinned evidence

OrcaSlicer v2.4.2:

- [wxWidgets dependency declaration](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps/wxWidgets/wxWidgets.cmake)

Fork source and lineage:

- [Current `v3.3.2` branch tip](https://github.com/OrcaSlicer/Orca-deps-wxWidgets/tree/b44c39c100975a0ac0e46f937aa3f3eae5e18631)
- [Upstream wxWidgets 3.3.2 base commit](https://github.com/wxWidgets/wxWidgets/commit/db1005db3dea2c37a46fb455a9a02e37aa360751)
- [Compiler-prefix fix](https://github.com/OrcaSlicer/Orca-deps-wxWidgets/commit/4a671ff5ce797f99cf535b5ea3fc2f72bb0c9607)
- [OrcaSlicer patch merge](https://github.com/OrcaSlicer/Orca-deps-wxWidgets/commit/5b7e8c0cde6b975d63613188d2ac6c1ab8769fbc)
- [Wayland protocol fix](https://github.com/OrcaSlicer/Orca-deps-wxWidgets/commit/b44c39c100975a0ac0e46f937aa3f3eae5e18631)
- [wxWindows Library Licence 3.1](https://github.com/OrcaSlicer/Orca-deps-wxWidgets/blob/b44c39c100975a0ac0e46f937aa3f3eae5e18631/docs/licence.txt)
- [LGPL v2 text in docs/wine/COPYING.LIB](https://github.com/OrcaSlicer/Orca-deps-wxWidgets/blob/b44c39c100975a0ac0e46f937aa3f3eae5e18631/docs/wine/COPYING.LIB)
- [Unicode data license](https://github.com/OrcaSlicer/Orca-deps-wxWidgets/blob/b44c39c100975a0ac0e46f937aa3f3eae5e18631/misc/languages/data/unicode/unicode-license.txt)

## 5. Remaining work

1. Determine the exact wxWidgets commit used by each historical OrcaSlicer release/build. The mutable branch ref cannot establish this after the fact.
2. For future reproducibility, replace the branch ref with an immutable commit or retained, hash-verified archive, after confirming the intended source contents.
3. Determine whether and how the 12 submodules are initialized and consumed by each supported build path; preserve their gitlink SHAs and applicable component notices.
4. Trace how `docs/licence.txt`, the LGPL text, Unicode data notice, and source-file notices are carried into source distributions and each platform's binary third-party notices.
5. Verify whether all four current fork changes are present in the actual source fetched by the relevant release build; this cannot be inferred from the mutable branch name alone.

## 6. Limitations

This review establishes the current branch's upstream base and observed delta, plus the license files and submodule gitlinks present in its current tree. It does not prove the historical build's fetched commit, verify an archive checksum, establish submodule build behavior, inspect release artifacts, or make a legal determination. No dependency source or build configuration was changed.
