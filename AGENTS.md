# Agent and Contributor Instructions

This file is the canonical, tool- and model-agnostic guidance for anyone (human or AI) contributing to this repository. Tool-specific instruction files may point here, but must not fork or silently contradict these rules.

## 1. Establish context before acting

- Read this file, the README, relevant architecture/decision records, and the task's acceptance criteria before making changes.
- Inspect the current branch, working tree, relevant files, open pull requests, and review comments before editing.
- Treat the repository as the source of truth. Chat history and model memory are not substitutes for checking current repository state.
- For technical claims, verify against authoritative upstream documentation, source, executable behavior, or reproducible tests. Distinguish verified facts from assumptions.

## 2. Plan, then execute

- For non-trivial work, separate analysis/planning from implementation.
- State scope, affected files/components, risks, test strategy, and acceptance criteria before implementation.
- Once a plan is approved, execute that plan. If new evidence requires a material redesign, stop and explain the change rather than silently changing direction.
- Keep changes small, cohesive, and reviewable. Prefer a sequence of focused commits or pull requests over a broad unreviewable change.

## 3. Protect collaborative work

- Do not overwrite, delete, reformat, or reinterpret another contributor's changes, comments, review notes, or in-progress work without explicit coordination.
- Check repository state immediately before editing and before committing.
- Keep independent work on separate branches. Coordinate overlapping file ownership before modifying shared areas.
- Resolve review comments with evidence; do not erase comments merely to make a review appear complete.
- Preserve attribution, provenance, and license notices.

## 4. Test-driven development and evidence

- For behavior changes, write a focused test first, run it, and confirm that it fails for the intended reason.
- Implement the smallest change that makes the test pass; then run focused tests and relevant broader suites.
- Validate tests against a known-good baseline when the work involves upgrades, migrations, or new validation logic. Fix faulty tests before treating baseline failures as product regressions.
- Tests must assert explicit expected values and meaningful boundary cases, not merely that code executes.
- Test the real downstream consumer/runtime when integration behavior is part of the requirement.
- Do not silently skip, weaken, quarantine, or bypass a failing test. Explain failures and obtain approval for any exception.
- Check reusable scripts, fixtures, and test data into the repository when they are part of the repeatable engineering process.

## 5. Acceptance criteria and completion receipts

For substantial work, define acceptance criteria before implementation. At completion, provide a concise receipt mapping each criterion to evidence and status: PASS, FAIL, or PENDING. Include exact commands, relevant outputs, and limitations. Never claim a test passed unless it was actually run and its result observed.

## 6. Upstream, dependencies, and licensing

- Verify upstream repository, release/tag, commit, and license information before relying on it.
- Do not copy source, profiles, assets, documentation, or code from another project until provenance and applicable license obligations have been reviewed.
- Do not add dependencies, vendor integrations, telemetry, cloud requirements, or proprietary components without documenting the need, license, security impact, and approval.
- Preserve third-party notices and file-level licensing distinctions. A repository-level license does not automatically relicense every dependency or asset.
- Do not make legal conclusions from a project name or a top-level badge; record unresolved questions explicitly.

## 7. Slicer-specific quality and safety principles

- Quality, reliability, and predictable behavior take precedence over headline speed.
- Do not change default speeds, accelerations, flow limits, extrusion behavior, or machine limits without evidence and explicit review.
- Distinguish firmware-reported/mechanical limits, material limits, hotend volumetric-flow limits, and quality-oriented operating ranges.
- G-code analysis and simulation are validation aids, not certified physical safety systems.
- Unknown motion-affecting commands or firmware behavior must be reported as unverified; never silently treat them as safe.
- A negative logical coordinate is not automatically a physical collision. Account for coordinate modes, offsets, transforms, mesh compensation, and machine geometry before drawing conclusions.
- Label validation evidence accurately: automated, community physical validation, project-hardware physical validation, or unverified. Never imply a printer was physically tested when it was not.

## 8. Documentation and decisions

- Update relevant documentation in the same change as behavior or policy changes.
- Record material architectural choices as decision records, including context, alternatives, consequences, and revisit triggers.
- Do not rewrite historical decisions to hide changed direction. Supersede them with a new decision record.
- Keep examples and instructions reproducible and version-aware.

## 9. Git and pull-request hygiene

- Use focused branches and descriptive commits.
- Do not commit secrets, credentials, private user data, or unlicensed material.
- PRs must explain intent, scope, compatibility impact, licensing/provenance implications, tests run, results, and known limitations.
- Do not merge or bypass required checks without explicit authorization.
- If a tool fails or a source becomes unavailable, report that limitation. Do not reconstruct missing current state from memory and present it as verified.

## 10. Working principle

Prefer a small, testable, documented change with repeatable evidence over a large change supported only by explanation. The repository should retain enough context that a different person or agent can continue the work without relying on this conversation.
