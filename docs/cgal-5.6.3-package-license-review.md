# CGAL 5.6.3 package-license review — mesh boolean path

**Status:** Exact bundled release archive and active GPL-package API use identified; effective provider and full header closure remain configuration-dependent. This is a source-level provenance review, not a legal determination.  
**Reviewed OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (v2.4.2)

## 1. Executive findings

- The dependency recipe `deps/CGAL/CGAL.cmake` downloads the official **CGAL 5.6.3** release archive, `CGAL-5.6.3.zip`, and pins it with SHA-256 `5d577acb4a9918ccb960491482da7a3838f8d363aff47e14d703f19fd84733d4`. The recipe also retains a commented Git tag/commit reference (`3654f780ae0c64675cabaef0e5ddaf904c48b4b7`, `releases/CGAL-5.6.3`).
- The application does not constrain `find_package(CGAL REQUIRED)` to a version. The dependency build normally installs the pinned archive into the generated dependency prefix, but the effective CGAL provider must be verified from each actual configure/build. A caller-supplied prefix or package environment can affect CMake discovery.
- The active application source uses APIs from two CGAL packages whose CGAL 5.6 documentation classifies them as **GPL**:
  - **Polygon Mesh Processing**: `corefine_and_compute_difference`, `corefine_and_compute_union`, `corefine_and_compute_intersection`, and the other directly included polygon-mesh-processing headers.
  - **Triangulated Surface Mesh Segmentation**: `sdf_values` and `segmentation_from_sdf_values`.
- The same source uses the **2D and 3D Linear Geometry Kernel** (including `Exact_predicates_exact_constructions_kernel` and `Exact_predicates_inexact_constructions_kernel`), which CGAL 5.6.3 documents as **LGPL**. CGAL is not governed by one uniform license: package and file notices matter.
- This confirms the CGAL package-level GPL licensing is not merely a theoretical concern or an inference from the directory name. The relevant GPL package APIs are called by the compiled `libslic3r_cgal` target. The exact source/header closure, effective package provider, and distribution model still need build evidence and qualified review.

## 2. Exact dependency recipe and provider selection

At the reviewed OrcaSlicer commit:

- `deps/CGAL/CGAL.cmake` declares the official release archive URL `https://github.com/CGAL/cgal/releases/download/v5.6.3/CGAL-5.6.3.zip` and the SHA-256 above.
- The dependency orchestration includes `CGAL/CGAL.cmake` after Boost, Eigen, GMP, and MPFR, and includes `dep_CGAL` in the aggregate dependency target.
- `src/libslic3r/CMakeLists.txt` executes `find_package(CGAL REQUIRED)` without a requested version and links `CGAL::CGAL` privately into `libslic3r_cgal`.
- The generated dependency prefix is normally added to `CMAKE_PREFIX_PATH`, but the top-level project also supports a caller-supplied prefix. Source inspection alone cannot establish which CGAL package was selected by a particular build.

Pinned source evidence:

- [CGAL dependency recipe at the reviewed OrcaSlicer commit](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps/CGAL/CGAL.cmake)
- [Dependency orchestration](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps/CMakeLists.txt)
- [Application CGAL discovery and target linkage](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/CMakeLists.txt)

## 3. Confirmed application APIs and package-level license evidence

### 3.1 Polygon Mesh Processing — GPL

`src/libslic3r/MeshBoolean.cpp` includes:

- `CGAL/Polygon_mesh_processing/corefinement.h`
- `CGAL/Polygon_mesh_processing/orient_polygon_soup.h`
- `CGAL/Polygon_mesh_processing/repair.h`
- `CGAL/Polygon_mesh_processing/remesh.h`
- `CGAL/Polygon_mesh_processing/repair_polygon_soup.h`
- `CGAL/Polygon_mesh_processing/orientation.h`

The same translation unit calls:

- `corefine_and_compute_difference`
- `corefine_and_compute_union`
- `corefine_and_compute_intersection`
- `does_self_intersect`
- `orient_polygon_soup`, `orient_to_bound_a_volume`, polygon-soup conversion and repair routines, remeshing, hole-repair and related functions.

CGAL's 5.6.3 reference manual classifies the **Polygon Mesh Processing** package as **GPL** and explicitly lists the three `corefine_and_compute_*` boolean functions. This is a package-level classification for the functions actively used here, not a conclusion inferred from the word `copyleft` in the libigl namespace.

Sources:

- [CGAL 5.6.3 Polygon Mesh Processing reference — GPL package and Boolean Operations API](https://doc.cgal.org/5.6.3/Polygon_mesh_processing/group__PkgPolygonMeshProcessingRef.html)
- [CGAL 5.6.3 Polygon Mesh Processing manual](https://doc.cgal.org/5.6.3/Polygon_mesh_processing/index.html)
- [OrcaSlicer MeshBoolean.cpp at the reviewed commit](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/MeshBoolean.cpp)

### 3.2 Triangulated Surface Mesh Segmentation — GPL

The same application file includes `CGAL/mesh_segmentation.h` and calls:

- `CGAL::sdf_values`
- `CGAL::segmentation_from_sdf_values`

CGAL's 5.6 package reference identifies **Triangulated Surface Mesh Segmentation** as **GPL** and documents these exact functions. The dependency page for this package also identifies 3D Fast Intersection and Distance Computation as a dependency; its exact instantiated header closure should be checked against the selected CGAL archive.

Sources:

- [CGAL 5.6 Triangulated Surface Mesh Segmentation reference — GPL package and functions](https://doc.cgal.org/5.6/Surface_mesh_segmentation/group__PkgSurfaceMeshSegmentationRef.html)
- [OrcaSlicer MeshBoolean.cpp at the reviewed commit](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/MeshBoolean.cpp)

### 3.3 Linear Geometry Kernel — LGPL

The application and libigl implementation use CGAL kernel types, including exact-predicate/exact-construction and exact-predicate/inexact-construction kernels, as well as kernel conversion facilities. CGAL 5.6.3 classifies the **2D and 3D Linear Geometry Kernel** package as **LGPL**.

This is an important counterexample to treating all CGAL code as GPL. The exact license of each included CGAL file remains determined by its source notice and package documentation.

Source:

- [CGAL 5.6.3 Kernel 23 reference — LGPL package](https://doc.cgal.org/5.6.3/Kernel_23/group__PkgKernel23Ref.html)

## 4. CGAL's own license model

CGAL's licensing documentation describes a dual model: packages are offered under the open-source GPL/LGPL terms or under commercial licenses. It explains that foundational packages are generally LGPL while higher-level algorithms are generally GPL, with exceptions, and directs users to the exact source-file notices and package overview for the formal result.

Accordingly:

- Do not label the complete CGAL distribution simply `GPL` or simply `LGPL`.
- Do not infer a commercial license from the existence of a commercial licensing option.
- Preserve the notices from the actual selected CGAL distribution and the package/file-level license evidence.
- The CGAL manual states the open-source GPL/LGPL model is version 3 or later for the relevant license families; confirm the exact license files included in the downloaded 5.6.3 archive before recording SPDX expressions.

Sources:

- [CGAL official license explanation](https://www.cgal.org/license.html)
- [CGAL 5.6.3 installation manual](https://doc.cgal.org/5.6.3/Manual/installation.html)

## 5. Scope, remaining evidence, and limitations

This review establishes the dependency recipe's pinned archive and the active use of GPL-classified CGAL packages. It does **not** establish:

1. Which CGAL provider was selected in every supported build (bundled archive, system package, or caller-provided prefix).
2. The exact package/file closure after preprocessing, templates, transitive includes, and platform-specific compile conditions.
3. Whether all required CGAL license texts and third-party notices are preserved in each produced package.
4. The exact license terms of every CGAL header reached by the call path; package-level documentation is a strong locator, not a replacement for source-file notices.
5. The final legal characterization of the combined application, MCUT, libigl, and CGAL distribution.

The next technical evidence should come from clean supported builds: capture `CGAL_DIR`, `CGAL_VERSION`, selected config-file path, compile commands, dependency target graph, and packaged license notices for Linux, Windows, and macOS. If a system CGAL is intentionally supported, record its package/version and license provenance as a separate provider path.

**Conclusion:** CGAL is not just a hypothetical unresolved dependency in the libigl review. The pinned default dependency recipe is CGAL 5.6.3, and the application directly invokes CGAL APIs from both the GPL Polygon Mesh Processing package and the GPL Triangulated Surface Mesh Segmentation package, while also using LGPL kernel facilities. This is a concrete provenance and distribution-review gate. No source code was imported or modified, no commercial CGAL license was assumed, and no legal compatibility conclusion is made.
