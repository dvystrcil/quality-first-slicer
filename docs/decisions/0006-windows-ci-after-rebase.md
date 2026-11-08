# 0006: Windows CI starts right after the 2.5.0 rebase, on GitHub-hosted runners

**Status:** Accepted
**Date:** 2026-11-08
**Decided by:** maintainer
**Answers:** [goals Q8a](../goals.md#7-open-questions-summary)

## Context

Windows x64 is a supported platform ([0001](0001-supported-platforms.md)). The project's self-hosted CI runners are Linux-only. Upstream OrcaSlicer builds Windows x64 on GitHub's `windows-latest` runner in `build_all.yml`, and the fork inherits that workflow. A recent upstream run took about 90 minutes for the app build with cached dependencies. Several planned removals (Expat, Qhull, SLA, mDNS, 3D mouse) touch code that Windows compiles differently. Use-map items R2 and Qhull need Windows evidence before any removal.

## Decision

- **No Windows CI on the 2.4.2 baseline.**
- Enable the inherited upstream Windows x64 job **immediately after the 2.5.0 baseline is green on Linux** ([0002](0002-base-on-orcaslicer-2.5.0.md)), and **before the first removal PR**.
- Run it on GitHub-hosted `windows-latest`. This is a recorded exception to the project's preference for self-hosted runners, because there are no self-hosted Windows nodes. The job gets no secrets, and fork pull requests need maintainer approval, as for the Linux job.

## Alternatives considered

- **From the start, on 2.4.2.** This would spend CI time on a base that is about to be replaced. Rejected.
- **Hand-builds only until v0.1.** Windows breakage from removals would be found late, and R2/Qhull would have no automated evidence. Rejected.
- **Self-hosted Windows runner.** More control, but it adds operations work and security exposure for a public repository. Possible later.

## Consequences

- Each removal PR shows a Windows x64 build result before merge.
- Maintainer hand-testing on Windows remains the physical-validation layer; CI is evidence that the build compiles and tests pass.
- About 90 minutes per run. If that is too slow for every PR, the trigger is narrowed (for example to PRs that touch `deps/`, `deps_src/`, CMake or platform code, plus pushes to the baseline branch), and that change is recorded.

## Revisit when

- a self-hosted Windows runner becomes available;
- GitHub-hosted runner minutes or policy change for public repositories.
