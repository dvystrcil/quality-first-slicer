# 0005: 3D mouse support optional, off in project builds

**Status:** Accepted
**Date:** 2026-11-08
**Decided by:** maintainer
**Answers:** [goals Q11](../goals.md#5-feature-scope-decisions)

## Context

3Dconnexion/spacenavd input is implemented in `Mouse3DController.cpp`. HIDAPI calls (`hid_*`) and libspnav calls (`spnav_*`) appear only there, but `Mouse3DController.hpp` is included by `GLCanvas3D`, `GUI_App`, `MainFrame` and `Plater` ([use map](../dependency-use-map.md) O2). HIDAPI's license election is undocumented and its upstream license files are missing ([HIDAPI review](../hidapi-provenance-license-election.md)). libspnav is linked statically when found and has had no review. The maintainer has no 3D mouse to test with.

## Decision

Add a CMake option, `SLIC3R_3DMOUSE`, **default OFF**.

- OFF: no hidapi, no libspnav; a stub `Mouse3DController` keeps the four including files compiling, and the GUI works normally with mouse and keyboard.
- ON: the current behaviour, documented as **unverified** by the project.

Project releases are built with the option OFF.

## Alternatives considered

- **On by default, labelled unverified.** This ships code nobody on the project has run. Rejected.
- **Remove entirely.** The cost of keeping it behind an option is low, and some users rely on it. Not chosen.

## Consequences

- Shipped binaries contain no HIDAPI or libspnav, which takes the HIDAPI license-election question off the release path. Notices are still kept for the source tree.
- CI builds both settings so the ON path keeps compiling; only OFF is released.
- Work is done on the 2.5.0 base ([0002](0002-base-on-orcaslicer-2.5.0.md)); Windows uses `win/hid.c`, which needs Windows CI ([0006](0006-windows-ci-after-rebase.md)).

## Revisit when

- a maintainer or regular tester with a 3D mouse joins; then ON could be validated and shipped.
