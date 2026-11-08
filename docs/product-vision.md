# Product Vision

## Why this project exists

OrcaSlicer and PrusaSlicer are two of the best FDM slicers available. Both give granular control over the G-code they produce. Each has a different weakness that pushed this project into existence:

| | Strength worth keeping | Problem this project exists to fix |
|---|---|---|
| **OrcaSlicer** | Modern, practical workflow; broad printer ecosystem; calibration tools | **Growing bloat** in the form of features, vendor integrations and dependencies that do not serve print quality. **Walls around user data:** synced profile storage is offered only through Orca's own hosted service (`OrcaCloudServiceAgent`, defaulting to `api.orcaslicer.com`/`cloud.orcaslicer.com` in v2.5.0), with no open or self-hosted alternative |
| **PrusaSlicer** | Fast, accurate G-code | A dated, awkward user interface |
| **Both** | Fine-grained control | **Questionable defaults** that users must discover and undo |

**Worked example of a questionable default: arc fitting.** Arc fitting converts line segments into `G2`/`G3` arcs. It mainly helps older firmware and controllers that are short on G-code bandwidth or storage. On Klipper, `G2`/`G3` needs the optional `[gcode_arcs]` module, and that module [splits every arc back into line segments](https://github.com/Klipper3d/klipper/blob/master/docs/Config_Reference.md#gcode_arcs) of a fixed resolution (default 1 mm). The printer therefore gains nothing from the arc, while the path has passed through an extra approximation step. Even so, OrcaSlicer's bundled vendor process profiles turn it on: 207 profile entries in v2.4.2 and 218 in v2.5.0, mostly Creality, Flashforge, Anycubic and Qidi. In v2.5.0 the option became a three-way choice, and the [release notes](https://github.com/OrcaSlicer/OrcaSlicer/releases/tag/v2.5.0) record that a fix ([OrcaSlicer#17047](https://github.com/OrcaSlicer/OrcaSlicer/pull/17047)) re-enabled it from profiles for Creality, Prusa and 11 other vendors after the alpha had briefly turned it off. A user upgrading through 2.5 could see arc fitting switch itself back on without having changed anything. A default like this should follow the target firmware and be backed by evidence, not inherited from older hardware.

This project therefore aims for **OrcaSlicer's workflow, PrusaSlicer-grade G-code, and defaults that a user can trust**. It should be lean, keep the user's data under the user's control, and justify every default.

## Positioning

A quality-first, general-purpose FDM slicer that combines OrcaSlicer's practical workflow and broad ecosystem with a conservative, evidence-driven approach to slicing quality, reliability, and defaults.

The goal is not to remove capability for its own sake. The goal is to make the common path dependable and understandable while keeping advanced control available when it is genuinely useful.

## Product principles

1. **Quality before headline speed.** Optimize for repeatable, successful prints rather than marketing maximums.
2. **Sensible defaults.** Common printer and material combinations should produce good results without requiring users to tune dozens of parameters.
3. **Progressive disclosure.** Present approachable Standard, Advanced, and Expert experiences without removing expert capability.
4. **Evidence over intuition.** Changes to slicing behavior and defaults require reproducible benchmarks, regression tests, and physical validation where practical.
5. **Broad, honest compatibility.** Support a wide range of FDM printers and firmware, while clearly labeling what has and has not been validated.
6. **Offline-first core.** Local slicing and local profiles must remain useful without an account or cloud service. Network integrations are optional.
7. **Upstream leverage.** Build on the OrcaSlicer foundation; avoid rewriting mature functionality without a demonstrated need.
8. **Transparent provenance.** Preserve upstream attribution and comply with all applicable licenses and third-party terms.

## Intended scope

The product is intended to retain the essential workflow and capabilities expected of a modern FDM slicer, including:

- Model import, arrangement, plate management, and preview.
- Supports, infill, modifiers, variable layer heights, and multi-material workflows where supported by the printer.
- Printer, filament, and process profiles with clear compatibility and inheritance.
- Calibration workflows for flow, pressure advance, temperature, retraction, and related parameters.
- Klipper and other common firmware workflows.
- 3MF project import/export and preservation of relevant project metadata.
- Bambu printer profile and file compatibility, subject to explicit validation limits.

## Quality and defaults work

Defaults to evaluate include wall speeds and counts, acceleration and jerk, volumetric flow, infill, supports, cooling and bridging, retraction, layer heights, first-layer behavior, and machine/material constraints.

The project must distinguish:
- Mechanical or firmware motion limits.
- Material and hotend extrusion-flow limits.
- Quality-oriented operating ranges.
- Advertised or theoretical maximums.

No default should be raised simply because a printer advertises a higher maximum speed. Changes require documented rationale and measurable evidence.

## Validation honesty

Automated profile checks, G-code analysis, and simulation provide valuable evidence but do not replace physical prints. Validation status must distinguish automated validation, community physical validation, project-hardware physical validation, and unverified behavior.

The initial project hardware target is a Klipper/Kalico Cartesian bed-slinger. Other printer families, including Bambu models, may be supported in software before project-owned physical validation is available. Such support must not be described as physically validated without evidence.

## Non-goals and boundaries

- Rewriting the slicing engine from scratch.
- Removing advanced capabilities solely to make the interface appear simpler.
- Optimizing for speed at the expense of reliability or quality.
- Requiring vendor accounts, cloud services, or telemetry for core slicing.
- Claiming G-code simulation is a certified safety system.
- Redistributing proprietary vendor libraries or credentials as part of the core project.

## Initial technical direction

OrcaSlicer is the intended initial code foundation. PrusaSlicer is an external engineering and quality benchmark, not a source to copy from by default. Source import and derived distribution are gated on upstream architecture, exact license text, dependency, and file-level provenance review.

The initial repository phase establishes governance and requirements before importing slicer source.
