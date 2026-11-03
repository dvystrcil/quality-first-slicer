# Contributing

Thank you for helping build a quality-first FDM slicer. Contributions should improve correctness, print quality, usability, compatibility, or maintainability without weakening the project's evidence and safety standards.

## Before starting

1. Read [AGENTS.md](AGENTS.md) and the relevant documentation under [docs/](docs/).
2. Check existing issues and pull requests to avoid duplicating or conflicting with active work.
3. For non-trivial changes, propose scope, alternatives, acceptance criteria, and a test plan before implementation.
4. Confirm upstream provenance and licensing before copying or adapting external code, profiles, assets, or documentation.

## Development workflow

1. Create a focused branch for one cohesive change.
2. Establish or update explicit tests before changing behavior (red → green → refactor).
3. Run the relevant baseline and focused tests; then run broader checks appropriate to the affected components.
4. Update documentation and fixtures in the same change.
5. Review the complete diff for accidental changes, lost comments, generated-file churn, secrets, and license notices.
6. Open a pull request with evidence and limitations.

## Pull request contents

A useful PR description includes:

- **Problem and intent:** what is wrong or missing, and why this change is needed.
- **Scope:** affected components and explicitly excluded work.
- **Acceptance criteria:** observable conditions for completion.
- **Implementation:** concise explanation of the approach and relevant alternatives.
- **Validation:** exact commands and observed results, including baseline results where applicable.
- **Compatibility:** affected printers, firmware, profiles, file formats, and upstream behavior.
- **Quality and safety:** implications for motion, extrusion, machine limits, and print quality.
- **Licensing/provenance:** source origin, license review, notices, and new dependencies.
- **Limitations:** untested hardware, unknown commands, or pending evidence.

## Evidence discipline

Do not describe generated G-code as physically validated unless it has been printed and inspected on the stated hardware. Clearly distinguish automated checks, community reports, project-hardware tests, and unverified behavior.

A failing check must be explained, not hidden. If a criterion remains incomplete, mark it pending rather than implying completion.
