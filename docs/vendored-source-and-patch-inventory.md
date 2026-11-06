# Vendored source and local patch inventory — OrcaSlicer v2.4.2

**Status:** First-pass remote tree inventory; incomplete origin, revision, nested-license, and patch applicability review  
**Reviewed upstream revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (`v2.4.2`)  
**Scope:** `deps_src/` tree, its top-level CMake inclusion list, and patch/diff-like files under `deps/`  
**Method:** GitHub tree and file inspection at the fixed upstream tag. No local checkout, source build, complete file-by-file review, or SBOM generation was performed.

## 1. Executive findings

- `deps_src/CMakeLists.txt` adds **27 subdirectories**: 7 header-only/interface libraries and 20 static-library/utility subprojects, as classified by upstream CMake comments. One of these, `hints`, is an internal BambuStudio translation-template utility rather than a third-party dependency; the remaining 26 are the third-party component inventory.
- The tree contains identifiable license/notice files for 12 of those components. A later targeted source-header review found license declarations embedded in several additional components; see [selected source-header review](deps-src-license-header-review.md). This remains incomplete and does not establish that all nested components or required notices are covered.
- **MCUT is an active, high-priority licensing gate:** its own CMake file states GPL-3.0-or-later by default and mentions a commercial license option. OrcaSlicer's `MeshBoolean.cpp` calls the MCUT API and the application CMake links `mcut`. Its tree also contains a separate GPL license and a license for the bundled internal CDT component. See the [targeted MCUT/libigl license review](mcut-libigl-license-review.md); the exact combined license obligations still require review.
- The tree also contains projects with no obvious top-level license/notice filename. Absence from a filename scan is not proof that a project is unlicensed; some declarations are embedded in source headers. HIDAPI's upstream 0.9.0 commit and available license choices are now pinned, but OrcaSlicer's selected license and omitted notices remain unresolved. The `hints` utility's history is traced to the BambuStudio 1.0.10 source import; its individual copyright attribution remains unconfirmed.
- The dependency build contains **14 patch/diff-like files** under `deps/`. Their existence is not equivalent to application: some are conditional, some are copy/replacement steps rather than patches, and the Blosc patch command is commented out in the inspected v2.4.2 CMake.
- This is an inventory, not approval to import any component or patch.

## 2. Vendored component inventory

The following 27 directories are explicitly included by `deps_src/CMakeLists.txt`.

| Component | CMake classification | License/notice filename found in tree scan | Initial review note |
|---|---|---|---|
| Shiny | Static library | Not found as a separate file; MIT text in `Shiny.h` | MIT header found; see [selected source-header review](deps-src-license-header-review.md) |
| admesh | Static library | Not found as a separate file; GPL notice in source headers | GPL-2.0-or-later; linked into `libslic3r_cgal`; see [selected source-header review](deps-src-license-header-review.md) |
| agg | Header-only/interface | `copying` | Inspect exact license text and provenance |
| ankerl | Header-only/interface | Not found | README exists; license/provenance unresolved |
| clipper | Static library | Not found as a separate file; Boost license in `clipper.hpp` | Boost Software License 1.0; actual compiled/consumed legacy subset needs tracing |
| clipper2 | Static library | Not found as a separate file; Boost license in source headers | Boost Software License 1.0; CMake and version header both report 1.5.2, matching upstream release commit `6901921c4be75126d1de60bfd24bd86a61319fd0` |
| earcut | Header-only/interface | `LICENSE` | Inspect license text and upstream revision |
| expat | Static library | `COPYING` | Also check source fallback and build selection |
| fast_float | Header-only/interface | Not found as a separate file; MIT text in `fast_float.h` | MIT; README records 2.0.0 / commit `fe1ce58` |
| glu-libtess | Static library | Not found as a separate file; SGI license in implementation files | SGI Free Software License B 2.0; README records Mesa GLU source commit |
| hidapi | Static library | Four upstream license files absent from vendored subset | Upstream 0.9.0 commit `7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f` offers three alternative license elections; OrcaSlicer's selection is unrecorded and all four referenced license documents are omitted. The vendored header blob matches upstream exactly; GUI linkage and platform source selection are confirmed. See [HIDAPI provenance and license-election review](hidapi-provenance-license-election.md) |
| hints | Internal utility (not third-party) | No file-level notice found | `HintsToPot.cpp` first appears in the BambuStudio 1.0.10 source import; it builds a translation-template generator and an interface target. File-level copyright attribution still needs confirmation; see [hints utility provenance review](hints-utility-provenance.md) |
| imgui | Static library | `LICENSE.txt` | Check bundled extensions and attribution |
| imguizmo | Static library | `LICENSE` | Check upstream relationship and bundled files |
| libigl | Static library | Not found | Active `igl::copyleft::cgal::mesh_boolean` use; entry-point files are MPL-2.0, but several helper files lack visible file notices, exact upstream revision is unpinned, and the recursive include closure is incomplete. See [MCUT/libigl license review](mcut-libigl-license-review.md) and [source-closure follow-up](mcut-libigl-transitive-closure-review.md) |
| libnest2d | Static library | `LICENSE.txt` | Inspect bundled dependencies and notices |
| mcut | Static library | `LICENSE.txt`, `LICENSE.GPL.txt`, nested CDT `LICENSE.txt` | **GPL-3.0-or-later default; commercial option not evidenced as obtained. Upstream v1.2.0 substantially pinned; local CMake, `math.cpp`, and `shewchuk.c` differ. CDT is actively included and dual-licensed MPL-2.0/GPL; modified Shewchuk predicates preserve a public-domain attribution. See [MCUT/libigl license review](mcut-libigl-license-review.md) and [source-closure follow-up](mcut-libigl-transitive-closure-review.md)** |
| md4c | Static library | `LICENSE.md` | Inspect license and bundled files |
| mdns | Static library | `NOTICE.md` | Notice is not necessarily the complete license text |
| minilzo | Static library | `COPYING` | Inspect license terms and any exceptions |
| miniz | Static library | `LICENSE` | Also has upstream README attribution |
| nanosvg | Header-only/interface | Not found as a separate file; custom permissive grant in headers | SoftFever fork commit `863f6aa97ef62028126fa2c19bd4350394c2e15e` pinned. `nanosvgrast.h` matches upstream exactly; `nanosvg.h` has a local zero-initialization change that must be marked as altered. Embedded Anti-Grain Geometry, stb_truetype-derived rasterization, and FLTK modification attributions are reviewed in [NanoSVG attribution review](nanosvg-embedded-attribution-review.md); copied-code boundaries and license elections remain unresolved. See also [source provenance review](nanosvg-nlohmann-provenance.md) |
| nlohmann | Header-only/interface | Not found as a separate file; MIT/SPDX in `json.hpp` | Exact match of all 41 vendored files to upstream nlohmann/json 3.10.4 commit `fec56a1a16c6e1c1b1f4e116a20e79398282626c`; MIT; see [source provenance review](nanosvg-nlohmann-provenance.md) |
| qhull | Static library | `COPYING.txt` | Inspect bundled source and notices |
| qoi | Static library | Not found as a separate file; MIT text in `qoi.h` | MIT; `qoilib.c` includes PrusaSlicer-specific integration changes |
| semver | Static library | Not found as a separate file; MIT notice in `semver.c` | MIT; exact upstream revision still needs resolution |
| stb_dxt | Header-only/interface | No separate upstream license file found; BSD 2-Clause text in `stb_dxt.h` | RygsDXTc mirror commit `8b983d43c85f84c1c16665c1661b16acd1f6f429` pinned; Orca header is a close derivative with a small wrapper delta and matches the inspected BambuStudio header blob exactly. Copyright-holder/year notice remains unresolved; see [stb_dxt provenance review](stb-dxt-provenance-review.md) |

The upstream CMake comments classify `agg`, `ankerl`, `earcut`, `fast_float`, `nanosvg`, `nlohmann`, and `stb_dxt` as header-only/interface libraries. The remaining entries are in the static-library/utility group. This classification describes the upstream CMake organization, not necessarily every target emitted by each subdirectory.

### 2.1 Nested and non-obvious licensing risks

- MCUT contains `include/mcut/internal/cdt/LICENSE.txt` in addition to its project-level license files. Review both; do not collapse them into a single MCUT license label.
- libigl contains a `igl/copyleft/` subtree and a TetGen README. This requires targeted inspection of the exact files compiled or included by OrcaSlicer and any additional license/notice obligations.
- Several projects have no license-named file at the component root. Inspect source-file headers, nested directories, package metadata, and upstream repository history before concluding the applicable license.
- `deps_src/README_CMAKE_INTERFACES.md` is project integration documentation, not a license inventory. Its claims about target interfaces should not be treated as evidence of provenance.

## 3. Local patch and modification inventory

The fixed v2.4.2 tree contains 14 patch/diff-like files under `deps/`:

| Patch / modification file | Target | Initial purpose indicated by patch | Applicability caveat |
|---|---|---|---|
| `deps/Blosc/blosc-mods.patch` | Blosc | Blosc 1.17 fixes and CMake configuration changes | Patch command is commented out in the inspected Blosc CMake; do not count as applied without further evidence |
| `deps/Boost/0001-Boost-fix.patch` | Boost.Process | Process/handle limit and pipe/handle behavior changes | Confirm exact application condition and target Boost source |
| `deps/GMP/0001-GMP_GCC15.patch` | GMP | Adjust generated configure/acinclude compiler probe | Source-build path only; prebuilt MSVC binaries are a separate provenance path |
| `deps/OCCT/0001-OCCT-fix.patch` | OCCT | Changes install layout for binaries/libraries | Confirm platform/build branch and resulting package layout |
| `deps/OpenCV/0001-vs.patch` | OpenCV | Adds/updates MSVC runtime recognition, including newer compiler versions | Windows/MSVC-specific |
| `deps/OpenCV/0002-clang19-macos.patch` | OpenCV | macOS/Clang 19 compatibility changes | Inspect exact source version and platform condition |
| `deps/OpenEXR/0001-OpenEXR-GCC13.patch` | OpenEXR | Adds missing standard integer includes for newer GCC | Linux/GCC conditional according to build matrix |
| `deps/OpenEXR/patch_openexr_arm64.cmake` | OpenEXR | CMake patching/configuration for Windows ARM64 | Script is a patch mechanism, not a conventional unified diff |
| `deps/OpenVDB/0001-clang19.patch` | OpenVDB | Clang 19 template-call compatibility | Applied on the relevant source build path |
| `deps/PNG/0002-clang19-macos.patch` | libpng | Uses `math.h` instead of obsolete Apple `fp.h` selection | Platform/compiler-specific |
| `deps/PNG/PNG.patch` | libpng | Removes conditional Adler-32 validation behavior | Confirm exact source branch and security/behavior implications |
| `deps/PNG/macos-arm64.patch` | libpng | Apple ARM64 cross-compilation and architecture handling | Conditional cross-compile path; includes related PNG behavior changes |
| `deps/TBB/0001-TBB-GCC13.patch` | oneTBB | Qualifies `task` type as `tbb::task` | Confirm exact compiler and build condition |
| `deps/ZLIB/0001-Respect-BUILD_SHARED_LIBS.patch` | zlib | Changes target construction to respect `BUILD_SHARED_LIBS` | Confirm exact application condition and target zlib source revision |

Additional maintained source/build-file replacement not named as a `.patch`/`.diff` file:

- `deps/OpenCSG/CMakeLists.txt.in` is copied into the downloaded source tree by the dependency build. Treat this as a maintained build-file replacement and review its provenance/diff.
- Some dependency CMake files use copy commands or direct source modifications. The full effective source delta must be derived from each active `ExternalProject_Add` configuration, not from filename extensions alone.

## 4. Important build-time behavior discovered

- `deps_src/CMakeLists.txt` uses `add_subdirectory` for each listed component; these are checked-in source trees, not ordinary ExternalProject downloads.
- MCUT's own CMake contains `FetchContent` logic for libigl and Eigen when it is built as a standalone project. The parent-project condition and actual OrcaSlicer configuration must be checked to determine whether that network fetch runs in the integrated build.
- The MCUT CMake file explicitly states GPL-3.0-or-later as its default license and notes a commercial license can be purchased. This is a blocking provenance/license question for any reuse that includes MCUT.
- The dependency graph is configuration-dependent. A vendored directory being present does not prove its targets are built, linked, shipped, or even enabled in every platform configuration.

## 5. Required follow-up evidence

1. For every component, resolve canonical upstream repository, exact release/tag/commit, source tree relationship, and any Orca/Prusa/vendor modifications.
2. Inspect every license and notice file, all nested license files, source headers, and bundled subcomponents. Record SPDX identifiers only when supported by the actual text; the [selected source-header review](deps-src-license-header-review.md) is a partial first pass.
3. Trace which targets and source files are built for Linux, macOS, MinGW, and MSVC; distinguish compiled, header-included, optional, disabled, and packaged components.
4. For each patch or replacement, record target source revision, exact application command, platform/compiler condition, patch hash, patch result, and rationale.
5. Resolve the concrete copyright notice/holder/year for stb_dxt before treating its BSD-2-Clause source and binary notice obligations as complete; see [stb_dxt provenance review](stb-dxt-provenance-review.md).
5. Reconcile MCUT and libigl/copyleft licensing before considering import. Obtain qualified legal review where the project's intended distribution model makes the license consequences uncertain.
6. Generate an SBOM from a reproducible checkout/build configuration and manually reconcile it with this source inventory.
7. Preserve all upstream notices and Orca/Prusa attribution; do not copy any source or asset into this project until its individual provenance and license obligations are cleared.

## 6. Evidence and limitations

- Verified by remote GitHub tree inspection at OrcaSlicer v2.4.2 commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`.
- Verified that the top-level `deps_src/CMakeLists.txt` includes all 27 named directories.
- Verified the presence/absence of license-like filenames using a tree-path scan. This is not a full content/license scan.
- Verified the existence and sampled content of the patch files listed above. Full patch applicability and complete platform conditions remain to be traced.
- No local source checkout, source archive extraction for these components, build, SBOM generation, complete license review, or legal review was performed.

**Conclusion:** the vendored source tree and patch set are now enumerated at a fixed upstream revision, but they are not approved for import. MCUT's GPL/commercial licensing and the incomplete license/provenance coverage are explicit blockers to resolve before source reuse.
