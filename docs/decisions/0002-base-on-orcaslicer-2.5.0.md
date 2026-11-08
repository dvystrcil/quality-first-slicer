# 0002: Base on OrcaSlicer 2.5.0

**Status:** Accepted
**Date:** 2026-11-08
**Decided by:** maintainer
**Answers:** [goals Q7](../goals.md#3-first-milestone-v01-proposal)

## Context

The fork's `baseline-2.4.2` branch builds green on Linux CI, and every audit so far is pinned to v2.4.2 (`8500fcdccaa10b5099ac20d252af3a7c560046f1`). OrcaSlicer v2.5.0 was released on 2026-11-07 (`40ecc66f78ed72dc368e0c1ebe40d77f00cc8a19`).

## Decision

v0.1 and all later source work are based on **OrcaSlicer v2.5.0**. The fork gets a new baseline branch from the v2.5.0 tag, carrying over the fork's CI changes. `baseline-2.4.2` is kept unchanged as the reference for the existing audits.

## Alternatives considered

- **Stay on 2.4.2.** All audits are already done for it, but the project would start on a release that upstream has already superseded, with a larger rebase debt later. Rejected.

## Consequences

The jump is large: `git diff --stat v2.4.2 v2.5.0` reports about 16.5k files changed, including 148 under `deps/` and `deps_src/`. Measured differences in the dependency tree:

| Change in 2.5.0 | Effect on this project |
|---|---|
| **Removed:** `deps/OpenCSG`, `deps/GLEW`, `deps/FREETYPE`, `deps_src/clipper` | Use-map item **R1 (OpenCSG + GLEW) is done upstream**. Legacy Clipper removal changes the clipper review |
| **Added:** `deps/Assimp` (5.3.1/5.4.3), `deps/DataChannel` (libdatachannel v0.24.5), `deps/FFMPEG` (n7.0.3 source, or a prebuilt binary on some architectures), `deps/SLVS`, `deps/python3` + `deps_src/pybind11`, `deps/wxInspector` (v1.0.0) | **Six new components** need provenance and license review, and each is a candidate under G4 (lean). The prebuilt FFMPEG path is a binary-provenance item like the [Windows binaries](../windows-binary-provenance.md) |
| Modified: Boost, CGAL, curl, Draco, Expat, Eigen, GMP, JPEG, NLopt, OCCT, OpenCV, OpenSSL, PNG, TBB, wxWidgets declarations | The pinned versions and hashes in the [provenance audit](../dependency-provenance-audit.md) and [platform matrix](../platform-dependency-matrix.md) need a delta review |
| Still present: minilzo wrapper, Creality discovery, `Mouse3DController`, SLA/OpenVDB code | Removal decisions 0003–0005 and R2–R4 still apply, pending re-confirmation on 2.5.0 |

Work this creates, in order:

1. Create the fork's 2.5.0 baseline branch and get the Linux CI build green on it.
2. Re-run `tools/dependency-use-map/run.sh` on 2.5.0 and publish an updated [use map](../dependency-use-map.md). The 2.4.2 results stay as history.
3. Delta-review the provenance documents for changed and new dependencies. New components are not approved until reviewed ([AGENTS.md](../../AGENTS.md) §6).
4. Start Windows CI ([0006](0006-windows-ci-after-rebase.md)).

## Revisit when

- the 2.5.0 baseline cannot be made to build reproducibly on the CI runner;
- a 2.5.x point release fixes problems found while rebasing (then move to that point release).
