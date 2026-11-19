# `uv` 0.11.21 binary: provenance and license review (OrcaSlicer 2.5.0)

**Status:** Hash, provenance and license review of the prebuilt `uv` executables that the build downloads and installs into the application. Not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off. `uv` exists to install Python packages for plugins, so its keep/remove call goes with O8 (Python plugins) in the [use map](dependency-use-map.md#4-ranked-decision-list-re-checked-on-250), which is not decided here. The supply-chain risk of installing packages at runtime is **out of scope**.
**Slice:** C2 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (root `CMakeLists.txt` identical to upstream v2.5.0 `40ecc66f`)
**Method:** hash-verified all six archives with [`tools/verify-source-archives.py`](../tools/verify-source-archives.py) and the [binary manifest](../audit/orcaslicer-v2.5.0-binary-artifacts.json); compared with each upstream `.sha256` asset and the GitHub asset digests; ran `gh attestation verify --repo astral-sh/uv` on each downloaded file (a signature check that reads the file; nothing was executed); listed each archive. Tag, license and `Cargo.toml` from the GitHub API.
**Reviewed:** 2026-11-19

## 1. Pin and integrity

`ORCA_UV_VERSION "0.11.21"` and one SHA-256 per triple are at root `CMakeLists.txt:135-141`; the URL is `https://github.com/astral-sh/uv/releases/download/0.11.21/uv-<triple>.<tar.gz|zip>` (`:201`).

| Triple | Declared SHA-256 | Bytes | Download | Upstream `.sha256` asset | Attestation |
|---|---|---:|---|---|---|
| `aarch64-apple-darwin` | `1f921d49…bf3f4` | 20,835,123 | **PASS** | same | verified |
| `x86_64-apple-darwin` | `f3c8e570…7765` | 22,349,034 | **PASS** | same | verified |
| `aarch64-unknown-linux-gnu` | `88e80083…2397` | 22,805,727 | **PASS** | same | verified |
| `x86_64-unknown-linux-gnu` | `8c88519b…4050` | 24,437,894 | **PASS** | same | verified |
| `aarch64-pc-windows-msvc` | `74e443f8…2f48` | 21,936,792 | **PASS** | same | verified |
| `x86_64-pc-windows-msvc` | `ace861f3…9589` | 23,452,481 | **PASS** | same | verified |

- The GitHub asset `digest` of each archive equals the declared hash too.
- Every attestation was signed by `https://github.com/astral-sh/uv/.github/workflows/release.yml@refs/heads/main` from source commit **`5aa65dd7ad0067a6b702bf490c8c2ffe25c50f39`**, which is what tag `0.11.21` resolves to ("Bump version to 0.11.21 (#19810)"). The release was published 2026-06-11 18:20:26 UTC.
- The configure step checks the hash itself and refuses to bundle on a mismatch (`:213-219`), with `TLS_VERIFY ON` (`:205`).
- The Flatpak manifest pins the same two Linux archives with the same hashes (`scripts/flatpak/com.orcaslicer.OrcaSlicer.yml:358-367`). Flatpak is not a target platform ([0001](decisions/0001-supported-platforms.md)).

## 2. What ships

| Archive contents | What the build keeps |
|---|---|
| tarballs: `uv-<triple>/uv`, `uv-<triple>/uvx` | `uv` only: renamed to the cache path, the rest of the directory removed (`:229-230`) |
| Windows zips: `uv.exe`, `uvw.exe`, `uvx.exe` at the root | `uv.exe` only is used as `ORCA_BUNDLED_UV_EXECUTABLE` (`:145-148`, `:240`); `uvw.exe` and `uvx.exe` stay in the build-tree cache |

That one executable is installed as `resources/tools/uv/uv[.exe]` on Windows (`:1292-1294`), under the FHS resources dir on Linux (`:1312-1320`) and in `OrcaSlicer.app/Contents/Resources/tools/uv` on macOS (`:1329-1331`). `src/CMakeLists.txt:370-374` also copies it next to the binary for the build-tree and `.app` flows, which do not run `install()`. Setting `ORCA_BUNDLED_UV_EXECUTABLE` replaces the download with any user-supplied file, which is then not hash-checked.

None of the six archives contains a license or notice file.

## 3. License

| Evidence | What it says |
|---|---|
| `Cargo.toml` `[workspace.package]` at `0.11.21` | `license = "MIT OR Apache-2.0"`; `crates/uv/Cargo.toml` inherits it |
| Repository root at `0.11.21` | `LICENSE-APACHE` and `LICENSE-MIT` ("Copyright (c) 2025 Astral Software Inc.") |
| GitHub license detection | Apache-2.0 (it reports one of the two files) |

`uv` is a Rust program statically linking many third-party crates (`Cargo.lock` at the tag). Their licenses were **not enumerated**, and upstream does not ship a third-party notice file in the release archives.

No `uv` license text is installed with the app by the lines above; `git grep -i astral` matches only the root `CMakeLists.txt`, the Flatpak manifest and one `.claude/skills` reference file, so there is no `uv` notice in `resources/`.

## 4. Open questions

1. No license file for `uv` (or for the crates linked into it) is installed with the application.
2. The crate licenses inside the binary were not enumerated (would need `cargo about`/`cargo deny` on `Cargo.lock` at `5aa65dd7`).
3. Keep/remove goes with O8 (Python plugins), a maintainer decision.

## 5. Approval

**Not approved.** This records what the files and release metadata say. A maintainer sign-off is still needed.
