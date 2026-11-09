# Goals and success criteria

**Status:** Draft. Every criterion and decision below is **PROPOSED** until the maintainer answers it. Answered items move into decision records under `docs/decisions/` and are marked **DECIDED** here, with a link.
**Builds on:** [Why this project exists](product-vision.md#why-this-project-exists) and the [product vision](product-vision.md)

The vision says what the project values. This document says what "done" and "better" mean, so that work can be ranked and pull requests can be judged against something.

## 1. Goals

Each goal traces back to a problem in the [why](product-vision.md#why-this-project-exists).

| ID | Goal | Problem it answers |
|---|---|---|
| **G1** | **Trustworthy defaults.** Defaults are chosen for the target firmware and backed by evidence | Questionable defaults in OrcaSlicer and PrusaSlicer (e.g. arc fitting on Klipper) |
| **G2** | **Accurate G-code.** Output matches or beats PrusaSlicer on the G-code accuracy benchmarks | PrusaSlicer's G-code is the bar to meet |
| **G3** | **User-owned profiles.** Profiles and settings are stored and synced where the user chooses, and no vendor cloud is required | OrcaSlicer's sync works only through its own hosted service |
| **G4** | **Lean.** Features and dependencies that don't serve FDM print quality are removed or made optional | OrcaSlicer bloat |
| **G5** | **Modern, responsive UI.** Keep OrcaSlicer's workflow, with progressive disclosure | PrusaSlicer's dated interface |
| **G6** | **Honest validation.** Every behaviour and profile claim carries its evidence level (automated, community, project hardware, unverified) | Applies across the board (vision principle 5) |

## 2. Proposed success criteria

These are candidates, written to be measurable. Each needs a yes, an edit, or a rejection.

| Goal | Proposed criterion | How it is measured | Open question |
|---|---|---|---|
| G1 | Every changed default has a decision record with rationale and before/after evidence | Review gate: a PR that changes a default without a linked record fails review | Q1: is a review gate enough, or should CI check it? |
| G1 | On the reference printer, a fixed test-print set does at least as well with project defaults as with stock OrcaSlicer defaults for the same printer, and no test gets worse | Physical prints scored with a written rubric (dimensional accuracy, first layer, surface defects) | Q2: which test prints and which rubric? |
| G2 | For a fixed model corpus, extrusion and path deviation from the intended geometry is no worse than PrusaSlicer's | G-code analysis harness: per-model geometric deviation and extrusion totals, run in CI | Q3: which deviation metrics count as "accuracy" to you? |
| G2 | No unexplained G-code change: every PR that changes G-code output shows the diff on the regression corpus | CI regression corpus with recorded baselines | — |
| G3 | A user can store and sync all user profiles to a target they choose (a local folder at minimum) with no account | End-to-end test: export, sync and restore on a clean machine | Q4: which backends? (folder, git, WebDAV, S3, self-hosted server) |
| G3 | Profiles stay in an open, documented format that is readable without the app | Format spec plus a round-trip test | — |
| G4 | Every dependency in the [dependency/use map](dependency-use-map.md) has a recorded keep/remove/optionalize decision | The map's ranked list has no undecided entries | — |
| G4 | The default build has no component that the use map shows as unused | `tools/dependency-use-map/run.sh` reports no unused targets in the app closure | — |
| G5 | Proposed: UI responsiveness budgets (e.g. a settings change shows in the preview within N ms on reference hardware) | Scripted UI timing | Q5: what UI problems matter most to you? This goal is the least defined |
| G6 | Every bundled printer profile carries a validation-level label | Profile check in CI | — |

## 3. First milestone (v0.1): proposal

**v0.1 = "the baseline is trustworthy, and the first default is evidence-backed".**

| # | Deliverable | Status |
|---|---|---|
| M1 | Reproducible baseline build of the fork on CI (`baseline-2.5.0`) | **Done** on Linux x86_64 (fork workflow `linux-arc-baseline.yml`, [dvystrcil/OrcaSlicer#3](https://github.com/dvystrcil/OrcaSlicer/pull/3)). Was done first on `baseline-2.4.2`, which stays as the audit reference |
| M2 | G-code regression corpus + harness (G2), with recorded baselines from stock 2.4.2 and PrusaSlicer | Not started |
| M3 | Remove the no-consumer components (R2–R4 in the [use map](dependency-use-map.md); R1 was removed upstream in 2.5.0) | Not started |
| M4 | First evidence-backed default: arc fitting off for Klipper/Kalico process profiles, with corpus diff + test prints | Not started |
| M5 | Validation-level labels on the reference printer's profile | Not started |

**Q6:** Is that the right v0.1? In particular, should G3 (user-owned profiles) come into v0.1? It is the most user-visible difference from OrcaSlicer.

**Q7: DECIDED.** The base is OrcaSlicer v2.5.0; see [0002](decisions/0002-base-on-orcaslicer-2.5.0.md). M1 has been redone on 2.5.0. R1 (OpenCSG + GLEW) is already removed upstream in 2.5.0, and six new dependency projects arrive with it.

## 4. Platform matrix

**Q8: DECIDED** in [0001: Supported platforms](decisions/0001-supported-platforms.md).

| Platform | Status |
|---|---|
| Linux x86_64 AppImage | **Supported** |
| Windows x64 | **Supported**, hand-tested; CI build path still open |
| Linux x86_64 Flatpak | Future |
| Linux aarch64 (arm64) | Future (testable on a Raspberry Pi or a Chromebook) |
| Windows ARM64 | Not supported |
| macOS | **Not supported** (cannot be tested); code stays as inherited upstream code, nothing removed |

## 5. Feature scope decisions

These come straight from the use map's ranked list. Each one blocks a removal or optionalization PR.

| ID | Feature | Options | What follows from each |
|---|---|---|---|
| ~~Q9~~ | SLA (resin) | **DECIDED: remove**; see [0003](decisions/0003-remove-sla.md) | OpenVDB, Blosc and OpenEXR leave the build; code under `SLA/` shared with FDM stays |
| ~~Q10~~ | Creality K-series LAN auto-discovery | **DECIDED: remove**; see [0004](decisions/0004-remove-creality-lan-discovery.md) | The AGPL mDNS wrapper leaves the build; manual IP entry stays |
| ~~Q11~~ | 3D mouse (3Dconnexion / spacenavd) | **DECIDED: optional, off in project builds**; see [0005](decisions/0005-3d-mouse-optional-off.md) | hidapi and libspnav are absent from released binaries |
| **Q12** | Bambu networking plugin (proprietary, loaded at runtime) | keep the loader / optional / remove | The vision's non-goal says no proprietary vendor libraries in core; Bambu compatibility is in scope. This decides how both hold together |
| **Q13** | OrcaSlicer Cloud client | keep / optional / remove, and replace with G3 | Decides whether `OrcaCloudServiceAgent` stays next to the user-owned sync |
| **Q14** | Printer web UI, camera view, cloud login (webkit2gtk, GStreamer, libsecret) | keep / optional | Linked by the GUI. Optional makes a no-network build possible (vision principle 6) |
| **Q15** | MCUT mesh boolean | keep / replace with CGAL once tests exist | Replacement removes a GPL-3.0-or-later component (O4) but needs a test corpus first |

## 6. Licensing objective

**Proposed:** the project ships under AGPL-3.0, as derived from OrcaSlicer (the SPDX expression is still provisional; see [licensing and provenance](licensing-and-provenance.md)). Removing GPL- or AGPL-licensed dependencies therefore **does not change the project's license** and is not a goal in itself. Licensing-driven removals aim to:

1. reduce the notice, provenance and license-election burden for shipped components;
2. shrink the supply-chain and security surface (forks, local patches, downloaded binaries);
3. support G4 (lean).

**Q16:** Do you confirm this objective, rather than aiming at a more permissive outbound license, which would not be achievable on an OrcaSlicer base?

## 7. Open questions (summary)

| ID | Question | Blocks |
|---|---|---|
| Q1 | Review gate vs CI check for default changes | G1 process |
| Q2 | Test-print set and scoring rubric | G1 physical criterion, M4 |
| Q3 | Which G-code accuracy metrics count | G2, M2 |
| Q4 | Profile sync backends | G3 |
| Q5 | Which UI problems matter most | G5 |
| Q6 | v0.1 contents, G3 in or out | Milestone |
| ~~Q7~~ | Base: **DECIDED, 2.5.0**; see [0002](decisions/0002-base-on-orcaslicer-2.5.0.md) | — |
| ~~Q8~~ | Platform matrix: **DECIDED**, [0001](decisions/0001-supported-platforms.md) | — |
| ~~Q8a~~ | Windows CI: **DECIDED**, GitHub-hosted, right after the 2.5.0 rebase; see [0006](decisions/0006-windows-ci-after-rebase.md) | — |
| ~~Q9–Q11~~ | Feature scope: **DECIDED**; see [0003](decisions/0003-remove-sla.md), [0004](decisions/0004-remove-creality-lan-discovery.md), [0005](decisions/0005-3d-mouse-optional-off.md) | — |
| Q12–Q15 | Feature scope: Bambu plugin, Orca Cloud client, printer web UI/camera, MCUT | O4–O6 |
| Q17 | Review and keep/remove decisions for the six dependency projects added in 2.5.0 (Assimp, DataChannel, FFMPEG, SLVS, python3 + pybind11, wxInspector) | 2.5.0 baseline approval, G4 |
| Q16 | Licensing objective | Framing of #47 |
