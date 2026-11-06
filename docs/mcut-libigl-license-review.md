# MCUT and libigl copyleft source review — OrcaSlicer v2.4.2

**Status:** Targeted source-level license review; not legal advice or a complete transitive-license determination  
**Reviewed upstream revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**Method:** Fixed-revision GitHub source inspection of the vendored files and the application call/link path. No local configure, build, binary inspection, or legal review was performed.

## 1. Executive findings

- **MCUT is an active dependency, not merely an unused vendored directory.** `src/libslic3r/MeshBoolean.cpp` includes the MCUT API and contains the mesh-boolean implementation calls. `src/libslic3r/CMakeLists.txt` links `mcut` into `libslic3r_cgal`.
- The vendored MCUT `CMakeLists.txt` explicitly says its default license is **GPL-3.0-or-later** and that a commercial license can be purchased. Its `LICENSE.GPL.txt` contains the GPL version 3 text. The checked-in files do not establish that OrcaSlicer has obtained a commercial license.
- MCUT's internal CDT component carries an MPL-2.0 notice and is actively included by `frontend.cpp`. MCUT's own `LICENSE.txt` says CDT files were dual-licensed under MPL-2.0 and GPL. Preserve both layers; do not label all MCUT content with a single SPDX identifier based only on the parent notice. The MCUT v1.2.0 upstream tag is now substantially pinned by blob comparisons, with local changes in CMake, `math.cpp`, and `shewchuk.c` documented in [the source-closure follow-up](mcut-libigl-transitive-closure-review.md).
- OrcaSlicer's application code directly calls `igl::copyleft::cgal::mesh_boolean`. The exact `mesh_boolean.h` and `mesh_boolean.cpp` files both carry MPL-2.0 notices. However, libigl's copyleft README warns that the namespace contains code under more aggressive copyleft, including GPL. Other files in the same subtree have different license headers (including GPL and LGPL examples). A directory-level label is not enough to decide the license of the exact transitive source closure.
- The reviewed `mesh_boolean.cpp` implementation uses CGAL headers. CGAL's own license and the exact selected CGAL package/build configuration remain a separate review item.
- These findings do **not** establish that GPL-3.0-or-later MCUT is incompatible with an AGPLv3 project. They establish that MCUT's GPL obligations, its nested component notices, and the exact combined distribution model must be explicitly accounted for. No license compatibility conclusion is made here.

## 2. MCUT: active use and license evidence

### 2.1 Source and license declarations

At the pinned OrcaSlicer revision:

- `deps_src/mcut/CMakeLists.txt` begins with a copyright notice for Floyd M. Chitalu and states: "This file is licensed under GPL-3.0-or-later (default)." It also identifies a commercial-license option.
- `deps_src/mcut/LICENSE.txt` describes two mutually exclusive licensing options: the open-source GPL and a commercial license. It also identifies the bundled CDT code and says those files were dual-licensed under MPL-2.0 and GPL.
- `deps_src/mcut/LICENSE.GPL.txt` contains the GNU GPL version 3 text.
- `deps_src/mcut/include/mcut/internal/cdt/LICENSE.txt` contains the Mozilla Public License 2.0 text.

The README uses the generic term "GPL"; the CMake file is the clearest version-specific declaration in this pinned tree. The presence of a commercial option is not evidence that the project has purchased or received that license.

### 2.2 Confirmed application use

The following source references establish that MCUT is in the application dependency path:

1. `src/libslic3r/MeshBoolean.cpp` includes `mcut/include/mcut/mcut.h`.
2. The same file contains MCUT mesh conversion and boolean execution code, including calls through the MCUT API.
3. `src/libslic3r/CMakeLists.txt` links `mcut` privately into `libslic3r_cgal`.
4. The same CMake file links `libslic3r_cgal` into `libslic3r`.

The vendored MCUT CMake option `MCUT_BUILD_AS_SHARED_LIB` defaults to `OFF`, and the target is created as a static library in that configuration. This is the declared source-build default; the actual generated build configuration has not been inspected.

### 2.3 Conditional network fetches

MCUT's CMake contains `FetchContent` logic for libigl and Eigen inside a condition requiring `MCUT_BUILD_TESTS` or `MCUT_BUILD_TUTORIALS`. The CMake file only creates the default-ON test/tutorial options when MCUT is the top-level project. In OrcaSlicer it is added as a subdirectory, so that standalone-project branch is not taken.

This source inspection suggests those optional test/tutorial fetches are not part of the ordinary parent-project configuration unless the options are set elsewhere. A real CMake configure with the supported build presets is still required to confirm the effective behavior.

## 3. libigl: actual copyleft API use and per-file notices

### 3.1 Application call path

At the pinned revision, `src/libslic3r/MeshBoolean.cpp`:

- includes `<igl/copyleft/cgal/mesh_boolean.h>`;
- calls `igl::copyleft::cgal::mesh_boolean` for mesh subtraction; and
- calls it again for self-union.

The `libslic3r_cgal` target links the CGAL target, admesh, libigl, and MCUT. The bundled `deps_src/libigl/CMakeLists.txt` creates an INTERFACE target and exposes the vendored include tree when a system libigl package is not found.

The `mesh_boolean.h` header includes `mesh_boolean.cpp` unless `IGL_STATIC_LIBRARY` is defined. The exact build's compile definitions have not been resolved here, so this review does not claim which translation unit receives every implementation body.

### 3.2 Per-file license evidence

- `deps_src/libigl/igl/copyleft/README.md` says the copyleft namespace is under more aggressive copyleft than the MPL-2.0 used by the main libigl namespace, and that it includes GPL code. It also says obtaining licenses for the dependencies used allows use under MPL-2.0; the precise intended scope of that statement needs upstream clarification if relied upon.
- The exact `igl/copyleft/cgal/mesh_boolean.h` and `mesh_boolean.cpp` files each contain an MPL-2.0 notice.
- As examples of why a directory-wide label is insufficient, `igl/copyleft/quadprog.cpp` contains a GPL version 2-or-later notice, while `igl/copyleft/marching_cubes.cpp` contains an LGPL version 2 notice. Their adjacent headers carry different MPL-2.0 notices. These files were inspected as examples in the tree; this review did not find evidence that OrcaSlicer's reviewed mesh-boolean call path uses them.
- The CGAL implementation includes CGAL headers. CGAL's licensing, including the exact components and configuration selected by the build, must be reviewed independently.

### 3.3 What remains unresolved

- Determine the complete transitive source/include closure for `igl::copyleft::cgal::mesh_boolean` in every supported build configuration.
- Identify whether any included or instantiated file in that closure is GPL/LGPL or subject to additional third-party terms, rather than relying on the namespace name or the README alone.
- Resolve the CGAL license for the exact package/version and distribution configuration.
- Confirm whether a system libigl package can replace the vendored tree, and whether that changes the effective license/source set.
- Check the exact use and distribution of MCUT and libigl in produced binaries, including static-linking and source-correspondence obligations.

## 4. Fixed-revision evidence

All links below point to OrcaSlicer commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`.

| Evidence | Upstream file |
|---|---|
| MCUT license declaration and build options | [`deps_src/mcut/CMakeLists.txt`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/mcut/CMakeLists.txt) |
| MCUT dual-license summary | [`deps_src/mcut/LICENSE.txt`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/mcut/LICENSE.txt) |
| MCUT GPL text | [`deps_src/mcut/LICENSE.GPL.txt`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/mcut/LICENSE.GPL.txt) |
| Nested CDT MPL notice | [`deps_src/mcut/include/mcut/internal/cdt/LICENSE.txt`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/mcut/include/mcut/internal/cdt/LICENSE.txt) |
| MCUT application use | [`src/libslic3r/MeshBoolean.cpp`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/MeshBoolean.cpp) |
| Application target linkage | [`src/libslic3r/CMakeLists.txt`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/CMakeLists.txt) |
| libigl copyleft scope note | [`deps_src/libigl/igl/copyleft/README.md`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/libigl/igl/copyleft/README.md) |
| Used libigl mesh-boolean header | [`deps_src/libigl/igl/copyleft/cgal/mesh_boolean.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/libigl/igl/copyleft/cgal/mesh_boolean.h) |
| Used libigl mesh-boolean implementation | [`deps_src/libigl/igl/copyleft/cgal/mesh_boolean.cpp`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/libigl/igl/copyleft/cgal/mesh_boolean.cpp) |
| libigl interface target | [`deps_src/libigl/CMakeLists.txt`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/libigl/CMakeLists.txt) |

## 5. Required follow-up

1. Preserve MCUT's GPL and CDT license notices if this code is retained; do not assume the commercial license option applies to this project.
2. Decide whether MCUT remains in the architecture. If retained, document the intended AGPL/GPL distribution model and obtain qualified legal review of the combined work and corresponding-source obligations.
3. Trace the full libigl/CGAL source and license closure for the exact functions actually used. Record each file and its notice; resolve any inconsistent or ambiguous file/header notices with upstream maintainers or counsel.
4. Configure the fixed upstream revision using the actual supported build presets and record the effective MCUT test/tutorial options, libigl provider, CGAL provider, compile definitions, linked targets, and packaged artifacts.
5. Add the resolved component/file-level results to the eventual SBOM and third-party notices.

**Conclusion:** MCUT is confirmed to be actively linked and carries an explicit GPL-3.0-or-later default license declaration. Its upstream v1.2.0 identity is substantially established, with three local file deltas requiring provenance review; the CDT component and modified Shewchuk predicates are also active. OrcaSlicer actively calls a libigl copyleft-namespace API whose entry-point files declare MPL-2.0, while the first-level closure includes several files without visible notices and the exact libigl source revision is not pinned. Neither issue can be resolved by a directory-name heuristic. See [MCUT/libigl source-closure follow-up](mcut-libigl-transitive-closure-review.md). No legal compatibility conclusion, dependency approval, source import, or build validation is claimed.
