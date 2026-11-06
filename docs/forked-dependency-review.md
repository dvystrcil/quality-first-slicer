# Review of OrcaSlicer-maintained dependency sources

**Status:** Targeted source-reference review; incomplete provenance and license audit  
**Upstream baseline:** OrcaSlicer `v2.4.2`, commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**Reviewed build declarations:** `deps/Blosc/Blosc.cmake`, `deps/OpenVDB/OpenVDB.cmake`, `deps/wxWidgets/wxWidgets.cmake`, `deps/GMP/GMP.cmake`

This review resolves several source references and inspects selected fork changes. It is not a complete file-by-file diff, independent archive verification, complete dependency license audit, or build validation.

## 1. Blosc — forked branch archive

OrcaSlicer downloads:

- Repository: [tamasmeszaros/c-blosc](https://github.com/tamasmeszaros/c-blosc)
- Source ref in CMake: branch archive `v1.17.0_tm`
- Resolved branch commit observed through the GitHub API: `ab274210ddf40af659811062323cb0d6a0c64d76`
- Commit date: 2021-03-24
- Commit subject: `Fix wrong compiler features detection on AppleClang`
- CMake archive SHA-256 declaration: `dcb48bf43a672fa3de6a4b1de2c4c238709dad5893d1e097b8374ad84b1fc3b3`

The fork is based on `Blosc/c-blosc`. Comparing its master history with upstream Blosc v1.17.0 showed 12 commits ahead and no commits behind that release. The additional history includes Windows DLL installation changes, compiler/build fixes, safer LZ4 decompression behavior, and restoration of an initial bounds check in the BloscLZ decompressor.

The checked-in CMake uses the archive URL for a branch ref, not an immutable commit URL. The declared archive hash protects the expected bytes when the build downloads the archive, but the branch name itself is mutable. For our own reproducible dependency manifest, record the resolved commit and archive digest together. Prefer an immutable commit archive or retained, hash-verified source archive.

The fork tree includes a `LICENSES/` directory with separate notices for Blosc and bundled codec components (including Bitshuffle, FastLZ, LZ4, Snappy, stdint, and zlib). A single project-level license label is not a substitute for reviewing and retaining all of these notices. The fork repository metadata does not expose a detected SPDX license.

**Finding:** The fork appears to contain meaningful portability and decompression-safety changes, not just an arbitrary repackaging. Preserve the exact fork changes and all component notices if this dependency is retained. Do not replace it with upstream Blosc without testing the fixes and build behavior.

## 2. OpenVDB — forked commit archive

OrcaSlicer downloads:

- Repository: [tamasmeszaros/openvdb](https://github.com/tamasmeszaros/openvdb)
- Exact source commit: `a68fd58d0e2b85f01adeb8b13d7555183ab10aa5`
- Commit date: 2022-01-26
- Commit subject: `Additional fixes on windows`
- CMake archive SHA-256 declaration: `f353e7b99bd0cbfc27ac9082de51acf32a8bc0b3e21ff9661ecca6f205ec1d81`

The fork is based on [AcademySoftwareFoundation/openvdb](https://github.com/AcademySoftwareFoundation/openvdb). The exact commit inspected modifies the OpenVDB CMake configuration by removing installation of several find modules (including FindBlosc, FindIlmBase, and FindOpenEXR) and adding `-Wa,-mbig-obj` for MinGW. The OrcaSlicer dependency build additionally applies its local `0001-clang19.patch`; that patch must be reviewed together with the fork commit.

The fork's `LICENSE` file contains the Mozilla Public License 2.0 text. Its README also identifies MPL-2.0 as the project license. GitHub's repository metadata reports `NOASSERTION`; that metadata result should not override the actual source license file. MPL-2.0 includes an express secondary-license mechanism, but any combined-work decision still needs a file-level notice review and qualified license review.

**Finding:** The dependency is pinned to an immutable source commit and a declared archive hash. Preserve the fork commit and OrcaSlicer's additional patch as distinct provenance layers. Do not treat the GitHub `NOASSERTION` field as evidence that the source is unlicensed.

## 3. wxWidgets — forked branch with documented upstream base

The v2.4.2 CMake declaration uses the SoftFever repository URL, `GIT_TAG v3.3.2`, and `GIT_SHALLOW ON`, but does not record an immutable commit or archive digest. The URL now resolves to [OrcaSlicer/Orca-deps-wxWidgets](https://github.com/OrcaSlicer/Orca-deps-wxWidgets). The resolved repository has `refs/heads/v3.3.2`, but no `refs/tags/v3.3.2`; the CMake ref is therefore a mutable branch, not a release tag.

The current branch tip observed on 2026-11-06 is `b44c39c100975a0ac0e46f937aa3f3eae5e18631`. Its merge base is `db1005db3dea2c37a46fb455a9a02e37aa360751`, which GitHub confirms is identical to upstream `wxWidgets/wxWidgets` ref `v3.3.2`. The fork branch is four commits ahead and zero behind that upstream base.

The current fork delta affects four files:

- `build/cmake/wxWidgetsConfig.cmake.in`: compiler-prefix fallback so MSVC and clang-cl can consume compatible library layouts.
- `src/osx/cocoa/colour.mm`: use sRGB color components.
- `src/msw/webview_edge.cpp`: keep WebView2 rasterization aligned with monitor DPI.
- `src/gtk/wayland.cpp`: bind Wayland seats at protocol v5 and add handlers for v5 pointer events.

The branch history includes the compiler-prefix fix, its merge, the OrcaSlicer macOS/Windows patches (with two other proposed changes later reverted), and the Wayland backport. The three modified source files retain wxWindows license headers. OrcaSlicer's dependency CMake also copies selected wxWidgets private headers after install; this is a consumer-side customization, separate from the fork delta.

License evidence is now available in the fork tree: `docs/licence.txt` contains the wxWindows Library Licence 3.1 and its LGPL-based exception; `docs/wine/COPYING.LIB` contains GNU Library GPL v2 text; and `misc/languages/data/unicode/unicode-license.txt` is an additional notice to account for if its data is shipped. The LGPL text's placement under `docs/wine` needs notice-packaging review rather than an assumption that it is the intended primary license copy. The recursive tree also contains 12 Git submodules; their initialization and consumption by the Orca dependency build have not been established.

**Finding:** The upstream base and current fork delta are now substantially resolved, but the source pin remains non-reproducible because the build follows a mutable branch. The current branch tip does not prove which commit historical release builds fetched. See [wxWidgets 3.3.2 fork provenance and license review](wxwidgets-3.3.2-fork-provenance-review.md) for commit-level evidence, license details, submodule SHAs, and remaining work.

## 4. GMP — release asset from SoftFever

OrcaSlicer downloads:

- Release repository: [SoftFever/OrcaSlicer_deps](https://github.com/SoftFever/OrcaSlicer_deps)
- Release tag: `gmp-6.2.1`
- Asset: `gmp-6.2.1.tar.bz2`
- Release published: 2023-10-06
- CMake archive SHA-256 declaration: `eae9326beb4158c386e39a356818031bd28f3124cf915f8c5b1dc4c7a36b4d7c`

The release API reports no asset-level digest. The CMake file does declare a SHA-256 for the downloaded archive, which is useful integrity metadata, but the release repository's visible README is only a short description and does not explain the source preparation, patches, or release process. The CMake build also applies `0001-GMP_GCC15.patch`.

**Finding:** The declared archive hash is a useful integrity check, but source provenance is incomplete from the release metadata alone. Compare the archive contents to the corresponding GNU GMP 6.2.1 source, inspect the local patch, and retain the exact archive and verification record before relying on this release asset.

## 5. Source-pin quality summary

| Dependency | Source pin in Orca build | Current reproducibility assessment | Remaining evidence |
|---|---|---|---|
| Blosc | Branch archive + SHA-256 | Archive content can be hash-checked; source ref is mutable | Independently verify archive hash; record immutable commit and all notices |
| OpenVDB | Commit archive + SHA-256 | Stronger immutable source reference | Review full fork delta and local patch; reconcile file-level notices |
| wxWidgets | Mutable shallow branch `v3.3.2` | Current branch tip and upstream base resolved; historical build commit remains unknown | Pin immutable commit; verify submodule use and release notice packaging; see [wxWidgets fork review](wxwidgets-3.3.2-fork-provenance-review.md) |
| GMP | Release asset + SHA-256 | Archive can be hash-checked; source preparation unclear | Verify archive against GNU source; inspect patch and release provenance |

## 6. Follow-up requirements

- [ ] Independently download and verify each declared SHA-256; this remote review did not recalculate hashes.
- [ ] Replace wxWidgets `v3.3.2` branch with an immutable commit or retained hash-verified archive; establish historical release commit, submodule initialization, and notice packaging. See [wxWidgets fork review](wxwidgets-3.3.2-fork-provenance-review.md).
- [ ] Inspect the full OpenVDB fork delta against the exact upstream base relevant to the 2022 source revision; the single commit inspected here is not the entire fork delta.
- [ ] Review the Blosc component notices and determine exactly which codec implementations are enabled by OrcaSlicer's build options.
- [ ] Compare the GMP release archive against GNU GMP 6.2.1, inspect its local patch, and identify the release build/source process.
- [ ] Review all dependency patches and platform-specific branches, including OpenEXR and OCCT.
- [ ] Complete the Linux, macOS, MinGW, and Windows dependency matrix.
- [ ] Reconcile the resulting source inventory with a generated SBOM and a manual license/notice audit.

## 7. Conclusion

The forked dependencies are not interchangeable with their upstream projects without review. Blosc carries portability and decompression changes; OpenVDB has a specific Windows/MinGW-oriented fork and an additional Orca patch; wxWidgets is sourced from a fork using a mutable shallow branch with a now-documented upstream base and four-commit delta; and GMP comes from a SoftFever release asset with a separate local patch.

These observations help explain why OrcaSlicer uses these sources, but they do not approve them for import. No source has been copied into this project, no dependency has been accepted, and no final project license decision is made here.
