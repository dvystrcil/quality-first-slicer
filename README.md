# Quality-First Slicer

A quality-first, general-purpose FDM slicer built on the OrcaSlicer foundation.

The project aims to combine OrcaSlicer's practical workflow and broad printer support with a conservative, evidence-driven approach to print quality, reliability, and sensible defaults.

## Project goals

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
