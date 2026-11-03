# OrcaSlicer baseline and source inventory

**Status:** Preliminary engineering inventory; baseline candidate only  
**Review date:** 2026-11-03  
**Upstream:** [OrcaSlicer/OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer)  
**No upstream source has been imported into this repository.**

## 1. Baseline candidate

The latest stable GitHub release observed during this review is **OrcaSlicer v2.4.2**, published 2026-07-07:

- Release: https://github.com/OrcaSlicer/OrcaSlicer/releases/tag/v2.4.2
- Tag: `v2.4.2`
- Tag target commit: `8500fcdccaa10b5099ac20d252af3a7c560046f1`
- License file at the tag: `LICENSE.txt`, blob `dba13ed2ddf783ee8118c6a581dbf75305f816a3`

The tag reference resolves directly to a commit, not an annotated tag object. The exact commit is therefore the reproducible source identity; the tag name alone is not sufficient for future provenance.

The current upstream `main` was also inspected and is ahead of the release line: its `version.inc` identifies itself as `2.5.0-dev`. The current `main` commit observed during this review was `8cdc68a6a042448622edac88199dece40246c647`. Do not silently substitute this moving development branch for the release candidate.

**Recommendation:** Use v2.4.2 / `8500fcdccaa10b5099ac20d252af3a7c560046f1` as the *initial baseline candidate* for the reproducible build investigation. This is not yet an approved fork pin. Before adoption, compare the release with current development and confirm that the release is suitable for the project's desired starting point. If a newer release appears before source import, repeat this comparison rather than automatically following `main`.

## 2. Repository structure observed at v2.4.2

The following high-level directories were confirmed from the tag's GitHub tree:

| Area | Observed contents | Review significance |
|---|---|---|
| `src/libslic3r` | Core slicing/library code | Main slicing engine; file-level notices and provenance required |
| `src/slic3r` | GUI/application code | UI and application integration |
| `src/libvgcode` | G-code visualization library | Separate source/license inventory required |
| `deps/` | CMake-managed external dependency projects | Build downloads, versions, patches, and licenses must be traced |
| `deps_src/` | Vendored source libraries | Individual upstream origins, versions, and licenses required |
| `resources/printers`, `resources/profiles`, `resources/profiles_template` | Printer and profile data | Treat as a distinct data/provenance and rights audit |
| `resources/fonts`, `resources/images`, `resources/i18n`, `resources/web` | Fonts, images, translations, web assets | Asset-specific notices and licenses required |
| `resources/calib`, `resources/handy_models`, `resources/flush` | Calibration and model-related assets | Inspect independently; do not assume source-code license |
| `tests/` | Catch2, test data, and test suites | Test framework and fixtures have their own provenance |
| `cmake/`, build scripts, packaging files | Build and distribution logic | Inspect downloaded artifacts, redistribution, and platform-specific components |

This is a top-level map, not a complete inventory of every file.

## 3. Dependency topology observed

At v2.4.2, `deps/CMakeLists.txt` describes a CMake ExternalProject-based dependency build. Its dependency source projects include directories for:

- Blosc, Boost, CGAL, CURL, Cereal, Draco, EXPAT, Eigen, FreeType, GLEW, GLFW, GMP, JPEG, MPFR, NLopt, NanoSVG, OCCT, OpenCSG, OpenCV, OpenEXR, OpenSSL, OpenVDB, PNG, Qhull, TBB, WebView2, ZLIB, libnoise, and wxWidgets.
- Platform-specific dependency scripts exist for Linux, macOS, MinGW, Unix-common, and Windows.

At the same tag, `deps_src/CMakeLists.txt` includes vendored projects for:

- Shiny, admesh, agg, ankerl, clipper, clipper2, earcut, expat, fast_float, glu-libtess, hidapi, hints, imgui, imguizmo, libigl, libnest2d, mcut, md4c, mdns, minilzo, miniz, nanosvg, nlohmann, qhull, qoi, semver, and stb_dxt.

These lists are names and source locations only. They are **not** license conclusions. Some may be header-only, platform-conditional, built only for optional features, or sourced through CMake download declarations. Their exact versions, origins, patches, license texts, and redistribution behavior still need review.

A `.gitmodules` file was not present at the v2.4.2 repository root (the GitHub contents API returned 404 for that path). This does not rule out dependencies downloaded by build scripts or CMake.

## 4. Build and test observations

The v2.4.2 top-level `CMakeLists.txt` exposes these relevant options:

- `SLIC3R_GUI` defaults to enabled.
- `SLIC3R_STATIC` defaults to enabled unless overridden by the build environment.
- `BUILD_TESTS` defaults to disabled.
- `ORCA_TOOLS` defaults to disabled.
- `SLIC3R_ASAN` defaults to disabled.

The source CMake configuration builds `libslic3r` and conditionally includes GUI components, including wxWidgets and libvgcode. The test CMake configuration uses Catch2 and registers suites for libnest2d, libslic3r, slic3rutils, FFF print, and SLA print.

The dependency CMake documentation describes downloading/configuring/building dependencies into a build-local destination directory. It also warns that some build outputs (for example wxWidgets' `wx-config`) embed that destination path. A reproducible build plan must therefore pin both the OrcaSlicer source and all external dependency inputs; a source commit alone does not guarantee a reproducible build.

No build was run as part of this remote repository inspection. Build success, build prerequisites, offline behavior, and test results remain unverified.

## 5. Additional provenance flags

- The source CMake file for the profile validator includes a platform bundle copyright string identifying "OrcaSlicer Pte Ltd" and "All Rights Reserved". This is a review flag, not a conclusion about the licensing of the whole project. The exact file and surrounding notices need to be checked before copying.
- The root release license is AGPLv3, but that does not establish the licensing of every dependency, vendored library, profile, font, image, model, or generated asset.
- The optional Bambu networking component and its proprietary library boundary remain excluded from the proposed core baseline pending separate review.
- The current development branch contains newer work and possibly newer source/resource provenance than v2.4.2. Any cherry-picks or later upstream syncs must repeat provenance review for the changed files.

## 6. Required next audit steps

Before approving the baseline or importing source:

1. Compare v2.4.2 with current upstream development for material fixes, features, security updates, and compatibility changes relevant to the project.
2. Obtain and inspect the exact v2.4.2 source tree locally so automated scanners can examine every file, including file headers and non-code assets.
3. Extract exact external dependency versions, source URLs, checksums, patches, and build conditions from CMake and scripts for each target platform.
4. Inspect all vendored dependency directories and their license/notice files; identify missing, ambiguous, conflicting, or non-redistributable content.
5. Audit profiles, fonts, images, translations, web assets, calibration assets, sample models, branding, and certificates separately.
6. Review optional integrations and packaging paths, including Bambu networking and any platform-specific proprietary binaries.
7. Generate and manually triage an SBOM and license-scan report. Scanner output is evidence to review, not a legal determination.
8. Run a clean, documented baseline build and enabled test suites on the intended first development platform; record exact toolchain and dependency inputs.
9. Decide and record the immutable upstream pin, license expression, exclusions, third-party notices, and import strategy in a reviewed decision record.

## 7. Current decision

**Proposed candidate:** OrcaSlicer v2.4.2 at commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`.

**Not yet approved:** source import, final upstream pin, project SPDX declaration, dependency redistribution, or baseline build reproducibility.

The next engineering task should be the local source/dependency/asset audit and clean baseline build. Keep this repository documentation-only until those checks identify what can safely and reproducibly be imported.
