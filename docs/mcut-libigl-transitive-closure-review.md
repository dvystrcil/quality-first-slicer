# MCUT and libigl source-closure follow-up

**Status:** MCUT upstream tag substantially identified; active nested components and local deltas documented. libigl entry-point closure partially inspected; exact source revision and complete transitive closure remain unresolved.  
**Reviewed OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (v2.4.2)

## 1. MCUT: upstream tag and source identity

The vendored MCUT tree corresponds substantially to upstream **`cutdigital/mcut` tag `v1.2.0`**, but is not a byte-for-byte copy of that tag.

The following files have matching Git blob IDs between OrcaSlicer and upstream `v1.2.0`:

| File | Shared blob SHA |
|---|---|
| `source/mcut.cpp` | `f3b5c1deed1b9d2523c32ade4cdd7d710c3630a8` |
| `source/kernel.cpp` | `4ec72329f91aeea75f84713c5750825e5e18b7bd` |
| `source/hmesh.cpp` | `cfc3d219dcfbcef744bdcc1af00dfa2e23a1aafd` |
| `source/bvh.cpp` | `925642188e9f0080c4095702e03ff5f2b787258a` |
| `source/frontend.cpp` | `467e1117754220848959ff6cbd2c77709bc67728` |
| `source/preproc.cpp` | `01b21f92819c9f507164722997299ce1cb54b1fc` |
| `include/mcut/mcut.h` | `76f68f3fd5b7912f02a6ee0f3e519d07b3cd10af` |
| `LICENSE.txt` | `237246b1dc85df5e4fa95d5748e73122124885dc` |
| `LICENSE.GPL.txt` | `94a9ed024d3859793618152ea559a168bbcbb5e2` |
| `include/mcut/internal/cdt/cdt.h` | `cdc96095e41535ec35d09de21c19c6350a6f7ae7` |

Three reviewed files differ from the tag:

| File | OrcaSlicer blob SHA | Upstream v1.2.0 blob SHA |
|---|---|---|
| `CMakeLists.txt` | `69c42610c9ba8a272c83a2182c7a68afa751a208` | `464854dc54ca96c1a75d2959ed1d91f6b28ecd4c` |
| `source/math.cpp` | `8d6fe59b3250b6f7a940ab637bd31c0cd6c7d43b` | `cdb5c70eca2a9ee341080de82462e911b62c2993` |
| `source/shewchuk.c` | `b23c3bea9dbf70dd00d812af7424a39a8688a141` | `67c01955a51c1b45bda8dc37bd826ca42deca807` |

The evidence supports `v1.2.0` as the upstream source tag for this vendored component, with at least these three local deltas to review. The exact delta and its authorship have not yet been established.

Version identifiers also need to be read in context: the vendored CMake file sets the package version to **1.2.0**, while `mcut.h` defines API header version **1.2.100**. The same values appear in the upstream tag; they are separate version fields, not evidence by themselves of a version mismatch.

Pinned upstream references:

- [MCUT v1.2.0 CMakeLists](https://github.com/cutdigital/mcut/blob/v1.2.0/CMakeLists.txt)
- [MCUT v1.2.0 public API header](https://github.com/cutdigital/mcut/blob/v1.2.0/include/mcut/mcut.h)
- [MCUT v1.2.0 license-choice document](https://github.com/cutdigital/mcut/blob/v1.2.0/LICENSE.txt)
- [MCUT v1.2.0 GPLv3 text](https://github.com/cutdigital/mcut/blob/v1.2.0/LICENSE.GPL.txt)

## 2. MCUT: active source, license notices, and nested components

### 2.1 GPL/commercial choice

The CMake file and public API header both state **GPL-3.0-or-later by default** and identify a commercial license available from Floyd M. Chitalu. The root `LICENSE.txt` says the GPL and commercial options are mutually exclusive. `LICENSE.GPL.txt` is the full GPL version 3 text.

No commercial license, written permission, or project-specific election record was found in the reviewed source tree. Therefore, the documented default for this audit remains GPL-3.0-or-later; the presence of a commercial option is not evidence that OrcaSlicer obtained it.

### 2.2 Compiled source files and per-file notice coverage

The vendored CMake target compiles eight files:

- `mcut.cpp`, `kernel.cpp`, `hmesh.cpp`, `math.cpp`, and `bvh.cpp` carry the MCUT GPL-3.0-or-later default/commercial-option notice in their source headers.
- `frontend.cpp` and `preproc.cpp` are compiled into the same target but do not show that same notice at the start of the inspected files. The root MCUT license documents remain the component-level licensing evidence; retain this file-level notice gap in the inventory.
- `shewchuk.c` is also compiled into the target. It retains Jonathan Richard Shewchuk's public-domain dedication and says it is a modified version used in Cinolib, listing the local modifications. Its blob differs from upstream MCUT v1.2.0 and the exact Cinolib-to-MCUT-to-Orca delta has not been traced.

### 2.3 CDT is actively included

The MCUT target compiles `source/frontend.cpp`, which includes `mcut/internal/cdt/cdt.h`. The nested CDT component is therefore not merely dormant content.

The nested `cdt.h` carries an MPL-2.0 notice. MCUT's root `LICENSE.txt` separately states that the CDT files, originally under MPL-2.0, are dual-licensed under MPL-2.0 and GPL. Preserve both the nested MPL notice and the parent component's dual-license statement; do not collapse the entire MCUT tree into one undifferentiated license label.

The optional `FetchContent` block in MCUT's CMake downloads libigl v2.3.0 and Eigen only when MCUT tests or tutorials are enabled. MCUT is added as a subdirectory in OrcaSlicer, and the CMake file only creates the default-ON test/tutorial options when MCUT is the top-level project. Source inspection suggests these fetches are not part of the ordinary parent-project configuration, but a real configure using supported presets is still needed to confirm the effective option values.

## 3. libigl: first-level source-closure findings

### 3.1 Provider and version are configuration-dependent

OrcaSlicer's `deps_src/libigl/CMakeLists.txt` first calls `find_package(libigl QUIET)`. If a system package is found, it links `igl::core`; otherwise it exposes the vendored `deps_src/libigl` include tree.

The checked-in README mentions libigl v2.5.0 as the latest version, but this is not a source pin. Selected files match the upstream `libigl/libigl` v2.5.0 tag by Git blob SHA (including `mesh_boolean.h`, `mesh_boolean_type_to_funcs.h`, and `IGL_ASSERT.h`), while other files do not (including `mesh_boolean.cpp` and `writePLY.h`). No exact upstream commit or complete vendored source delta is recorded. The build may also select a system package instead of the bundled tree.

### 3.2 Used entry point and inspected includes

`src/libslic3r/MeshBoolean.cpp` includes `<igl/copyleft/cgal/mesh_boolean.h>` and calls `igl::copyleft::cgal::mesh_boolean` for subtraction and self-union. The entry-point `mesh_boolean.h` and `mesh_boolean.cpp` both carry MPL-2.0 notices.

The implementation includes a first group of libigl helper files. The following inspected headers carry MPL-2.0 notices: `assign_scalar.h`, `extract_cells.h`, `propagate_winding_numbers.h`, `relabel_small_immersed_cells.h`, `remesh_self_intersections.h`, `string_to_mesh_boolean_type.h`, `combine.h`, `PlainVector.h`, `PlainMatrix.h`, `cumsum.h`, `extract_manifold_patches.h`, `get_seconds.h`, `parallel_for.h`, `remove_unreferenced.h`, `resolve_duplicated_faces.h`, `unique_edge_map.h`, and `unique_simplices.h`.

A second inspection of selected helpers reached additional MPL-2.0-noticed files, including `BinaryWindingNumberOperations.h`, `assign.h`, `cell_adjacency.h`, `extract_cells_single_component.h`, `closest_facet.h`, `outer_facet.h`, `submesh_aabb_tree.h`, `triangle_triangle_adjacency.h`, `vertex_triangle_adjacency.h`, `extract_non_manifold_edge_curves.h`, `piecewise_constant_winding_number.h`, and `writeOBJ.h`.

### 3.3 File-level notice gaps and scope limits

The following files encountered in this first-level inspection did not show a file-level MPL/GPL/LGPL notice in the inspected header region:

- `igl/copyleft/cgal/mesh_boolean_type_to_funcs.h` and its `.cpp` implementation;
- `igl/copyleft/cgal/string_to_mesh_boolean_type.cpp` (its corresponding header does carry MPL-2.0);
- `igl/IGL_ASSERT.h`;
- `igl/writePLY.h`.

Absence of a visible header is not proof that a file is unlicensed or GPL-licensed. It is a notice/provenance question requiring the upstream file history and applicable project-level licensing evidence.

No GPL/LGPL file was identified in the direct include list and selected helper headers inspected for this entry point. The broader `igl/copyleft` subtree still contains other GPL/LGPL examples, but the current evidence does not show that those particular files are used by this call path. This is not a complete recursive include/template-instantiation closure. The CGAL headers used by the implementation also require an independent license review for the exact selected CGAL package and configuration.

## 4. Follow-up required

1. Record and review the local MCUT changes in `CMakeLists.txt`, `source/math.cpp`, and `source/shewchuk.c` against upstream v1.2.0; establish their authorship and rationale.
2. Preserve MCUT's full GPLv3 text, commercial-option notice, CDT MPL-2.0 text, and dual-license statement in source and release third-party notices.
3. Confirm whether OrcaSlicer relies on the default GPL-3.0-or-later grant or has written commercial licensing permission. Do not infer a commercial license from the available option.
4. Preserve the Shewchuk public-domain attribution and Cinolib-modification notice; complete the source delta/provenance record for this modified predicate file.
5. Pin the exact libigl upstream revision and resolve the differences from v2.5.0. Record whether each supported build uses system libigl or the vendored tree.
6. Finish the recursive include/template-instantiation closure for `igl::copyleft::cgal::mesh_boolean`; resolve the missing file-level notices listed above with upstream provenance evidence.
7. Review the exact CGAL package/version and effective build configuration. A directory name or a README warning is not a substitute for file-level and dependency-closure evidence.
8. Configure supported build presets and inspect the resulting linked targets and release artifacts before making any distribution conclusion.

## 5. Scope and limitations

This is a documentation-only follow-up. No source or license file was changed or imported; no MCUT commercial license was assumed; no complete libigl recursive closure, local build, binary/package inspection, SBOM, or legal determination was performed.
