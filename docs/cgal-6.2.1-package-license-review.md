# CGAL 6.2.1 package-license review (OrcaSlicer 2.5.0)

**Status:** Source-level provenance and package-license review of the CGAL release that OrcaSlicer 2.5.0 builds. It succeeds the [CGAL 5.6.3 package-license review](cgal-5.6.3-package-license-review.md), which stays as the v2.4.2 record. Not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off.
**Slice:** D3 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (build files identical to upstream v2.5.0 `40ecc66f`); v2.4.2 `8500fcdc` for comparison
**Method:** downloaded `CGAL-6.2.1.zip` into an empty scratch directory and re-hashed it; listed it and read its license files and per-file SPDX headers with `python3 -I` (nothing extracted to disk, built or run). Tag and release metadata from the GitHub API. Application use from `git grep` on `665552c1` and `8500fcdc`.
**Reviewed:** 2026-11-19

## 1. Pin and integrity

| Item | Value | Evidence |
|---|---|---|
| Declared archive | `https://github.com/CGAL/cgal/releases/download/v6.2.1/CGAL-6.2.1.zip` | `deps/CGAL/CGAL.cmake:10` |
| Declared SHA-256 | `eebd737d9b7f0199647ba5c1f9f6c7a3d0651aacef9c2fd4dedc52da6c25edbe` | `deps/CGAL/CGAL.cmake:11` |
| Download (41,102,950 bytes) | **PASS**, same hash. Also PASS in the slice A run ([archive-verification.md](archive-verification.md#250-verification-result)) | re-hashed for this review |
| GitHub release asset digest | `sha256:eebd737d…edbe`, the declared hash. Release published 2026-09-04 13:39:57 UTC | `repos/CGAL/cgal/releases/tags/v6.2.1` |
| Tag `v6.2.1` | annotated tag `2e3640e7` → commit **`28811b671a12b5caa9e3688569dadbc6b3728fe6`** | matches the commented `GIT_TAG` at `deps/CGAL/CGAL.cmake:7-8`. The archive's `$Id:` lines also name `28811b671a1` |
| `VERSION` in the archive | `6.2.1` | |
| Superbuild order | after Boost, Eigen, GMP, MPFR (`DEPENDS`, `:12`) | |

**What the app asks for:** `find_package(CGAL 6.2 REQUIRED)` at `src/libslic3r/CMakeLists.txt:627`. In v2.4.2 the call had no version (the 5.6.3 review recorded that). A CGAL older than 6.2 is now rejected at configure time. The provider is still whatever CMake finds first on the prefix path, so a system or caller-supplied CGAL 6.2.x would be accepted. Not checked on a build.

## 2. Where the application uses CGAL

Nine files include CGAL headers in 2.5.0, up from five in v2.4.2. They include 78 distinct CGAL headers, up from 24.

| File | In v2.4.2 | Target |
|---|---|---|
| `src/libslic3r/MeshBoolean.cpp` | yes | `libslic3r_cgal` (`src/libslic3r/CMakeLists.txt:633-640`) |
| `src/libslic3r/CutSurface.cpp` | yes | `libslic3r_cgal` |
| `src/libslic3r/Triangulation.cpp` | yes | `libslic3r_cgal` |
| `src/libslic3r/MeshRepair.cpp` | **new** | `libslic3r_cgal` |
| `src/libslic3r/Geometry/VoronoiUtilsCgal.cpp` | yes | `libslic3r` (`:334`) |
| `src/libslic3r/TextureToColor/ColorUtils.cpp` (+ `CgalUtils.hpp`, `Repair.hpp`) | **new** | `libslic3r` (`:208-211`) |
| `src/slic3r/GUI/Selection.cpp` | yes | GUI |

Calls into GPL packages found by `git grep` (not a complete list):

| Call | Where | CGAL package |
|---|---|---|
| `corefine_and_compute_difference/union/intersection` | `MeshBoolean.cpp:443-455` | Polygon Mesh Processing (corefinement) |
| `isotropic_remeshing` | `MeshBoolean.cpp:339` | Polygon Mesh Processing (meshing) |
| `PMP::clip` | `CutSurface.cpp:2635` | Polygon Mesh Processing (corefinement) |
| `sdf_values`, `segmentation_from_sdf_values` | `MeshBoolean.cpp:495`, `:502` | Triangulated Surface Mesh Segmentation |
| `SMP::parameterize` with `LSCM_parameterizer_3` | `MeshBoolean.cpp:416-417` | **Surface Mesh Parameterization (new use in 2.5.0)** |

## 3. Package license of each included header

Each CGAL 6.2.1 header names its license in an `SPDX-License-Identifier` line. GPL-package headers also include `<CGAL/license/<Package>.h>`. This replaces the `package_info/<package>/license.txt` files that the 5.6.3 review cited: the release zip has a flat `include/` layout, and those files are not in it.

The 78 headers the application includes directly fall into two groups:

| SPDX in the header | Count | Packages (from `CGAL/license/…`) |
|---|---:|---|
| `GPL-3.0-or-later OR LicenseRef-Commercial` | 47 | AABB_tree, Arrangement_on_surface_2, Bounding_volumes, Box_intersection_d, Polygon_mesh_processing (corefinement, combinatorial_repair, geometric_repair, meshing_hole_filling, orientation, predicate, measure, connected_components, detect_features, Compute_normal, miscellaneous), Surface_mesh, Surface_mesh_parameterization, Surface_mesh_segmentation, Surface_sweep_2, TDS_2, Triangulation_2 |
| `LGPL-3.0-or-later OR LicenseRef-Commercial` | 31 | none named (kernel, number types, `boost/graph` helpers, `property_map`, `spatial_sort`, …) |

Headers from these packages are new in 2.5.0 (not included anywhere in v2.4.2): AABB_tree, Box_intersection_d, Surface_mesh_parameterization, and more Polygon Mesh Processing sub-packages. Triangulation_2 was already used by `Triangulation.cpp` in v2.4.2; `MeshRepair.cpp` adds more of it. **Surface_mesh** is a GPL package too, and every mesh path uses it. These counts are for directly included headers only. The full transitive header closure was not computed: that needs a compile (`-H` or `ninja -t deps`).

### 3.1 A segmentation header without the commercial option

Across all 3,756 files under `include/` in the archive:

| SPDX | Files |
|---|---:|
| `GPL-3.0-or-later OR LicenseRef-Commercial` | 2,241 |
| `LGPL-3.0-or-later OR LicenseRef-Commercial` | 1,405 |
| `LGPL-3.0-or-later` | 66 |
| `GPL-3.0-only` | 23 (all `CGAL/Qt/`) |
| `LicenseRef-RFL` | 6 (`Classification/ETHZ`) |
| `BSL-1.0` | 6 (Boost-derived, listed in `LICENSE`) |
| `(GPL-3.0-or-later OR LicenseRef-Commercial) AND MIT` | 4 (`Isosurfacing_3`) |
| no SPDX line | 3 (`Qt` resources, `license/gpl_package_list.txt`) |
| `CC0-1.0` | 1 |
| **`GPL-3.0-or-later`** only | **1**: `CGAL/Surface_mesh_segmentation/internal/auxiliary/graph.h` |

`graph.h` is Boykov and Kolmogorov's MAXFLOW 2.21. Its header says "Re-licensed for CGAL distribution to: GPL-3.0-or-later" and "Original license is: GPL-2.0-or-later". Unlike the rest of the package, it carries no `LicenseRef-Commercial` alternative.

How it is reached, from the headers:

1. `CGAL/Surface_mesh_segmentation/internal/Surface_mesh_segmentation.h:24-25` includes `CGAL/boost/graph/Alpha_expansion_MaxFlow_tag.h` unless `CGAL_DO_NOT_USE_BOYKOV_KOLMOGOROV_MAXFLOW_SOFTWARE` is defined. The same macro picks the default graph-cut tag (`:205-208`).
2. `Alpha_expansion_MaxFlow_tag.h:23` includes `graph.h`.
3. OrcaSlicer 2.5.0 does not define the macro: `git grep BOYKOV 665552c1 -- src cmake CMakeLists.txt deps` finds nothing. `MeshBoolean.cpp:53` and `TextureToColor/ColorUtils.cpp:39` include `CGAL/mesh_segmentation.h`, and `MeshBoolean.cpp:502` calls `segmentation_from_sdf_values`.

So, by reading the headers, the default segmentation path compiles a file that is GPL-3.0-or-later with no commercial alternative. This was **not confirmed by a compile**. Whether CGAL 5.6.3 had the same file and default was not checked here. Recorded, not concluded.

## 4. License files in the archive

| File | What it is |
|---|---|
| `LICENSE` | CGAL's overview. Each file states GPL or LGPL "either version 3 of the License or (at your option) any later version", with texts in `LICENSE.GPL` and `LICENSE.LGPL`. Four Boost-derived files are BSL-1.0. `include/CGAL/CORE` and `include/CGAL/ImageIO` are third-party LGPL code. `Classification/ETHZ` is MIT-like (`LICENSE.RFL`). Files without a copyright notice (examples, some demos) are CC0-1.0 |
| `LICENSE.GPL` / `LICENSE.LGPL` | GNU GPL v3 and GNU LGPL v3 texts |
| `LICENSE.BSL`, `LICENSE.RFL`, `LICENSE.COMMERCIAL` | Boost 1.0; the ETHZ random-forest notice (Stefan Walk, 2014); a pointer to GeometryFactory commercial licenses |
| `LICENSES/` | REUSE-style texts: BSL-1.0, CC0-1.0, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.1-only, LGPL-3.0-or-later, LicenseRef-Commercial, LicenseRef-RFL, MIT |
| `REUSE.toml` | Marks build files, docs, examples, demos, tests and similar as CC0-1.0 |

**What gets installed.** CGAL's `CMakeLists.txt:722-725` installs `AUTHORS`, `CHANGES.md`, `LICENSE`, `LICENSE.GPL` and `LICENSE.LGPL` into `CGAL_INSTALL_DOC_DIR` (default `CMAKE_INSTALL_DOCDIR`, `:616-619`). That puts them in the dependency prefix, not in the app. `LICENSE.BSL`, `LICENSE.RFL` and `LICENSES/` are not installed. In OrcaSlicer 2.5.0, `git grep` for `CGAL_INSTALL_DOC`, `share/doc` and `COPYING` across the root and `src/CMakeLists.txt`, `deps/` and `src/dev-utils` found **no step that copies CGAL's license texts into a shipped app**. This is the same as the 5.6.3 finding. No release artifact was inspected.

## 5. Changes from the 5.6.3 review

| Topic | 5.6.3 (v2.4.2) | 6.2.1 (2.5.0) |
|---|---|---|
| Pin | `5d577acb…`, tag commit `3654f780` | `eebd737d…`, tag commit `28811b67` |
| `find_package` | no version | `CGAL 6.2` minimum |
| Where package licenses are stated | `package_info/*/license.txt` in the source tree | SPDX lines in every header. No `package_info/` in the release zip |
| GPL packages called | Polygon Mesh Processing, Surface Mesh Segmentation | the same, plus Surface Mesh Parameterization (LSCM), AABB tree and Box intersection (new includes) |
| GPL-only file (no commercial option) | not examined | `graph.h` (MAXFLOW) on the default segmentation path (§3.1) |
| License texts in the shipped app | no copy step found | no copy step found |

## 6. Open questions

1. Is the effective CGAL on every platform this pinned 6.2.1? A system 6.2.x would satisfy `find_package`. Needs configure logs.
2. The full header closure per translation unit was not computed, so the package list in §3 is a lower bound.
3. §3.1: does a real build compile `graph.h`? And was it already on the 5.6.3 path?
4. CGAL's GPL/LGPL texts, the BSL and RFL notices are not staged into any app package by the build files read here.
5. How these packages combine with OrcaSlicer's AGPL and with MCUT/libigl is a legal question. It is not answered here.

## 7. Approval

**Not approved.** This records what the archive, its license files and the OrcaSlicer build files say. A maintainer sign-off is still needed.
