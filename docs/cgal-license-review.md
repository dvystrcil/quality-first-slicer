# CGAL license and application-use review — OrcaSlicer v2.4.2

**Status:** Targeted source/package-level review; not legal advice or a complete transitive-license determination  
**OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**CGAL release:** `v5.6.3`, tag commit `3654f780ae0c64675cabaef0e5ddaf904c48b4b7`  
**Method:** Fixed-revision source, CMake, and CGAL package metadata inspection. No local configure/build, binary inspection, or legal review.

## 1. Executive findings

- OrcaSlicer pins CGAL 5.6.3 using the release archive and SHA-256 in `deps/CGAL/CGAL.cmake`: `5d577acb4a9918ccb960491482da7a3838f8d363aff47e14d703f19fd84733d4`. The corresponding upstream Git tag resolves to commit `3654f780ae0c64675cabaef0e5ddaf904c48b4b7`.
- CGAL 5.6.3 does not have one blanket license. Its `Installation/LICENSE` says individual source files specify GPL or LGPL, version 3 or later, and separately identifies bundled third-party material. It also points to commercial licensing by component.
- OrcaSlicer directly includes headers from CGAL packages whose package metadata declares **GPL (v3 or later)**: Polygon Mesh Processing, Triangulation 2, Surface Mesh, Arrangement on Surface 2, and Surface Mesh Segmentation.
- The Kernel 23 package used by the application declares **LGPL (v3 or later)**.
- OrcaSlicer compiles CGAL-dependent geometry files into static target `libslic3r_cgal` and links `CGAL::CGAL` privately. This is an active application dependency, not an unused inventory item.
- These findings do not establish the legal outcome for an AGPLv3-derived application. Exact source/header closure, build configuration, distribution model, and any commercial permissions still require qualified review.

## 2. Exact pin and license model

At the pinned OrcaSlicer revision, `deps/CGAL/CGAL.cmake` selects:
- Release archive: `https://github.com/CGAL/cgal/releases/download/v5.6.3/CGAL-5.6.3.zip`
- SHA-256: `5d577acb4a9918ccb960491482da7a3838f8d363aff47e14d703f19fd84733d4`
- Git tag commit: `3654f780ae0c64675cabaef0e5ddaf904c48b4b7`
- Declared dependencies: Boost, Eigen, GMP, and MPFR.

CGAL's own `Installation/LICENSE` states that individual source files specify GPL or LGPL, each version 3 or later. It separately identifies Boost-derived files and bundled CORE, ImageIO, OpenNL, and ETH Zurich random-forest material. Therefore neither "CGAL is GPL" nor "CGAL is LGPL" is an adequate package-wide label.

## 3. Confirmed application use

At the pinned OrcaSlicer revision, `src/libslic3r/CMakeLists.txt` calls `find_package(CGAL REQUIRED)`, creates static target `libslic3r_cgal` from `CutSurface.cpp`, `IntersectionPoints.cpp`, `MeshBoolean.cpp`, `TryCatchSignal.cpp`, and `Triangulation.cpp`, links `CGAL::CGAL` privately, and then links `libslic3r_cgal` into `libslic3r`.

Direct CGAL header/package mapping from the application sources:

| OrcaSlicer source | CGAL headers / package evidence |
|---|---|
| `MeshBoolean.cpp` | `Polygon_mesh_processing/*`, `Surface_mesh.h`, `mesh_segmentation.h`, graph helpers; Polygon Mesh Processing, Surface Mesh, and Surface Mesh Segmentation package metadata declare GPL v3+ |
| `CutSurface.cpp` | `Polygon_mesh_processing/corefinement.h`, `clip.h`, `Surface_mesh.h`; Polygon Mesh Processing and Surface Mesh declare GPL v3+ |
| `Triangulation.cpp` | `Exact_predicates_inexact_constructions_kernel.h`, `Constrained_Delaunay_triangulation_2.h`, triangulation helpers; Kernel 23 declares LGPL v3+, Triangulation 2 declares GPL v3+ |
| `Geometry/VoronoiUtilsCgal.cpp` | `Exact_predicates_exact_constructions_kernel.h`, `Arr_segment_traits_2.h`, `Surface_sweep_2_algorithms.h`; Kernel 23 declares LGPL v3+, Arrangement on Surface 2 declares GPL v3+ |

Package classifications above are from CGAL 5.6.3's own `package_info/<package>/license.txt` files. This is a direct-include/package mapping, not a complete transitive include closure. Actual compile commands, instantiated templates, and platform-specific provider selection have not been inspected.

## 4. Relationship to libigl and MCUT

The [MCUT/libigl license review](mcut-libigl-license-review.md) established that OrcaSlicer calls `igl::copyleft::cgal::mesh_boolean`; the exact libigl entry-point files inspected declare MPL-2.0. The implementation directly includes `CGAL/Exact_predicates_exact_constructions_kernel.h`. OrcaSlicer also uses CGAL directly in its mesh boolean, cut-surface, triangulation, and Voronoi source files.

Resolving the libigl entry-point notice alone is therefore insufficient. CGAL's package licenses and transitive source/header closure must be evaluated independently. MCUT remains a separate active GPL-3.0-or-later default-license gate.

## 5. Fixed-revision evidence

OrcaSlicer links point to commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`; CGAL links point to tag commit `3654f780ae0c64675cabaef0e5ddaf904c48b4b7`.

| Evidence | Source |
|---|---|
| OrcaSlicer CGAL pin | [`deps/CGAL/CGAL.cmake`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps/CGAL/CGAL.cmake) |
| Application CGAL target/link | [`src/libslic3r/CMakeLists.txt`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/CMakeLists.txt) |
| Mesh boolean CGAL use | [`src/libslic3r/MeshBoolean.cpp`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/MeshBoolean.cpp) |
| Cut surface CGAL use | [`src/libslic3r/CutSurface.cpp`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/CutSurface.cpp) |
| Triangulation CGAL use | [`src/libslic3r/Triangulation.cpp`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/Triangulation.cpp) |
| Voronoi CGAL use | [`src/libslic3r/Geometry/VoronoiUtilsCgal.cpp`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/Geometry/VoronoiUtilsCgal.cpp) |
| CGAL license model | [`Installation/LICENSE`](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Installation/LICENSE) |
| CGAL commercial option notice | [`Installation/LICENSE.COMMERCIAL`](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Installation/LICENSE.COMMERCIAL) |
| Kernel 23 license | [`Kernel_23/package_info/Kernel_23/license.txt`](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Kernel_23/package_info/Kernel_23/license.txt) |
| Polygon Mesh Processing license | [`Polygon_mesh_processing/package_info/Polygon_mesh_processing/license.txt`](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Polygon_mesh_processing/package_info/Polygon_mesh_processing/license.txt) |
| Triangulation 2 license | [`Triangulation_2/package_info/Triangulation_2/license.txt`](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Triangulation_2/package_info/Triangulation_2/license.txt) |
| Arrangement on Surface 2 license | [`Arrangement_on_surface_2/package_info/Arrangement_on_surface_2/license.txt`](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Arrangement_on_surface_2/package_info/Arrangement_on_surface_2/license.txt) |
| Surface Mesh license | [`Surface_mesh/package_info/Surface_mesh/license.txt`](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Surface_mesh/package_info/Surface_mesh/license.txt) |
| Surface Mesh Segmentation license | [`Surface_mesh_segmentation/package_info/Surface_mesh_segmentation/license.txt`](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Surface_mesh_segmentation/package_info/Surface_mesh_segmentation/license.txt) |

## 6. Required follow-up

1. Resolve the complete CGAL include/instantiation closure for each OrcaSlicer translation unit and record file-level notices, including separately licensed third-party files.
2. Verify actual CGAL package selection and configuration from compile commands for each supported platform.
3. Determine whether any applicable CGAL commercial permissions exist; do not infer this from the upstream commercial option.
4. Assess combined distribution and source-correspondence obligations for selected CGAL GPL/LGPL components alongside the intended AGPLv3 licensing and MCUT's GPL-3.0-or-later default.
5. Include the exact CGAL package set, source pin, archive hash, and notices in the eventual SBOM and third-party notices.
6. Obtain qualified legal review before source import, binary redistribution, or offering the future network service.

**Conclusion:** CGAL is actively used, and application sources directly include headers from CGAL 5.6.3 packages whose metadata declares GPL-3.0-or-later as well as LGPL-3.0-or-later packages. The complete source closure and legal effect remain open. No compatibility conclusion, dependency approval, local build validation, or legal opinion is claimed.
