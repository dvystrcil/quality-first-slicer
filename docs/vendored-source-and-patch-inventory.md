# Vendored source and local patch inventory — OrcaSlicer v2.4.2 and 2.5.0

**Status:** Updated for OrcaSlicer 2.5.0 in §0 (slice D4 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)). §0 records every `deps_src/` change and every patch or replacement-file change between v2.4.2 and 2.5.0, and compares each changed vendored file with its upstream. Sections 1–6 below are the v2.4.2 inventory, kept as history; where §0 corrects them, it says so. Origin, nested-license and patch-applicability review is still incomplete for the components 2.5.0 did not touch. **Nothing here is approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off.  
**OrcaSlicer baseline:** 2.5.0: fork `baseline-2.5.0` `665552c1e4b950b32707953cbca67e178e219366` (no differences from upstream v2.5.0 `40ecc66f` under `deps/` or `deps_src/`; see the [delta](dependency-delta-2.4.2-to-2.5.0.md)). §1–6: `v2.4.2`, `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**Scope:** `deps_src/` tree, its top-level CMake inclusion list, and patch, diff and replacement files under `deps/`  
**Method:** §0: `git diff 8500fcdc 665552c1 -- deps_src deps` and `git show` in a local OrcaSlicer clone; upstream tags shallow-cloned or read through the GitHub API into scratch directories and compared file by file (Git blob IDs or `diff`). Nothing was built or run. §1–6: GitHub tree and file inspection at the fixed v2.4.2 tag; no local checkout, source build, complete file-by-file review, or SBOM generation.

## 0. OrcaSlicer 2.5.0 update (slice D4, reviewed 2026-11-19)

### 0.1 Summary

- `deps_src/CMakeLists.txt` now adds **26** subdirectories (was 27): `add_subdirectory(clipper)` is gone (`deps_src/CMakeLists.txt`, 2.4.2 line 18). `deps_src/pybind11` is new but is not added there; the root `CMakeLists.txt:1041-1044` builds a `pybind11::embed` interface target from its headers. `deps_src/` therefore holds 27 directories, `hints` included.
- **clipper2 1.5.2 → 2.0.1.** The vendored tree is upstream `Clipper2_2.0.1` plus Orca changes. Three of them are **new in 2.5.0 and change behaviour**: engine nodes are allocated through oneTBB's `scalable_malloc`, round offsets use a different step count, and concave corners are joined differently. Two files are BETA upstream, and Clipper2 now links `TBB::tbbmalloc`. See §0.2.
- **libigl:** a whole-tree comparison shows the v2.4.2 copy was **byte-identical to libigl v2.6.0** (`40e7900c`, all 1,241 files). That corrects the "exact upstream revision is unpinned" note in §2 and in the [MCUT/libigl review](mcut-libigl-license-review.md). In 2.5.0, 15 `igl/copyleft/cgal/` files differ from v2.6.0, and every changed line is the CGAL 6 rename `AABB_traits` → `AABB_traits_3` and `AABB_triangle_primitive` → `AABB_triangle_primitive_3`. Upstream libigl `main` has not made that change.
- **mcut:** the one 2.5.0 change in `tpool.h` is the same as upstream commit `89326e29` ("fix hang in wait_for_data", 2024-11-01), which is on `master` but in no MCUT tag. A whole-tree comparison against v1.2.0 also found **two local deltas the [source-closure review](mcut-libigl-transitive-closure-review.md) did not list**: an added `#include <chrono>` in `frontend.h` and `#include <cstdint>` in `hmesh.h`. Both were already there in v2.4.2.
- **admesh, imgui, imguizmo, libnest2d, semver:** each 2.5.0 change is an Orca change. None of them is in the upstream version the tree is based on or on the upstream default branch. No license or notice text changed in any of them.
- **miniz, qhull:** only the Orca-written `CMakeLists.txt` changed (compiler flags and link targets). No upstream source changed.
- **pybind11 3.0.1 added:** all 54 files are byte-identical to `pybind/pybind11` `v3.0.1` (`f5fbe867`). This was re-checked here and agrees with [B5](cpython-pybind11-provenance-license-review.md).
- **Legacy Clipper removed** (`deps_src/clipper`, 5 files). Its review is [historical](clipper-legacy-license-use-review.md).
- **Patch files:** 14 → 9 patch or diff files. The OCCT patch was replaced, the OpenCV patches (2) and PNG patches (3) were deleted, and the GMP patch was edited. One replacement file was added (`deps/TBB/MSVC.cmake`), one was added with SLVS (`deps/SLVS/CMakeLists.txt.in`), and one was removed with OpenCSG (`deps/OpenCSG/CMakeLists.txt.in`). **`deps/Boost/0001-Boost-fix.patch` and `deps/TBB/0001-TBB-GCC13.patch` are not referenced by any build file in v2.4.2 or 2.5.0**, so they are not applied. See §0.4.
- No license or notice file under `deps_src/` was changed or removed (legacy Clipper had none). The only one added is `deps_src/pybind11/LICENSE` (`git diff --name-status` filtered for license, copying, notice and readme names).

### 0.2 clipper2 1.5.2 → 2.0.1

**Upstream compared:** `AngusJohnson/Clipper2` tag `Clipper2_2.0.1` → commit `21ebba05db8894f0c7217ad35ea518080f324946` (released 2025-12-19), directory `CPP/Clipper2Lib`. For the v2.4.2 copy: tag `Clipper2_1.5.2` → `6901921c4be75126d1de60bfd24bd86a61319fd0`.
**Orca commit:** `222c6a2df5` "Improve performance by migrating to Clipper2 2.0.1 (#15969)". `clipper.version.h` and the `project()` line in `deps_src/clipper2/CMakeLists.txt` both say 2.0.1.

| File (under `Clipper2Lib/`) | Compared with `Clipper2_2.0.1` |
|---|---|
| `include/clipper2/clipper.export.h`, `clipper.version.h` | Byte-identical |
| `include/clipper2/clipper.core.h`, `clipper.h`, `clipper.minkowski.h`, `clipper.offset.h`, `clipper.rectclip.h`, `clipper.triangulation.h`; `src/clipper.rectclip.cpp`, `clipper.triangulation.cpp` | Namespace switch only: `#ifdef USINGZ namespace Clipper2Lib_Z { #else namespace Clipper2Lib { #endif`. The same switch was in the v2.4.2 copy |
| `include/clipper2/clipper.engine.h` | Namespace switch; `Clipper2LibArea<T>()` helper used by `PolyPath64::Area()`/`PolyPathD::Area()` (also in v2.4.2); **new in 2.5.0:** a `CLIPPER2_NODE_ALLOCATOR` macro ("Orca: engine nodes are allocated through tbbmalloc") declared in `Vertex`, `OutPt`, `OutRec`, `Active`, `LocalMinima`, `PolyPath` |
| `src/clipper.engine.cpp` | Namespace switch; **new in 2.5.0:** `#include <oneapi/tbb/scalable_allocator.h>` and class `operator new`/`delete` for those six types using `scalable_malloc`/`scalable_free` ("Orca: tbbmalloc scales far better than the default heap when all slicing threads clip at once") |
| `src/clipper.offset.cpp` | Namespace switch; **new in 2.5.0, changes output:** (1) round-join step count uses `std::max(round(...), 1)` where upstream uses `ceil(...)` ("Orca: round the step count like Clipper1 did"); (2) a new `OffsetConcaveCrossing()` joins a concave corner at the crossing of the two edge offsets when it is safe, used by `OffsetPolygon()` unless a delta callback is set ("Orca: … 3-point loops make dense inward offsets slow"). Neither is on upstream `main` at `4be46556` (2026-11-19) |
| `include/clipper2/clipper2_z.hpp`, `src/clipper2_z.cpp` | Not upstream. The Orca/Prusa "hackish wrapper" that compiles the library a second time with `USINGZ`. 2.5.0 adds `#include "clipper.triangulation.cpp"` to `clipper2_z.cpp` |

Other facts from the files:

- `deps_src/clipper2/CMakeLists.txt` compiles the new `clipper.triangulation.{h,cpp}`. Its header says `Release : BETA RELEASE`. No `Triangulate(` call was found under `src/` at `665552c1`, so it is compiled but not called by the app (a `git grep`, not a link-map check).
- Clipper2 now has `target_link_libraries(Clipper2 PRIVATE TBB::tbbmalloc)`. oneTBB's `tbbmalloc` is now in the Clipper2 link closure. oneTBB is already reviewed as a `deps/` dependency.
- Every upstream file keeps its `License : https://www.boost.org/LICENSE_1_0.txt` header line. The two wrapper files and `clipper.version.h` have none. As in v2.4.2, upstream's `LICENSE` file (Boost Software License 1.0) is not in the vendored subset.
- The v2.4.2 copy was not a byte-identical 1.5.2 either. Besides the namespace switch, `Clipper2LibArea` and the wrapper files, 1.5.2 had trailing-whitespace differences in several files (`clipper.export.h` among them). §2 called it "matching upstream release commit `6901921c`", which is true of the version but not of every byte.

### 0.3 Other vendored components changed in 2.5.0

| Component | Upstream compared (tag → commit) | 2.5.0 change (Orca commit) | Same change upstream? |
|---|---|---|---|
| **libigl** | `libigl/libigl` `v2.6.0` → `40e7900ccbd767f1f360e0eb10f0f1a6432e0993`, the version `deps_src/libigl/README-OrcaSlicer.md` names. Whole tree: v2.4.2 1,241/1,241 files identical; 2.5.0 1,226 identical, 15 differ | 15 files in `igl/copyleft/cgal/`, 65 lines. After undoing the rename `AABB_traits_3`→`AABB_traits` and `AABB_triangle_primitive_3`→`AABB_triangle_primitive`, the removed and added lines are identical (checked by sorting both sets). This is the CGAL 6 API (`e729dbf142` "Upgrade CGAL from 5.6.3 to 6.2.1 (#16258)") | No. `main` at `b41f1944` has no `AABB_traits_3` in `closest_facet.h` |
| **libnest2d** | Not resolved (§2 left this open). Checked against `tamasmeszaros/libnest2d` `master` `663daa69`, PrusaSlicer `master` `e6c85c50` (`bundled_deps/libnest2d`) and BambuStudio `master` `8e524a39` (`src/libnest2d`) | `nester.hpp`: six new `Item` fields for z-range and bed-exclusion volumes. `nfpplacer.hpp`: optional `should_check_collision` callback that limits which packed items constrain the NFP; an `on_bin` clamp keeping a pile on the bed when it is aligned off-centre (belt printers); fixed items always go to `excludes`, and the inner-fit NFP is skipped when there are none ("can exceed clipper's range and crash MSVC"). `geometries.hpp`: `Slic3r::ClipperLib::jtSquare` → `Slic3r::jtSquare` (Clipper2 migration). Commits `785aa2637b`, `bfbf5ad1c2`, `61a0db4a87`, `a0a4a33c72`, `222c6a2df5` and merges | No. `should_check_collision` and `on_bin` are absent from all three |
| **imgui** | `ocornut/imgui` `v1.83` → `ad5d1a8429ea219d3d34e6a36a48918650402697` (`IMGUI_VERSION "1.83"`). Whole tree: 7 of 12 shared files already differed in v2.4.2; 8 in 2.5.0 | `imgui_draw.cpp`: adds U+2103 (℃) to the default glyph ranges (`117ed0060d`, #15202). `imstb_textedit.h` (was identical to v1.83): multi-line click and drag clamp `y` to the text's vertical bounds, two new blocks of 51 and 44 lines (`66d3f3f9c3`, #15052) | No. Not in imgui `master` `77fe4588` `imstb_textedit.h`, nor in BambuStudio `master`. Not checked against `nothings/stb` |
| **imguizmo** | `CedricGuillemet/ImGuizmo` `1.83` → `664cf2d73864a36b2a8b5091d33fc4578c885eca` (the README's "latest stable tagged version"). `ImGuizmo.cpp` already differed by 912 lines in v2.4.2, so the vendored base is not the 1.83 tag itself; the exact base is still unresolved | `ImGuizmo.cpp`: the view navigator holds mouse capture for the whole drag (`SetNextFrameWantCaptureMouse(true)`, or `CaptureMouseFromApp()` before imgui 1.87), 13 lines (`63085be729`, #17284) | No. Absent from `master` `105e4fde` (`src/ImGuizmo.cpp`) |
| **admesh** | Orca's admesh is the PrusaSlicer C++ derivative, not `admesh/admesh`. Checked against PrusaSlicer `master` `e6c85c50` (`bundled_deps/admesh/admesh/stlinit.cpp`) and BambuStudio `master` `8e524a39` (`src/admesh/stlinit.cpp`) | `stlinit.cpp`: (1) a file classed as ASCII is re-classed as binary when its size equals the header facet count × 50 + header (`4b4a261787`, #16130); (2) `fscanf`/`sscanf` get field widths (`%255[^\n]`, `%15s %127s %15s`) against stack overflows (`d112a0af29`, #15594). The GPL-2.0-or-later notice block is unchanged | (1) not in either. (2) BambuStudio has a similar `%255[^\n]` fix on a differently named buffer (`solid_content`, line 182), not the same text; the `sscanf` widths are in neither |
| **mcut** | `cutdigital/mcut` `v1.2.0` → `953375ca9cbfec5f5c697d00265e06b114154b19`. Whole tree: v2.4.2 24 of 29 files identical, 2.5.0 23 | `include/mcut/internal/tpool.h`: `push()` calls `disrupt_wait_for_data()` (which takes `head_mutex` before `notify_one()`) where it called `data_cond.notify_one()` directly (`1466c0e57f`, #16330 "Fix rare hang") | **Yes:** identical to upstream `89326e290ebdfefb4db281cf93e98bc77867d03d` (Dmitry, 2024-11-01), on `master` (`d424aec5`) and in no tag (`git tag --contains` is empty; v1.3.0 is older) |
| **miniz** | `README-Prusa.txt`: miniz 2.1.0 amalgamated plus Prusa changes. Not compared: only the build file changed | `CMakeLists.txt` (Orca-written; defines `miniz_static`): `-Wno-error=incompatible-pointer-types` for clang-cl (`d865e9e6e1`) | n/a (integration file) |
| **qhull** | Qhull 2015.2 (`README.txt`). Not compared: only the build file changed | `CMakeLists.txt` (Orca-written; uses `slic3r_remap_configs`): the static system-Qhull branch always links the release `Qhull::qhullcpp`/`qhullstatic_r`, with no `_d` debug variants (`6c6e8be43d`, #14593) | n/a (integration file) |
| **semver** | Checked against `h2non/semver.c` `master` `bd1db234` (upstream has no `dev` handling) | `semver.c` `compare_prerelease`: inside the existing "Orca: Special handling for 'dev'" block, the two return values are swapped, so `x.y.z-dev` now ranks **above** every other prerelease and below the release (`a8d73e6456`). It changes how the app orders versions, for example for update checks; that use was not traced | No (the `dev` block is Orca's) |

**MCUT, outside the 2.5.0 delta:** the whole-tree comparison found five v2.4.2 files that differ from v1.2.0. The [source-closure review](mcut-libigl-transitive-closure-review.md) §6 lists three of them (`CMakeLists.txt`, `source/math.cpp`, `source/shewchuk.c`). The other two are one added line each: `#include <chrono>` in `include/mcut/internal/frontend.h` and `#include <cstdint>` in `include/mcut/internal/hmesh.h` (OrcaSlicer history: `f6ac67e601` "Fix VS2022 17.13 build failure", then `883607e1d4` "Refactor folder"). `tpool.h` makes six in 2.5.0.

### 0.4 Added and removed

| Change | Evidence | Note |
|---|---|---|
| **Added `deps_src/pybind11`** (54 files) | `PYBIND11_VERSION_*` 3/0/1 in `include/pybind11/detail/common.h`; `LICENSE` (BSD-3-Clause-style, Wenzel Jakob); added in `ecddf3d18f` "feat: Python Plugins" | All 54 blob IDs equal `pybind/pybind11` `v3.0.1` → `f5fbe867d2d26e4a0a9177a51f6e568868ad3dc8` (re-checked here through the GitHub tree API). No local change. Reviewed in [B5](cpython-pybind11-provenance-license-review.md), **not approved** |
| **Removed `deps_src/clipper`** (`clipper.cpp`, `clipper.hpp`, `clipper_z.cpp`, `clipper_z.hpp`, `CMakeLists.txt`) | `222c6a2df5`; `deps_src/CMakeLists.txt` no longer adds it. No `ClipperLib::` or `clipper.hpp` reference is left under `src/` at `665552c1` (`git grep`) | The [legacy Clipper review](clipper-legacy-license-use-review.md) is historical |
| **Removed `deps/GLEW/glew`** (vendored under `deps/`, not `deps_src/`) | `35bac4cb69` "Remove unused OpenCSG, GLEW and GLU dependencies (#16318)" | Not in the §2 table, which covers `deps_src/` only. The removal is in the [delta §4](dependency-delta-2.4.2-to-2.5.0.md#4-removed) |

### 0.5 Patch and replacement-file inventory for 2.5.0

Patch or diff files under `deps/`: **9** in 2.5.0 (14 in v2.4.2). "Applied" means a non-comment `PATCH_COMMAND` in the 2.5.0 build files names the file; no configure run checked it.

| File | 2.5.0 status | Applied by (2.5.0) | Note |
|---|---|---|---|
| `deps/OCCT/0001-BRepMesh-seam-pcurve-at-edge-parameter.patch` | **Added**, replaces `0001-OCCT-fix.patch` (221 lines, install-layout changes, **deleted**) | `deps/OCCT/OCCT.cmake:37` `git apply` | 28 lines, one file: `src/ModelingAlgorithms/TKMesh/BRepMesh/BRepMesh_ModelPreProcessor.cxx`. It takes the seam pcurve's first point at the edge parameter instead of `FirstParameter()`. The build file's comment links [Open-Cascade-SAS/OCCT#572](https://github.com/Open-Cascade-SAS/OCCT/issues/572) ("Cone surface cannot be triangulated", **open**) and says to remove the patch once a release has the fix. `git apply --check` succeeds against that file at `V8_0_1` → `b8f597c677811d1f9f4d8a97f5ae2825c0353a42`. Commits `78a4f2867c`, `8790b07773` |
| `deps/OpenCV/0001-vs.patch`, `0002-clang19-macos.patch` | **Deleted** | n/a | OpenCV 4.14.0 has no patch (`1008a47870`) |
| `deps/PNG/PNG.patch`, `0002-clang19-macos.patch`, `macos-arm64.patch` | **Deleted** | n/a | libpng 1.6.59 has no patch and one build path. `PNG.patch` was the one that removed Adler-32 validation behaviour (§3); 2.5.0 no longer carries it (`710341338c`) |
| `deps/GMP/0001-GMP_GCC15.patch` | **Edited** (3 hunks) | `deps/GMP/GMP.cmake:70` `git apply` (source-build path only) | Only the replacement probe line changed: `void g(int,t1 const*,t1,t2,t1 const*,int){}` → `void g(int a,t1 const*b,t1 c,t2 dd,t1 const*e,int ff){}`, in each of three copies of the configure probe. Unnamed parameters in a C function definition are not valid before C23, which is the likely reason (`1e038bfc53`, "build deps on older GCC"). Now applied to the GMP **6.3.0** source |
| `deps/OpenEXR/0001-OpenEXR-GCC13.patch` | Unchanged | `deps/OpenEXR/OpenEXR.cmake:34` (`_patch_cmd`) | |
| `deps/OpenVDB/0001-clang19.patch` | Unchanged | `deps/OpenVDB/OpenVDB.cmake:17` | |
| `deps/ZLIB/0001-Respect-BUILD_SHARED_LIBS.patch` | Unchanged | `deps/ZLIB/ZLIB.cmake:1`, `:10` | |
| `deps/Blosc/blosc-mods.patch` | Unchanged | **Not applied**: `PATCH_COMMAND` is commented out at `deps/Blosc/Blosc.cmake:17`, `:36` | As in v2.4.2 |
| `deps/Boost/0001-Boost-fix.patch` | Unchanged | **Not referenced** by any other file in the OrcaSlicer tree, in v2.4.2 or 2.5.0 (`git grep -l 'Boost-fix' -- . ':!*.patch'` finds nothing) | §3 said "confirm exact application condition". The answer is that nothing applies it |
| `deps/TBB/0001-TBB-GCC13.patch` | Unchanged | **Not referenced** by any other file in v2.4.2 or 2.5.0 (same `git grep` for `TBB-GCC13`) | Same as Boost |

Replacement files copied over upstream sources (not named `.patch`):

| File | 2.5.0 status | Copied by | Compared with upstream |
|---|---|---|---|
| `deps/TBB/MSVC.cmake` (98 lines) | **Added** (`0a7ac3f2ac` "fix: disable TBB LTCG to allow linking with lld-link") | `deps/TBB/TBB.cmake:1-2`: copied to `./cmake/compilers/MSVC.cmake` when `MSVC` (clang-cl included) | oneTBB `v2021.5.0` → `3df08fe234f23e732a122809b40eb129ae22733f` `cmake/compilers/MSVC.cmake` (85 lines): `/W4` only with `TBB_STRICT`; the IPO flags (`-flto`, `/GL`, `-LTCG`) apply only when `TBB_ENABLE_IPO`, which follows `CMAKE_INTERPROCEDURAL_OPTIMIZATION` (`TBB.cmake` passes both `OFF`); the rest is blank-line changes. Build flags only |
| `deps/TBB/GNU.cmake` | Unchanged (Flatpak + GCC only; not listed in §3) | `deps/TBB/TBB.cmake:3-4` | Against the same tag: adds `-Wno-error=stringop-overflow` (comment cites oneTBB#843) and clears the IPO flags |
| `deps/SLVS/CMakeLists.txt.in` | **Added** (`5d120921d5`) | `deps/SLVS/SLVS.cmake:8`, replaces upstream's `CMakeLists.txt` | Reviewed in [B4](slvs-provenance-license-review.md) |
| `deps/OpenCSG/CMakeLists.txt.in` | **Removed** with OpenCSG (`35bac4cb69`) | n/a | |

`deps/OpenEXR/patch_openexr_arm64.cmake` (a CMake script run as `PATCH_COMMAND` on Windows ARM64, `OpenEXR.cmake:39`) is unchanged. The new `deps/` projects' own build steps, such as CPython's `msbuild.rsp` copy (`deps/python3/python3.cmake:167`), are in slices B and C.

### 0.6 Open questions for the maintainer

1. **Clipper2 local changes:** the offset step-count and concave-join changes change geometry output and are not upstream. The allocator change adds a tbbmalloc dependency. Should they be kept, reported upstream, or recorded as a permanent fork delta? (Not a license question; Boost-1.0 allows modification.)
2. **Unapplied patch files:** `0001-Boost-fix.patch` and `0001-TBB-GCC13.patch` are in the tree but nothing applies them. Record as dead files, or confirm with a configure run?
3. **libigl pin:** §2 and the [MCUT/libigl review](mcut-libigl-license-review.md) say the libigl revision is unpinned. This comparison pins v2.4.2 to v2.6.0 exactly. Should those docs be updated, or is the correction here enough?
4. **imguizmo base:** the vendored `ImGuizmo.cpp` is far from the 1.83 tag. Its upstream base is still unresolved.
5. **Notices:** as for v2.4.2, no build step was found that stages the clipper2, libigl, pybind11 or mcut license texts into an app package. Not re-checked in detail for 2.5.0.

### 0.7 Limitations

- Changed files were compared with the named upstream refs only. Components that 2.5.0 did not change were not compared again, except where a whole-tree comparison was cheap (libigl, mcut, imgui, imguizmo); those results are above.
- "Not upstream" means not found at the upstream ref named in the table on 2026-11-19. Other forks and older branches were not searched.
- No build, configure or test run. Whether the patches apply cleanly was checked only for the OCCT patch (`git apply --check` on a single file).
- **Not approved.** This section records what the files say and draws no legal conclusions.

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
| admesh | Static library | Not found as a separate file; GPL notice in source headers | GPL-2.0-or-later; all seven target files preserve the notice, but upstream `COPYING` and the referenced `AUTHORS` are absent from the vendored subset. Active API use is confirmed in `TriangleMesh.cpp`; no ADMesh-specific linking exception found. See [ADMesh GPL notice review](admesh-gpl-notice-review.md) and [selected source-header review](deps-src-license-header-review.md) |
| agg | Header-only/interface | `copying` | AGG 2.4 headers identify Maxim Shemanarev (2002–2005); `copying` presents two alternative grants (AGG Public License and Modified BSD), but no project-specific license election is recorded. Initial BambuStudio 1.0.10 import is traced; exact upstream archive/commit and source deltas remain unresolved. Active SLA rasterization includes confirmed. See [AGG 2.4 provenance and license-election review](agg-2.4-provenance-license-election.md) |
| ankerl | Header-only/interface | No standalone file; full MIT notice embedded in `unordered_dense.h` | Exact byte match to upstream `martinus/unordered_dense` 4.5.0 commit `73f3cbb237e84d483afafc743f1f14ec53e12314`; header preserves MIT notice and 2022–2024 Martin Leitner-Ankerl copyright. Active Arachne use confirmed. Release notice distribution remains unverified. See [ankerl provenance review](ankerl-unordered-dense-provenance-review.md) |
| clipper | Static library | No standalone license file found in the vendored subtree; Boost notice embedded in source headers | Boost Software License 1.0; both 2D and Z-enabled variants are actively compiled. Initial BambuStudio import was banner 6.2.9 (macro 6.2.6); OrcaSlicer later records a PrusaSlicer-derived upgrade to 6.4.2 but leaves the macro stale. `clipper.cpp` is byte-identical to the PrusaSlicer 6.4.2 snapshot; header has two identified local differences. Exact original archive checksum and complete delta attribution remain open. See [legacy Clipper license and active-use review](clipper-legacy-license-use-review.md) |
| clipper2 | Static library | Not found as a separate file; Boost license in source headers | Boost Software License 1.0; CMake and version header both report 1.5.2, matching upstream release commit `6901921c4be75126d1de60bfd24bd86a61319fd0` |
| earcut | Header-only/interface | `LICENSE` | ISC License; vendored license file exactly matches Mapbox Earcut 2.2.4, and README identifies 2.2.4. Header differs from pinned upstream in two small places (extra `<cstdint>`, omitted `iterations` counter); active GUI include/API call confirmed. Original archive/checksum, attribution of the two differences, and release notice distribution remain open. See [Earcut provenance review](earcut-provenance-review.md) |
| expat | Static library | `COPYING` in `deps_src/expat`; separate MIT notices in `deps/EXPAT/expat` | Two source trees: `deps_src/expat` identifies stripped/modified Expat 2.2.0; `deps/EXPAT/expat` identifies a separate 2.5.0 copy. `deps_src` unconditionally defines a static `expat` target, while application linkage uses `${EXPAT_LIBRARIES}` from system Expat or the `deps/EXPAT` ExternalProject fallback. Active XML parser calls confirmed in AMF, 3MF, and GUI code. Exact provider per build configuration, duplicate target/source usage, and release notice staging remain to be verified. See [Expat duplicate-vendoring and provider review](expat-duplicate-vendoring-provider-review.md) |
| fast_float | Header-only/interface | No separate file in vendored subtree; complete MIT grant and attribution embedded in `fast_float.h` | README pins fast_float 2.0.0 / upstream commit `fe1ce5805331d9edae6fe71f10e0b38c3ac4bbe7`; original import and README addition are traced. Eight application source files include/call `fast_float::from_chars`. The interface target is defined, but consumer include propagation and generated build evidence remain open; About-dialog attribution field is currently blank. See [fast_float provenance and license review](fast-float-provenance-license-review.md) |
| glu-libtess | Static library | Not found as a separate file; SGI license in implementation files | SGI Free Software License B 2.0; README records Mesa GLU source commit |
| hidapi | Static library | Four upstream license files absent from vendored subset | Upstream 0.9.0 commit `7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f` offers GPLv3, BSD-style, or original HIDAPI license at the user's discretion; OrcaSlicer's election remains unknown. History traces 3Dconnexion integration (2019-09), Linux hidraw backend selection, and the 0.9.0 README pin, but no license election. All four referenced license documents remain omitted. GUI linkage and platform source selection are confirmed. See [HIDAPI provenance and license-election review](hidapi-provenance-license-election.md) |
| hints | Internal utility (not third-party) | No file-level notice found | `HintsToPot.cpp` first appears in the BambuStudio 1.0.10 source import and builds a translation-template generator and an interface target. Two later changes are attributed in Git history to `zhaofengli`; original author and copyright holder remain unverified. See [hints utility provenance review](hints-utility-provenance.md) and [hints attribution review](hints-attribution-review.md) |
| imgui | Static library | `LICENSE.txt` | Check bundled extensions and attribution |
| imguizmo | Static library | `LICENSE` | Check upstream relationship and bundled files |
| libigl | Static library | Not found | Active `igl::copyleft::cgal::mesh_boolean` use; entry-point files are MPL-2.0, but several helper files lack visible file notices, exact upstream revision is unpinned, and the recursive include closure is incomplete. See [MCUT/libigl license review](mcut-libigl-license-review.md) and [source-closure follow-up](mcut-libigl-transitive-closure-review.md) |
| libnest2d | Static library | `LICENSE.txt` | Inspect bundled dependencies and notices |
| mcut | Static library | `LICENSE.txt`, `LICENSE.GPL.txt`, nested CDT `LICENSE.txt` | **GPL-3.0-or-later default; commercial option not evidenced as obtained.** Upstream v1.2.0 substantially pinned. Local deltas are now characterized: CMake changes static/shared default and disables upstream install/CPack notice staging; `math.cpp` adds `<cstdint>` plus formatting; `shewchuk.c` comments out two `compress` implementations and initializes six predicate length variables. CDT is actively included and dual-licensed MPL-2.0/GPL; modified Shewchuk predicates retain public-domain/Cinolib attribution. Authorship, runtime impact, notice packaging, and commercial-license evidence remain unresolved. See [MCUT/libigl license review](mcut-libigl-license-review.md) and [source-closure follow-up](mcut-libigl-transitive-closure-review.md)** |
| md4c | Static library | `LICENSE.md` | MIT; copyright © 2016–2024 Martin Mitáš. MD4C 0.5.2 upstream tag identified; five reviewed source/header files match exactly, but `md4c.c` has substantial untraced local changes. Active release-note rendering and GUI linkage confirmed. Upstream install/export rules are disabled; application notice staging remains unverified. See [MD4C provenance and license review](md4c-provenance-license-review.md) |
| mdns | Static library | `NOTICE.md` | Composite component: Mattias Jansson mDNS library (public domain) plus CrealityPrint v7.1.1 C++ wrapper (AGPL-3.0). All four files exactly match the CrealityPrint tag; the mDNS files differ from pinned mjansson/mdns upstream and local deltas are characterized. Active LAN discovery and GUI linkage confirmed; release notice staging remains unverified. See [mDNS provenance and license review](mdns-provenance-license-review.md) |
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
