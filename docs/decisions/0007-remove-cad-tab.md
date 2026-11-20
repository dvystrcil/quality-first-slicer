# 0007: Remove the parametric Design/CAD tab

**Status:** Accepted
**Date:** 2026-11-19
**Decided by:** maintainer
**Answers:** [goals Q17](../goals.md#7-open-questions-summary), for SLVS only. The other five 2.5.0 projects are still open.

## Context

OrcaSlicer 2.5.0 adds a parametric Design/CAD tab. It is built when `SLIC3R_CAD` is ON, the default, and the option must match between the app and `deps/` (root `CMakeLists.txt:113`, `deps/CMakeLists.txt:66`, at fork `baseline-2.5.0` `665552c1`). Even when it is built, the tab is experimental and off in preferences until a user turns it on (`src/libslic3r/AppConfig.cpp:363-367`).

What the option pulls in:

- **SLVS** (the SolveSpace solver, `deps/SLVS`). It is built only with `SLIC3R_CAD` (`deps/CMakeLists.txt:383-387`). Its one consumer is `L/CAD/SketchSolver.cpp`, reached from `CadDocument.cpp`, `DesignPanel.cpp` and `DesignSketchTool.cpp` ([use map](../dependency-use-map.md) §3.2, `:107`). The files are GPL-3.0, two compiled files carry no notice, and the upstream revision is not recorded ([SLVS review](../slvs-provenance-license-review.md) §3–§4). Not approved.
- **The CAD kernel and GUI sources**: `CAD/*` in libslic3r (`src/libslic3r/CMakeLists.txt:581-583`) and `GUI/CAD/*` in the GUI, described there as "parametric sketch UI, its gizmos, and the MCP control socket" (`src/slic3r/CMakeLists.txt:858-860`).
- **OCCT's ModelingAlgorithms module**: `BUILD_MODULE_ModelingAlgorithms=${SLIC3R_CAD}` (`deps/OCCT/OCCT.cmake:59`; [delta](../dependency-delta-2.4.2-to-2.5.0.md) `:33`). The app adds `TKFillet TKOffset TKBool` to its link list only when the option is ON (`src/libslic3r/CMakeLists.txt:729-730`), and Windows then ships those three DLLs. The module flag also builds `TKFeat`, `TKHelix`, `TKXMesh` and `TKExpress`, which nothing references (`OCCT.cmake:14-26`; [OCCT check](../occt-8.0.1-license-file-check.md) `:59`).

STEP import (`L/Format/STEP.*`) is a separate consumer of OCCT ([use map](../dependency-use-map.md) `:118`). Its toolkits are linked in both configurations (`src/libslic3r/CMakeLists.txt:693-717`), and the module's other toolkits are built either way because DataExchange depends on them (`OCCT.cmake:20-22`).

## Decision

**Remove the Design/CAD tab:** project builds configure both `deps/` and the app with **`SLIC3R_CAD=OFF`**. That drops SLVS and the CAD-only OCCT toolkits (`TKFillet`, `TKOffset`, `TKBool`, and the rest of the ModelingAlgorithms module where `SLIC3R_CAD` gates it) from the build.

**STEP import stays.**

**The CAD sources stay in the fork, unbuilt.** They are not deleted, which keeps rebases onto upstream simple.

**CAD data in 3MF projects round-trips unchanged.** An OFF build opens a 3MF that carries a CAD recipe, slices its mesh, and on save writes the CAD data back byte-for-byte unchanged, so OrcaSlicer loses nothing.

## Scope boundary

- `SLIC3R_CAD=OFF` does **not** take OCCT out of the build. STEP import keeps `TKGeomBase`, `TKShHealing` and the other toolkits in `src/libslic3r/CMakeLists.txt:693-717`.
- 3MF loading reads a CAD recipe (`Metadata/orca_cad.bin`, or the legacy `SnapOrca_cad.bin`) into `model.cad_recipe` (`src/libslic3r/Format/bbs_3mf.cpp:236-239`, `:2046-2059`), and export writes it back (`:6695`). These lines are not under `SLIC3R_CAD` in the grep done for this record. Whether an OFF build already round-trips the recipe unchanged was not checked; the required test below decides it.

## Alternatives considered

- **Keep the upstream default (ON) with the tab off in preferences.** SLVS, the CAD code and the CAD-only OCCT toolkits would still be built and, on Windows, shipped, for a feature the project does not want. Rejected.
- **Optional build, off in project builds** (like [0005](0005-3d-mouse-optional-off.md)). This is in effect what `SLIC3R_CAD=OFF` already gives, because upstream provides the option. The maintainer does not want built-in CAD in this slicer, so the record says *remove*, not *optional*.

## Consequences

- SLVS and its open provenance questions leave the release path. Its review stays in the repository as a record.
- Windows ships three fewer OCCT DLLs. Linux and macOS link OCCT statically, so there the change is mostly build time and dead code (`OCCT.cmake:24-26`).
- **Not solved by this decision, and a blocker for any public release:** eight OCCT 8.0.1 `TKGeomBase` files carry a commercial "may not be provided … to any third party" header ([OCCT check](../occt-8.0.1-license-file-check.md) §3, `:42`, `:50`; upstream [OCCT#1564](https://github.com/Open-Cascade-SAS/OCCT/issues/1564), open with no reply on 2026-11-19). STEP import still links `TKGeomBase`. Reading the archive's build lists shows that all eight files are in `TKGeomBase`'s package file lists, so they are compiled whatever `SLIC3R_CAD` is, and that `TKShHealing`, linked in both configurations, uses two of the classes. No build has confirmed this yet. Tracked in [#62](https://github.com/dvystrcil/quality-first-slicer/issues/62): build to confirm, then patch, replace, or wait on upstream.
- The [use map](../dependency-use-map.md) was produced with `SLIC3R_CAD=ON`. It must be re-run with OFF to show SLVS and the CAD-only toolkits gone.
- The CAD sources remain in the tree as inherited upstream code. Rebases keep them; nothing in a project build compiles them.
- **Required test, before the first release:** a 3MF round-trip test on an OFF build. Load a 3MF that carries a CAD recipe, save it, and compare the CAD parts of the two archives (`Metadata/orca_cad.bin`, and the legacy `SnapOrca_cad.bin` if present): they must be byte-for-byte identical. The mesh must still slice. If the current code does not preserve the recipe, fix it so it does.
- Validation: deps and app build with `SLIC3R_CAD=OFF` on Linux and Windows; STEP import still works; the 3MF round-trip test above passes.
- Done on the 2.5.0 base ([0002](0002-base-on-orcaslicer-2.5.0.md)). Windows needs Windows CI ([0006](0006-windows-ci-after-rebase.md)).

## Revisit when

- the project decides it wants built-in modelling in the slicer.
