# Anti-Grain Geometry 2.4 provenance and license-election review

**Status:** Initial provenance and license-text review; license election and release notice distribution remain unresolved  
**OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (`v2.4.2`)  
**Component:** `deps_src/agg`, header-only Anti-Grain Geometry rasterization library  
**Method:** Inspected the vendored `copying` file, the 24 headers exposed by the component CMake target, import history, and application include sites. No local checkout, byte-for-byte comparison against an authenticated upstream source archive, build, or release artifact inspection was performed.

## 1. Upstream identity and source history

The vendored headers identify the project as **Anti-Grain Geometry (AGG) 2.4** and carry the copyright line:

- Copyright (C) 2002–2005 Maxim Shemanarev
- Project/contact references: `antigrain.com`, `mcseem@antigrain.com`, and `mcseemagg@yahoo.com`

The repository history shows the files first entering the OrcaSlicer lineage in BambuStudio's initial full-source import:

- Import commit: `1555904beffef41195003f184dec0af46b308eee`
- Commit message: “Add the full source of BambuStudio”, using version 1.0.10
- Author recorded by Git: `lane.wei` (`lanewei@bambulab.com`)
- Later move into `deps_src/agg`: `883607e1d4a0b2bb719f2f4bcd9fd72f8c2174fa`, a repository-structure refactor that moved third-party source from `src` to `deps_src`

The history establishes the first observed import point in this repository lineage, not the original upstream download location, archive checksum, or exact upstream commit. The vendored files' version banners are consistent with AGG 2.4, but a full source-to-upstream comparison has not been completed.

## 2. License text and unresolved election

The vendored `deps_src/agg/copying` file explicitly describes AGG 2.4 as having a dual-licensing model and includes two distinct alternatives:

1. **Anti-Grain Geometry Public License** — a short permissive grant allowing copying, use, modification, sale, and distribution, conditioned on the copyright notice appearing in all copies.
2. **Modified BSD License** — a three-condition BSD-style grant, including source-notice retention, binary-notice reproduction in documentation and/or other materials, and a restriction on using the author's name for endorsement without prior written permission.

The file says the Modified BSD license was first added in AGG v2.4 “just for convenience” and that it does not restrict rights when choosing the AGG Public License. This describes alternatives; it does not record which alternative BambuStudio/OrcaSlicer elected for this vendored copy.

The inspected AGG headers contain the AGG 2.4 copyright and the short original permission/warranty text. That text is consistent with the AGG Public License wording, but its presence alone does not establish that the project elected that alternative rather than the Modified BSD option also supplied in `copying`. No separate election statement, upstream package manifest, or project-specific licensing record was found in the inspected material.

**Do not classify this component as unambiguously BSD-3-Clause or as unambiguously AGG Public License on the present evidence.** The license election is an open provenance question requiring upstream packaging/history evidence or confirmation from the relevant copyright holder/distributor.

## 3. Vendored build boundary and active use

At the reviewed revision:

- `deps_src/CMakeLists.txt` adds `agg` in the header-only/interface group.
- `deps_src/agg/CMakeLists.txt` defines an INTERFACE target named `agg`, exports the component directory as an include directory, and lists 24 AGG headers as interface sources.
- Application and test sources include `libslic3r/SLA/AGGRaster.hpp`; that wrapper includes AGG headers for rasterization.
- Confirmed include sites include `src/libslic3r/SLA/RasterBase.cpp`, `src/libslic3r/SLA/RasterToPolygons.cpp`, GUI font-image jobs, and SLA/geometry tests.

This establishes active source-level use of AGG APIs in SLA rasterization and related rendering paths. It does not, by itself, prove that the `agg` interface target is propagated correctly in every platform build; the inspected `libslic3r` link list did not provide a conclusive target-link edge. Build-graph and platform validation remain open.

## 4. Findings and remaining work

Established:

- The vendored source identifies itself as AGG 2.4 and names Maxim Shemanarev with 2002–2005 copyright.
- The repository history traces the initial import to BambuStudio 1.0.10 and the later directory move to the OrcaSlicer `deps_src` layout.
- The component's `copying` file contains two alternative AGG 2.4 license texts.
- AGG is actively included by production SLA rasterization code and tests.
- CMake declares an interface target exposing the vendored headers.

Still open:

1. Resolve which of the two AGG 2.4 license alternatives was elected for the BambuStudio/OrcaSlicer distribution; do not infer the election solely from the header text.
2. Identify the original AGG 2.4 source archive or authoritative upstream revision and record a checksum or commit.
3. Compare all 24 vendored headers and `copying` against that source to identify local changes, omissions, and any additional copied code.
4. Trace the actual CMake dependency edge and validate compilation/target propagation on supported platforms.
5. Inspect source and binary release artifacts / third-party notices. If the Modified BSD alternative was elected, specifically verify the required binary documentation/materials notice; if the AGG Public License was elected, verify preservation of its copyright notice in copies.
6. Determine whether any AGG-derived or embedded code in this subset carries separate attribution or license terms.

This is a technical provenance and notice review, not a legal determination. No source, build, dependency, or license files were changed.
