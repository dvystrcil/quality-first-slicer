# wxWidgets 3.3.2 fork provenance and license review

**Status:** Source lineage substantially resolved; historical build pin, submodule consumption, and release notice packaging remain open  
**OrcaSlicer baseline:** `v2.4.2`, commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**Build declaration:** `deps/wxWidgets/wxWidgets.cmake`  
**Method:** GitHub API inspection of the fixed OrcaSlicer CMake declaration, the fork branch/ref, upstream wxWidgets history, selected fork commits, source headers, license files, and the recursive Git tree. No local checkout/build, submodule initialization, archive hash, binary package, or legal review.

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
