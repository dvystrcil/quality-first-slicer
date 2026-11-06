# ankerl::unordered_dense provenance and license review

**Status:** Targeted source/provenance review; release notice distribution remains unverified  
**OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (`v2.4.2`)  
**Component:** `deps_src/ankerl`, header-only hash map/set  
**Method:** Compared the vendored header against the exact upstream commit named in the vendored README, inspected its embedded license notice and CMake target, and traced application includes/usages. No build or binary/package inspection was performed.

## 1. Upstream identity and source integrity

The vendored `README.txt` identifies the component as:

- Project: [martinus/unordered_dense](https://github.com/martinus/unordered_dense)
- Version: `4.5.0`
- Commit: `73f3cbb237e84d483afafc743f1f14ec53e12314`
- Distribution note: this is a partial source distribution containing only files needed for compiling PrusaSlicer.

The vendored `unordered_dense.h` is byte-identical to upstream `include/ankerl/unordered_dense.h` at that exact commit. Both have Git blob `13484a9817b9ce598622b791c603588491be8957`. This establishes exact identity for the one vendored header, not completeness of the upstream project distribution.

## 2. License and copyright

The vendored header contains the complete MIT License notice, including:

- SPDX identifier: `MIT`.
- Copyright: `2022-2024 Martin Leitner-Ankerl <martin.ankerl@gmail.com>`.
- The permission condition requiring the copyright and permission notice in copies or substantial portions.
- The standard warranty and liability disclaimer.

The upstream repository's standalone `LICENSE` at the pinned commit is also MIT and identifies Martin Leitner-Ankerl (2022). The OrcaSlicer partial source distribution does not include that standalone file, but the vendored header itself preserves the full MIT notice and expanded 2022–2024 copyright line. This establishes notice presence in the source file; release-package notice inclusion has not been checked.

## 3. Build integration and active use

At the reviewed OrcaSlicer revision:

- `deps_src/CMakeLists.txt` includes `ankerl` in its header-only/interface component group.
- `deps_src/ankerl/CMakeLists.txt` declares an INTERFACE target named `ankerl` and exposes `unordered_dense.h`.
- Application source includes and uses the API, including `src/libslic3r/Arachne/WallToolPaths.hpp`, `SkeletalTrapezoidationGraph.cpp`, `SkeletalTrapezoidation.hpp`, and `SkeletalTrapezoidation.cpp`.

This is evidence of active application use, not merely an unused vendored directory. No reproducible build was performed to validate target propagation across platforms.

## 4. Findings and remaining work

Established:

- The README pins unordered_dense 4.5.0 to a full upstream commit hash.
- The single vendored header is byte-identical to that upstream file.
- The header preserves the full MIT license notice and Martin Leitner-Ankerl copyright attribution.
- The component is configured as a header-only interface target and used by application source.

Still open:

1. Inspect actual source and binary release artifacts / third-party notice bundles to verify notice distribution.
2. Confirm platform-specific compilation and target propagation from reproducible build configurations.
3. Review whether the partial PrusaSlicer source-distribution boundary includes any additional bundled code beyond the single header present in this OrcaSlicer component.

This is a technical provenance and notice-presence review, not a legal determination. No source, build, or dependency configuration was changed.
