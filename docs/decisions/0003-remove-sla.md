# 0003: Remove SLA (resin) printing

**Status:** Accepted
**Date:** 2026-11-08
**Decided by:** maintainer
**Answers:** [goals Q9](../goals.md#5-feature-scope-decisions)

## Context

The project is an FDM slicer (see the [product vision](../product-vision.md)). OrcaSlicer still carries PrusaSlicer-derived SLA code: `SLAPrint`, hollowing, the SLA gizmos and the SLA support tree. On v2.4.2 every bundled printer profile was FFF (239/239). OpenVDB, with its forked Blosc and patched OpenEXR, is reachable only from SLA code; the FDM tree-support OpenVDB path is compiled out (see [use map](../dependency-use-map.md) O3).

## Decision

**Remove SLA printing technology** from the product: the SLA print pipeline, SLA-only UI (for example the hollowing gizmo), SLA-only configuration, and the dependencies that only SLA uses (OpenVDB, Blosc, OpenEXR/IlmBase).

## Scope boundary

"SLA" means the resin printing feature, not every file under `src/libslic3r/SLA/`. Some code there is used by FDM. On v2.4.2:

- `SLA/IndexedMesh` is used by `AABBMesh`;
- `SLA/SupportTree.cpp` is in the libnest2d/NLopt consumer set;
- AGG rasterisation is used by both `SLA/RasterBase.cpp` and FDM `Support/SupportMaterial.cpp`.

Shared code stays, moved out of `SLA/` if that helps clarity. Removal PRs must show, through the use map and the test suites, that FDM consumers are untouched.

## Alternatives considered

- **Optional build.** This keeps the code and its fork-sourced dependencies alive for a feature the project does not target. Rejected.

## Consequences

- OpenVDB, Blosc and OpenEXR leave the build, along with their fork and patch provenance items.
- The removal is entangled: `Plater` holds an `SLAPrint`, `Model.hpp` and CSG voxelisation reference these headers. Expect several staged PRs, each with FDM regression evidence (G-code corpus unchanged).
- 3MF projects that contain SLA settings must still load; SLA-only keys are ignored with a warning. This needs a test.
- Done on the 2.5.0 base ([0002](0002-base-on-orcaslicer-2.5.0.md)). The reachability evidence must be re-confirmed there first.

## Revisit when

- the project decides to support resin printers.
