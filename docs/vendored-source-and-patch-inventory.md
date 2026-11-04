# Vendored source and local patch inventory — OrcaSlicer v2.4.2

**Status:** First-pass remote tree inventory; incomplete origin, revision, nested-license, and patch applicability review  
**Reviewed upstream revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (`v2.4.2`)  
**Scope:** `deps_src/` tree, its top-level CMake inclusion list, and patch/diff-like files under `deps/`  
**Method:** GitHub tree and file inspection at the fixed upstream tag. No local checkout, source build, complete file-by-file review, or SBOM generation was performed.

## 1. Executive findings

- `deps_src/CMakeLists.txt` explicitly adds **27 vendored components**: 7 header-only/interface libraries and 20 static-library or utility subprojects, as classified by the upstream CMake comments.
- The tree contains identifiable license/notice files for 12 of those components. A later targeted source-header review found license declarations embedded in several additional components; see [selected source-header review](deps-src-license-header-review.md). This remains incomplete and does not establish that all nested components or required notices are covered.
- **MCUT is an active, high-priority licensing gate:** its own CMake file states GPL-3.0-or-later by default and mentions a commercial license option. OrcaSlicer's `MeshBoolean.cpp` calls the MCUT API and the application CMake links `mcut`. Its tree also contains a separate GPL license and a license for the bundled internal CDT component. See the [targeted MCUT/libigl license review](mcut-libigl-license-review.md); the exact combined license obligations still require review.
- The tree also contains projects with no obvious top-level license/notice filename. Absence from a filename scan is not proof that a project is unlicensed; some declarations are embedded in source headers. HIDAPI's exact license selection and the `hints` utility's license remain unresolved.
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
| clipper2 | Static library | Not found as a separate file; Boost license in source headers | Boost Software License 1.0; CMake version 1.5.2 conflicts with `clipper.version.h` 2.0.1 |
| earcut | Header-only/interface | `LICENSE` | Inspect license text and upstream revision |
| expat | Static library | `COPYING` | Also check source fallback and build selection |
| fast_float | Header-only/interface | Not found as a separate file; MIT text in `fast_float.h` | MIT; README records 2.0.0 / commit `fe1ce58` |
| glu-libtess | Static library | Not found as a separate file; SGI license in implementation files | SGI Free Software License B 2.0; README records Mesa GLU source commit |
| hidapi | Static library | Referenced license files absent from vendored subset | **Unresolved multi-license selection** (GPLv3, BSD-style, or original HIDAPI); see [selected source-header review](deps-src-license-header-review.md) |
| hints | Static library / utility per upstream comment | Not found | Authorship, origin, and license unresolved; see [selected source-header review](deps-src-license-header-review.md) |
| imgui | Static library | `LICENSE.txt` | Check bundled extensions and attribution |
| imguizmo | Static library | `LICENSE` | Check upstream relationship and bundled files |
| libigl | Static library | Not found | Has upstream and Orca-specific READMEs; inspect nested/copyleft content |
| libnest2d | Static library | `LICENSE.txt` | Inspect bundled dependencies and notices |
| mcut | Static library | `LICENSE.txt`, `LICENSE.GPL.txt`, nested CDT `LICENSE.txt` | **GPL/commercial dual-licensing gate; nested CDT license also applies** |
| md4c | Static library | `LICENSE.md` | Inspect license and bundled files |
| mdns | Static library | `NOTICE.md` | Notice is not necessarily the complete license text |
| minilzo | Static library | `COPYING` | Inspect license terms and any exceptions |
| miniz | Static library | `LICENSE` | Also has upstream README attribution |
| nanosvg | Header-only/interface | Not found as a separate file; custom permissive grant in headers | Custom three-condition license; embedded upstream attributions and exact fork commit still need review |
| nlohmann | Header-only/interface | Not found as a separate file; MIT/SPDX in `json.hpp` | MIT; exact upstream version/commit still needs resolution |
| qhull | Static library | `COPYING.txt` | Inspect bundled source and notices |
| qoi | Static library | Not found as a separate file; MIT text in `qoi.h` | MIT; `qoilib.c` includes PrusaSlicer-specific integration changes |
| semver | Static library | Not found as a separate file; MIT notice in `semver.c` | MIT; exact upstream revision still needs resolution |
| stb_dxt | Header-only/interface | Not found as a separate file; BSD notice in `stb_dxt.h` | BSD 2-Clause; exact upstream revision still needs resolution |

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
