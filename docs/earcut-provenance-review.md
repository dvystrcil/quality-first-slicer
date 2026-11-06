# Mapbox Earcut provenance and license review

**Status:** Targeted source/provenance review; release-package notice distribution remains unverified  
**OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (`v2.4.2`)  
**Component:** `deps_src/earcut`, header-only C++ polygon triangulation library  
**Method:** Compared the vendored header and license text with Mapbox's pinned Earcut 2.2.4 source commit, inspected the component README/CMake declaration, and traced a direct application include and API call. No local build, binary/package inspection, or legal review was performed.

## 1. License and copyright evidence

The vendored `deps_src/earcut/LICENSE` contains the ISC License and identifies:

- Copyright (c) 2015, Mapbox.
- Permission to use, copy, modify, and/or distribute the software, provided the copyright notice and permission notice appear in all copies.
- The standard as-is warranty and liability disclaimer.

The vendored license file is byte-identical to the upstream `LICENSE` at Mapbox Earcut 2.2.4 commit `4811a2b69b91f6127a75e780de6e2113609ddabb` (Git blob `8bafb577305e2ade52a4f75a7c589f9db8a4e5eb`). The source tree therefore contains the full upstream license text and copyright notice. This establishes source-tree presence, not whether all binary/release notice bundles include it.

## 2. Upstream version and source comparison

The vendored README explicitly says the C++ port is based on Earcut 2.2.4. Its upstream release commit is:

- Repository: [mapbox/earcut.hpp](https://github.com/mapbox/earcut.hpp)
- Commit: [`4811a2b69b91f6127a75e780de6e2113609ddabb`](https://github.com/mapbox/earcut.hpp/commit/4811a2b69b91f6127a75e780de6e2113609ddabb)
- Commit subject: `Port bugfixes 2.2.4 (#102)`
- Commit date: 2022-09-06.

The vendored `earcut.hpp` is not byte-identical to the upstream header (vendored Git blob `fd3381484c6a10eae486ef74512c174a73b14e3a`; upstream blob `a73ae87c8ee393c65151ee0a8f5fb845776b6dfe`). A line comparison found two differences:

1. The OrcaSlicer copy adds `#include <cstdint>`, which is absent from the upstream 2.2.4 header.
2. The OrcaSlicer copy omits the upstream local `iterations` counter declaration and its increment in `Earcut<N>::earcutLinked()`.

No other line differences were found by this comparison. The upstream 2.2.4 commit's own diff records algorithm changes for z-order coordinate scaling, hole elimination/filtering, hole-bridge selection, and point-in-triangle comparisons. Those algorithm changes are present in the reviewed vendored header; the two differences listed above remain unexplained as downstream source edits. Do not infer their author, intent, or functional significance from this comparison alone.

The README's version statement is consistent with the upstream 2.2.4 lineage, but the exact original archive/checksum used when OrcaSlicer first obtained the source has not been established.

## 3. Build integration and active use

At the reviewed OrcaSlicer revision:

- `deps_src/CMakeLists.txt` includes `earcut` among the header-only/interface libraries.
- `deps_src/earcut/CMakeLists.txt` declares an `INTERFACE` target named `earcut` and exposes the component directory as a system include directory.
- `src/slic3r/GUI/SkipPartCanvas.cpp` includes `<earcut/earcut.hpp>` and calls `mapbox::earcut<uint32_t>(polygon)`.

This is evidence of an active application source include and API call, not merely an unused vendored directory. The exact target propagation and platform-specific compilation matrix were not independently built or validated in this review.

## 4. Findings and remaining work

Established:

- ISC license text and Mapbox 2015 copyright notice are present in the vendored source tree.
- The license file exactly matches the upstream 2.2.4 license file.
- The README identifies Earcut 2.2.4, and the source closely matches the corresponding upstream header.
- The component is configured as a header-only interface target and is used by GUI source code.

Still open:

1. Establish the original import commit/archive and its checksum, if an immutable original source artifact is available.
2. Attribute or explain the two header differences (the extra `<cstdint>` include and omitted `iterations` counter) from source history.
3. Inspect actual release/source packages and third-party notice bundles to verify that the ISC license and Mapbox copyright notice are distributed where required.
4. Confirm platform-specific compilation and target propagation from reproducible build configurations.

This is a technical provenance and notice-presence review, not a legal determination. No source, build, or dependency configuration was changed.
