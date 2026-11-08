# 0001: Supported platforms

**Status:** Accepted
**Date:** 2026-11-08
**Decided by:** maintainer
**Answers:** [goals Q8](../goals.md#4-platform-matrix)

## Context

The [goals](../goals.md) need a platform matrix. Several pieces of work depend on it:

- the [dependency/use map](../dependency-use-map.md) was configured only on Linux x86_64;
- its R2 (vendored Expat) and vendored-Qhull conclusions depend on how Windows resolves those packages;
- O5 (OpenCV IPP-ICV) applies only to Windows x64;
- macOS has its own sources (`*.mm`, `Mouse3DHandlerMac.mm`) and `deps/deps-macos.cmake`.

The vision requires honest validation labels (principle 5; [AGENTS.md](../../AGENTS.md) §7). A platform nobody on the project can run cannot be validated.

## Decision

| Platform | Status | Testing |
|---|---|---|
| **Linux x86_64, AppImage** | **Supported** | Built on the fork's CI (`linux-arc-baseline.yml`); maintainer can run it |
| **Windows x64** | **Supported** | Maintainer tests by hand. **How it is built in CI is undecided** and tracked separately |
| Linux x86_64, Flatpak | **Future**, not supported yet | — |
| **Linux aarch64** (arm64) | **Future** | Testable by the maintainer on a Raspberry Pi or a Chromebook (Linux container) |
| Windows ARM64 | Not supported | — |
| macOS (arm64 and x86_64) | **Not supported** | Maintainer has no way to test macOS |

"Supported" means the project builds it, releases it, and the maintainer can test it. Nothing ships on a platform the project cannot run.

## Alternatives considered

- **macOS builds in CI, labelled unverified.** This would catch compile breakage cheaply, but the project would ship a product nobody has run, against the validation-honesty principle. It would also need GitHub-hosted macOS runners. Rejected.
- **macOS deferred with a revisit trigger.** Today's work would be the same as "not supported". The revisit triggers below cover this case anyway.
- **Linux aarch64 now.** The maintainer can test it, but CI would need an arm64 runner (the project's self-hosted runners are amd64), and it does not serve v0.1. Recorded as future, not rejected.
- **Flatpak now.** It is a separate packaging and dependency path (`build_flatpak.sh`), and it adds CI work that does not serve v0.1. Left for the future.

## Consequences

- **Use map:** platform caveats now matter only for Windows x64. R2 and the vendored-Qhull decision need a **Windows x64 configure** before any removal PR. The macOS columns in [use map §5](../dependency-use-map.md#5-platform-caveats-for-the-ranked-items) no longer block anything.
- **O5 (OpenCV IPP-ICV)** is in scope, because Windows x64 is supported.
- **macOS code** (`*.mm` sources, `Mouse3DHandlerMac.mm`, `deps/deps-macos.cmake`, the macOS branches in CMake) stays as inherited upstream code. It is not maintained, and no project change needs to keep it building. **This decision removes nothing.** Removing it becomes a candidate under goal G4 (lean) and needs its own PR with evidence. Keeping it keeps rebases onto upstream simple, so the trade-off belongs in that PR.
- **Windows CI build path** (GitHub-hosted runner vs self-hosted Windows runner) is an open follow-up. Until it is decided, a Windows build is hand-built and hand-tested, and its evidence level is recorded accordingly.
- **Release notes and the README** must name the supported platforms. No macOS artifact is published.

## Revisit when

- someone with macOS hardware commits to testing releases;
- Flatpak packaging is requested, or becomes the better way to ship on Linux;
- **Linux aarch64:** an arm64 CI runner is available; hand-testing is already possible on a Raspberry Pi or a Chromebook. The upstream build script already has an aarch64 leg (`build_orca.yml`), so the starting point is known.
