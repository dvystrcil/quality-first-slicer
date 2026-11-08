# Quality-First Slicer

A quality-first, general-purpose FDM slicer built on the OrcaSlicer foundation.

The project aims to combine OrcaSlicer's practical workflow and broad printer support with a conservative, evidence-driven approach to print quality, reliability, and sensible defaults.

## Why

OrcaSlicer is becoming bloated and is putting up walls around user data: synced profile storage works only through its own hosted service. PrusaSlicer produces fast, accurate G-code, but its interface feels decades old. Both offer fine-grained control, yet ship questionable defaults; one example is arc fitting enabled in vendor profiles for modern Klipper printers, which gain nothing from it. This project aims for OrcaSlicer's workflow with PrusaSlicer-grade G-code and defaults you can trust. See [the product vision](docs/product-vision.md#why-this-project-exists).

## Project goals

- Keep profiles and settings under the user's control: local-first, with no dependency on any single vendor's cloud for storing or syncing them.
- Stay lean: remove or make optional the features and dependencies that do not serve FDM print quality.
- Match PrusaSlicer-grade G-code accuracy, using it as an external benchmark.
- Choose defaults for the target firmware (Klipper/Kalico first), not for decade-old controllers. Every default must have documented rationale and evidence.
- Prioritize reliable, repeatable print quality over headline speed.
- Make strong defaults work well without requiring extensive manual tuning.
- Keep advanced controls available through progressive disclosure.
- Support a broad range of FDM printers and firmware, including Klipper-based machines and Bambu printer profiles.
- Validate slicing behavior with reproducible tests, independent G-code analysis, and physical prints where hardware is available.
- Keep the core slicer useful offline; network and vendor integrations remain optional.
- Preserve upstream attribution and license obligations.

## Development status

**Project foundation.** The repository is being established. No slicer source has been imported yet. The upstream architecture, licensing, dependency inventory, and reproducible baseline build must be reviewed before source changes begin.

## Engineering approach

- Test-driven development: establish a failing, explicit test before changing behavior.
- Compare against known-good baselines.
- Use repeatable scripts and machine-readable evidence where possible.
- Test through real downstream consumers when integration behavior matters.
- Record acceptance criteria before substantial work and close with evidence for each criterion.
- Preserve contributor changes, comments, and review history.
- Treat physical print results as the authority for print-quality claims.

See [AGENTS.md](AGENTS.md) for contributor and AI-agent instructions. The project decisions and rationale will be recorded in [docs/](docs/).
