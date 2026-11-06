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

## 5. Build and package notice propagation — static workflow review

This section reviews the build and packaging configuration at the same pinned OrcaSlicer revision. It is static source inspection; no platform build artifact was downloaded or unpacked.

### 5.1 What CGAL's own install target provides

The matching CGAL source commit is `3654f780ae0c64675cabaef0e5ddaf904c48b4b7` (`releases/CGAL-5.6.3`). Its `Installation/CMakeLists.txt`:

- Uses `GNUInstallDirs` and sets the documentation destination from `CMAKE_INSTALL_DOCDIR`.
- Installs `AUTHORS`, `CHANGES.md`, `LICENSE`, `LICENSE.GPL`, and `LICENSE.LGPL` into that documentation directory when documentation installation is enabled.
- Describes CGAL as a collection of parts whose individual source files specify GPL or LGPL licensing, and identifies the GPL/LGPL license texts as the corresponding license documents.
- The source archive also contains package-specific `package_info/<package>/license.txt` files, including GPL classifications for Polygon Mesh Processing and Surface Mesh Segmentation, and an LGPL classification for the Installation package. These package metadata files are not among the five files named by the generic installation rule above.

Pinned upstream evidence:

- [CGAL 5.6.3 Installation/CMakeLists.txt](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Installation/CMakeLists.txt)
- [CGAL 5.6.3 Installation/LICENSE](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Installation/LICENSE)
- [Polygon Mesh Processing package license metadata](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Polygon_mesh_processing/package_info/Polygon_mesh_processing/license.txt)
- [Surface Mesh Segmentation package license metadata](https://github.com/CGAL/cgal/blob/3654f780ae0c64675cabaef0e5ddaf904c48b4b7/Surface_mesh_segmentation/package_info/Surface_mesh_segmentation/license.txt)

### 5.2 OrcaSlicer packaging behavior

At the reviewed OrcaSlicer commit:

- The ordinary dependency build installs dependencies beneath the generated dependency prefix, normally `deps/build/OrcaSlicer_dep/usr/local`. The CGAL ExternalProject uses that dependency install prefix. CGAL's documentation/license files therefore have an install destination in the dependency tree; that is separate from the application install tree.
- The top-level application install rule explicitly installs only the repository's `LICENSE.txt` as its generic license file. That file is the OrcaSlicer AGPLv3 text, not CGAL's separate GPL/LGPL texts.
- Windows packaging invokes CPack NSIS. `CPACK_RESOURCE_FILE_LICENSE` points to the same root `LICENSE.txt`; the install rule also places that file in the application install tree. The workflow separately uploads a portable application folder.
- The Linux AppImage helper constructs its image from the application install tree and adds desktop/metainfo assets. It contains no explicit step to copy CGAL's dependency-prefix documentation directory into the AppImage.
- The macOS workflow archives the built `OrcaSlicer` app bundle and later creates a universal DMG. The inspected packaging script contains no explicit CGAL documentation-copy step.
- The Flatpak manifest is a meaningful distinction: its dependency build uses `/app` as the install prefix and does not remove documentation directories in its cleanup list; the application post-install step separately installs OrcaSlicer's AGPL `LICENSE.txt` under `/app/share/licenses/com.orcaslicer.OrcaSlicer/`. The manifest does not explicitly stage CGAL's package-specific metadata into that license directory.

These findings show that the build system knows how to install CGAL's GPL/LGPL texts into a dependency documentation directory, while the ordinary application packaging rules explicitly stage the OrcaSlicer AGPL text. They do **not** prove that a given released binary omits CGAL's texts: a platform's dependency layout, CMake install behavior, bundle assembly, or artifact contents could preserve additional files. No release artifact was inspected, and the Flatpak dependency prefix differs from the normal platform layout.

Pinned OrcaSlicer evidence:

- [Dependency install-prefix configuration](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps/CMakeLists.txt)
- [CGAL dependency recipe](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps/CGAL/CGAL.cmake)
- [Application install and CPack license configuration](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/CMakeLists.txt)
- [Windows/macOS/Linux build and packaging workflow](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdcc10b5099ac20d252af3a7c560046f1/.github/workflows/build_orca.yml)
- [Release artifact assembly workflow](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdcc10b5099ac20d252af3a7c560046f1/.github/workflows/publish_release.yml)
- [AppImage assembly helper](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdcc10b5099ac20d252af3a7c560046f1/src/dev-utils/platform/unix/build_appimage.sh.in)
- [Flatpak manifest](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdcc10b5099ac20d252af3a7c560046f1/scripts/flatpak/com.orcaslicer.OrcaSlicer.yml)

### 5.3 Required artifact-level verification

For each supported release platform, retain the actual build configuration and inspect the final distributable (not just the build directory):

1. Record the selected `CGAL_DIR`, `CGAL_VERSION`, and resolved package config path.
2. Record the CGAL dependency install destination and whether `LICENSE`, `LICENSE.GPL`, and `LICENSE.LGPL` are present there.
3. Inspect the final Windows installer and portable ZIP, macOS app/DMG, Linux AppImage, and Flatpak bundle for those files and any applicable third-party notices.
4. For Flatpak, separately verify whether `/app/share/doc/CGAL` survives the build and appears in the exported bundle.
5. Preserve file listings or archive manifests as repeatable evidence. Do not treat the root OrcaSlicer AGPL license as a substitute for the dependency's distinct license texts.

## 6. Scope, remaining evidence, and limitations

This review establishes the dependency recipe's pinned archive and the active use of GPL-classified CGAL packages. It does **not** establish:

1. Which CGAL provider was selected in every supported build (bundled archive, system package, or caller-provided prefix).
2. The exact package/file closure after preprocessing, templates, transitive includes, and platform-specific compile conditions.
3. Whether all required CGAL license texts and third-party notices are preserved in each produced package.
4. The exact license terms of every CGAL header reached by the call path; package-level documentation is a strong locator, not a replacement for source-file notices.
5. The final legal characterization of the combined application, MCUT, libigl, and CGAL distribution.

The next technical evidence should come from clean supported builds: capture `CGAL_DIR`, `CGAL_VERSION`, selected config-file path, compile commands, dependency target graph, and packaged license notices for Linux, Windows, and macOS. If a system CGAL is intentionally supported, record its package/version and license provenance as a separate provider path.

**Conclusion:** CGAL is not just a hypothetical unresolved dependency in the libigl review. The pinned default dependency recipe is CGAL 5.6.3, and the application directly invokes CGAL APIs from both the GPL Polygon Mesh Processing package and the GPL Triangulated Surface Mesh Segmentation package, while also using LGPL kernel facilities. This is a concrete provenance and distribution-review gate. No source code was imported or modified, no commercial CGAL license was assumed, and no legal compatibility conclusion is made.
