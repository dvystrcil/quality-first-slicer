# Initial licensing and provenance review

**Status:** Preliminary repository-level review; not legal advice  
**Review date:** 2026-11-03  
**Scope:** Upstream project license declarations and known repository-level exceptions. This is not a file-by-file dependency or asset audit.

## Executive summary

The project is intended to be derived from OrcaSlicer. OrcaSlicer declares the GNU Affero General Public License version 3 (AGPL-3.0). PrusaSlicer also distributes its main project under the GNU Affero General Public License version 3.

This makes AGPLv3 the expected licensing baseline for a source-derived slicer fork. It does **not** establish that every upstream file, bundled dependency, profile, asset, plugin, or third-party component is licensed under AGPLv3.

Do not add a top-level `LICENSE`, SPDX declaration, or source imports until the project completes the source and third-party inventory described below and confirms the intended SPDX expression. The upstream license files inspected are the standard AGPL version 3 text; they do not, by themselves, establish an "or later" grant for the project code. `AGPL-3.0-only` is therefore the provisional SPDX candidate, not an approved declaration.

## Sources inspected

| Source | Finding |
|---|---|
| [OrcaSlicer README](https://github.com/OrcaSlicer/OrcaSlicer/blob/main/README.md) | Explicitly declares OrcaSlicer under GNU AGPL version 3. It also calls out separately licensed pressure-advance calibration code and the optional Bambu networking plugin. |
| [OrcaSlicer LICENSE.txt](https://github.com/OrcaSlicer/OrcaSlicer/blob/main/LICENSE.txt) | Contains the GNU Affero General Public License, Version 3, dated 19 November 2007. |
| [PrusaSlicer README](https://github.com/prusa3d/PrusaSlicer/blob/master/README.md) | Identifies PrusaSlicer as originally based on Slic3r. The repository identifies its license as AGPL-3.0. |
| [PrusaSlicer LICENSE](https://github.com/prusa3d/PrusaSlicer/blob/master/LICENSE) | Contains the GNU Affero General Public License, Version 3, dated 19 November 2007. |
| [GNU AGPLv3 text](https://www.gnu.org/licenses/agpl-3.0.html) | Section 13 covers remote network interaction with a modified program and the corresponding-source offer. |
| [GNU GPL FAQ](https://www.gnu.org/licenses/gpl-faq.html#AGPLv3CorrespondingSource) | FSF guidance explains corresponding-source scope, including certain incorporated dependency source. |

The upstream license files were fetched from their respective repositories during this review. The OrcaSlicer repository uses `LICENSE.txt`; the PrusaSlicer repository uses `LICENSE`.

## Known exceptions and boundaries

### Pressure-advance calibration pattern

OrcaSlicer documents that its pressure-advance calibration pattern test is adapted from Andrew Ellis' generator, which is licensed under GPL-3.0, and that generator in turn is adapted from a Sineos Marlin generator also licensed under GPL-3.0.

AGPLv3 section 13 includes a compatibility provision for combining an AGPLv3 work with a GPLv3 work. This does not remove the need to preserve the applicable notices, source provenance, and license terms for the incorporated code.

**Action:** If this code is retained, identify the exact files and upstream origins, preserve notices, and include it in the third-party inventory. If it is removed or replaced, record that explicitly.

### Bambu networking plugin

OrcaSlicer documents that its optional Bambu networking plugin is based on non-free libraries from Bambu Lab.

**Project boundary:** Do not copy, redistribute, statically or dynamically bundle, or otherwise incorporate those non-free libraries into this project without a separate, documented permission and licensing review. Keep any future Bambu-specific network integration optional and isolated from the core slicer. Compatibility with Bambu printers, profiles, 3MF files, and generated G-code does not itself require redistributing the vendor's proprietary networking libraries.

### Profiles, resources, branding, and user content

Do not assume that every printer profile, filament profile, preset, icon, image, font, translation, sample model, logo, or other resource inherits the top-level source license. Check file headers, adjacent notices, repository history, upstream sources, and any explicit terms before copying.

Likewise, imported user profiles and 3MF projects remain subject to their authors' rights and any applicable terms. The project's license should not be represented as granting rights to user-uploaded material.

### Dependencies and bundled components

Both upstream repositories contain dependency and bundled-dependency trees. A repository-level AGPL declaration is not a substitute for auditing those components.

Before importing/building the codebase, inventory:
- Git submodules and vendored source trees.
- Build-time and runtime dependencies, including platform-specific dependencies.
- Bundled libraries, generated code, and binary blobs.
- Optional plugins and dynamically loaded components.
- Fonts, icons, images, translations, profiles, and other non-code assets.
- Build scripts and packaging inputs that download or redistribute third-party materials.

Record each component's name, version or immutable source revision, origin, license expression, copyright/notice obligations, modifications, distribution status, and review status.

## AGPLv3 implications for this project

- Distribution of modified slicer binaries and source requires compliance with AGPLv3's applicable source, notice, and license conditions.
- AGPLv3 section 13 adds a corresponding-source offer for users interacting remotely over a computer network with a modified version that supports that interaction. The exact application depends on the design and deployment of each service; obtain legal review before launching a network-hosted derivative.
- The optional profile/3MF service is a separate architecture and licensing review item. Do not assume that putting a service in a separate repository or process automatically resolves derivative-work or network-interaction questions.
- The project must not impose additional restrictions that conflict with the rights granted by AGPLv3.

This document records engineering due diligence, not a legal opinion about whether a particular combination or deployment is a derivative work.

## Required work before source import

- [ ] Record exact upstream repositories, commit IDs, and source archive hashes selected for the initial fork.
- [ ] Review the upstream license and copyright notices at the exact pinned revisions.
- [ ] Inventory submodules, vendored dependencies, bundled binaries, generated code, and optional plugins.
- [ ] Inventory profiles, presets, translations, fonts, images, icons, sample models, and branding separately from source code.
- [ ] Identify all files with non-AGPL, missing, conflicting, or unclear licensing.
- [ ] Decide whether the Bambu networking plugin and its proprietary libraries are excluded from the fork.
- [ ] Decide the project's exact SPDX license expression based on the complete source and rights review.
- [ ] Establish a third-party notices and provenance directory before importing source.
- [ ] Select automated license and SBOM tooling; validate its output manually for high-risk or ambiguous components.
- [ ] Obtain qualified legal review before public binary distribution or deployment of a modified network-accessible service.

## Preliminary decision

**Working direction:** Treat AGPLv3 as the expected license for the source-derived slicer. Keep the top-level license declaration and source import blocked until the exact upstream revision and its complete third-party/resource inventory have been reviewed.

This is deliberately conservative. The goal is to preserve the ability to build and distribute the project without accidentally importing proprietary or incompatibly licensed material.
