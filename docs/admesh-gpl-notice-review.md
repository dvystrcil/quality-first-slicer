# ADMesh GPL notice, exception, and integration review

**Status:** Per-file GPL notices verified; full license text and contributor-list preservation are incomplete in the vendored subset  
**Reviewed OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (v2.4.2)  
**Upstream comparison snapshot:** `admesh/admesh` commit `e1b296b575ba574cc91480587a9876a36bbe2c0d`; its README identifies the 0.98.5 release  
**Scope:** The seven files in OrcaSlicer's `deps_src/admesh/CMakeLists.txt`, their license headers, upstream COPYING/README, and application build/use references

## 1. Executive findings

The six compiled implementation files and public header in OrcaSlicer's ADMesh target all carry the same complete short-form notice:

- Copyright (C) 1995, 1996 Anthony D. Martin.
- Copyright (C) 2013, 2014 several contributors, with a pointer to `AUTHORS`.
- GNU General Public License, version 2 **or, at the recipient's option, any later version**.
- Standard no-warranty disclaimer and a statement that a copy of the GPL should accompany the program.

This is **GPL-2.0-or-later**, not GPL-2.0-only. The vendored `deps_src/admesh` directory does not contain the full `COPYING` license text or an `AUTHORS` file. The pinned upstream comparison snapshot has a `COPYING` file containing the complete GPL version 2 text, but no root `AUTHORS` file was found at that snapshot either. Its README states that ADMesh is distributed under the GPL and points readers to `COPYING`.

No ADMesh-specific linking exception or additional permission was found in the inspected source headers, README, COPYING text, or build files. The word “exception” occurs in the standard GPLv2 text; it is not a special ADMesh linking exception. In particular, there is no notice authorizing linking ADMesh with proprietary or otherwise GPL-incompatible code.

**Distribution blocker:** preserve the complete GPL text with the ADMesh source and include the applicable license and attribution information in the project's third-party notices. Do not remove or rewrite the existing per-file copyright/license headers. Resolve the `AUTHORS` pointer with reliable attribution evidence; do not fabricate an AUTHORS file.

## 2. Vendored file and notice audit

The ADMesh CMake target contains exactly these seven listed source/header files:

| Vendored file | Git blob SHA | Header result |
|---|---|---|
| `stl.h` | `0f1a0cec88a697f6136743a56c1b243637086a29` | Full ADMesh copyright and GPL-2-or-later notice present |
| `connect.cpp` | `30a199120d141d2215dcef4eb10d9cebd7dd23b8` | Same notice present |
| `normals.cpp` | `f74ba01b6da449569c093dd540bd730b34c89f46` | Same notice present |
| `shared.cpp` | `a8fbc2a87db1760b913e47695c51aa3384614c05` | Same notice present |
| `stl_io.cpp` | `221572bca63e9be34ebe192bbacd4e325c29c9a9` | Same notice present |
| `stlinit.cpp` | `a69bd5497aa6b1a8001d32d91303635a0eaf061f` | Same notice present |
| `util.cpp` | `037a0a04da6f0f19bc4decdf385220c1cd30dea4` | Same notice present |

The vendored CMake file builds the six implementation files into a static `admesh` target. The directory has no `COPYING`, `LICENSE`, or `AUTHORS` file at the reviewed revision. The `stl.h` notice itself explicitly says a GPL copy should accompany the program and refers to the contributor list.

Fixed OrcaSlicer references:

- [ADMesh CMake target](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/admesh/CMakeLists.txt)
- [ADMesh public header](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/admesh/stl.h)
- [connect.cpp](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/admesh/connect.cpp)
- [normals.cpp](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/admesh/normals.cpp)
- [shared.cpp](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/admesh/shared.cpp)
- [stl_io.cpp](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/admesh/stl_io.cpp)
- [stlinit.cpp](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/admesh/stlinit.cpp)
- [util.cpp](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/admesh/util.cpp)

## 3. Upstream license and attribution evidence

At upstream commit `e1b296b575ba574cc91480587a9876a36bbe2c0d`:

- `README.md` identifies the 0.98.5 release tarball and states that ADMesh is copyrighted software distributed under the GNU GPL, with details in `COPYING`.
- `COPYING` is the complete GNU GPL version 2 text (blob SHA `d159169d1050894d3ea3b98e1c965c4058208fe1`).
- `src/stl.h` and all six upstream implementation files inspected carry the same GPL-2-or-later notice found in the vendored files.
- The source notice refers to “several contributors, see AUTHORS”; a root `AUTHORS` file was not found at this pinned repository snapshot. The vendored subset also omits it.

The copyright lines in the source identify Anthony D. Martin and a group of 2013–2014 contributors. As supplementary attribution evidence, Debian's ADMesh 0.98.5 package copyright metadata names Anthony D. Martin, Andy Doucette, Anton Gladky, Alessandro Ranellucci, Guillaume Seguin, Miro Hrončok, and Tomas Chvatal. This is downstream packaging metadata, not a replacement for an upstream `AUTHORS` file or proof that this list exhausts every contributor.

Pinned upstream references:

- [Upstream 0.98.5 README](https://github.com/admesh/admesh/blob/e1b296b575ba574cc91480587a9876a36bbe2c0d/README.md)
- [Upstream GPLv2 COPYING](https://github.com/admesh/admesh/blob/e1b296b575ba574cc91480587a9876a36bbe2c0d/COPYING)
- [Upstream stl.h notice](https://github.com/admesh/admesh/blob/e1b296b575ba574cc91480587a9876a36bbe2c0d/src/stl.h)
- [Debian ADMesh 0.98.5 copyright metadata](https://sources.debian.org/src/admesh/0.98.5-1/debian/copyright/)

## 4. Exception review and GPL version implications

The source notice explicitly permits use under GPL version 2 **or any later version**. This later-version clause is part of the license grant; it is not a linking exception.

The upstream `COPYING` file is the standard GPLv2 text. A search of the inspected upstream repository for “special exception” and “linking exception” surfaced only ordinary GPLv2 text, including its standard treatment of system libraries and its discussion of the LGPL as an alternative for library authors. No ADMesh-specific exception or additional linking permission was found. The ADMesh README likewise describes the program as GPL-distributed and does not state a separate exception.

The GPL-2.0-or-later grant allows recipients to choose GPLv3 for the ADMesh code. The Free Software Foundation explains that GPL-2-or-later code can be combined with GPLv3 code by choosing GPLv3, and that GPLv3 and AGPLv3 modules may be linked/combined under the express compatibility provisions in those licenses. This is relevant to the project's AGPLv3 licensing context, but it is not a complete legal conclusion about the application, its other dependencies, or any particular binary distribution.

References:

- [FSF GPL FAQ: GPLv2-or-later and GPLv3 compatibility](https://www.gnu.org/licenses/identify-licenses-clearly.html)
- [FSF GPL FAQ: GPLv3 and AGPLv3 linking compatibility](https://www.gnu.org/licenses/gpl-faq.html.en)

## 5. Actual use and local adaptation

ADMesh is actively used, not merely present in the dependency tree:

- `deps_src/admesh/CMakeLists.txt` builds the static `admesh` target.
- `src/libslic3r/CMakeLists.txt` links `admesh` publicly into `libslic3r` and privately into `libslic3r_cgal`.
- `src/libslic3r/TriangleMesh.cpp` includes and calls ADMesh operations including `stl_open`, `stl_check_facets_exact`, `stl_check_facets_nearby`, `stl_remove_unconnected_facets`, `stl_fill_holes`, `stl_fix_normal_directions`, `stl_fix_normal_values`, and `stl_calculate_volume`.

The OrcaSlicer copy is adapted: implementation files use `.cpp` names, and the public `stl.h` has a C++/Eigen-oriented data model and APIs that differ from the upstream C header. The license headers are preserved, but this review does not constitute a complete source diff or patch-lineage analysis. The precise set of local modifications and their dates should remain a separate provenance task.

## 6. Required follow-up

1. Restore the complete upstream GPLv2 `COPYING` text to the vendored component or otherwise ensure the complete applicable GPL text accompanies source and binary distributions.
2. Ensure third-party notices preserve the Anthony D. Martin and 2013–2014 contributor notices from the source headers.
3. Resolve the `AUTHORS` reference using reliable upstream or rights-holder evidence. Debian's copyright metadata is useful corroboration but should not be silently substituted as an upstream file.
4. Trace the complete OrcaSlicer C++/Eigen adaptation against the selected upstream snapshot and record the source revision, changed files, and modification provenance.
5. Confirm release packaging includes the full license text and attribution notices. This review did not inspect actual built packages.
6. Have qualified counsel review the complete dependency/license set and distribution model before making a project-wide compatibility determination.

Until packaging is checked, record the status as **GPL-2.0-or-later source headers preserved; full GPL text absent from vendored subset; no ADMesh-specific linking exception found; package notice delivery unverified**.

## 7. Scope and limitations

Documentation-only review. No ADMesh source or license text was imported, no source header was changed, no exception was added or inferred, no build or binary/package inspection was performed, and no legal determination was made.
