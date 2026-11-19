# CPython Windows build inputs: provenance and license review (OrcaSlicer 2.5.0)

**Status:** Hash, provenance and license review of what the Windows CPython 3.12.13 build downloads besides the CPython source: the `cpython-bin-deps` prebuilt libffi and OpenSSL, the `cpython-source-deps` archives, and the build-time nuget host Python. Not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off. The CPython source itself, pybind11 and the Linux bundle are [B5](cpython-pybind11-provenance-license-review.md). O8 (Python plugins) is not decided here.
**Slice:** C3 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (build files identical to upstream v2.5.0 `40ecc66f`)
**Method:** hash-verified the four binary inputs with [`tools/verify-source-archives.py`](../tools/verify-source-archives.py) and the [binary manifest](../audit/orcaslicer-v2.5.0-binary-artifacts.json), and re-verified the four `source-deps` archives from the [source manifest](../audit/orcaslicer-v2.5.0-source-archives.json); resolved each commit against the upstream tag of the same name and against CPython's own `PCbuild/get_externals.bat` at `v3.12.13`; compared the nuget packages with the nuget.org catalog; listed every archive and read its license files and `.nuspec`. Nothing was executed. **No Windows build was run**, so "what ships" comes from reading `deps/python3/` and CPython's `PC/layout` and `PCbuild/regen.targets`, not from an installed tree.
**Reviewed:** 2026-11-19

## 1. Pins and integrity

All are declared in `deps/python3/python3.cmake`: the six externals as `repo folder commit sha256` rows at `:93-101`, fetched from `https://github.com/python/cpython-<repo>/archive/<commit>.zip` (`:114`); the host Python at `:27-47`.

| Input | Commit / version | Same as upstream tag? | Declared SHA-256 | Result |
|---|---|---|---|---|
| `bin-deps` libffi-3.4.4 | `94cb9a1c7feb608adf2b9f8fe2dbd6925ffbf90d` | tag `libffi-3.4.4` → same commit | `6b0f5349…a877ca` | **PASS** (102,848 bytes) |
| `bin-deps` openssl-bin-3.0.16.2 | `1174fd43d858425c345b16d631716fb98ba492ea` | tag `openssl-bin-3.0.16.2` → same | `b741fd14…118a63b` | **PASS** (25,016,781 bytes) |
| `source-deps` bzip2-1.0.8 | `05301997b2f9590f49c672cf3dfd3d3dfa7ad521` | tag → same | `44b15bed…785fe5` | **PASS** |
| `source-deps` sqlite-3.49.1.0 | `cb7a3997059739fe9c63b2819aeda7c6907510ef` | tag → same | `586fe469…6d6759` | **PASS** |
| `source-deps` xz-5.2.5 | `c6bc0c612605622aaef101a33a751f9de2ecc193` | tag → same | `d99882a8…dc0bf` | **PASS** |
| `source-deps` zlib-1.3.1 | `4dc98e1909830e2bdc2a9cc2236e3c5d5037335b` | tag → same | `39d867c0…f50c` | **PASS** |
| nuget `pythonx86` 3.13.16 | `.nuspec` repository commit `cbc944f` | `v3.13.16` → `cbc944f4bc59…` | `c65cf476…dd15` | **PASS** (13,540,783 bytes); SHA-512 equals the nuget.org catalog `packageHash` |
| nuget `pythonarm64` 3.13.16 | same | same | `bfd77aa5…1694a` | **PASS** (14,172,486 bytes); SHA-512 equals the catalog `packageHash` |

The six externals are exactly the set CPython's own `PCbuild/get_externals.bat` at `v3.12.13` names for a build without Tkinter and with prebuilt OpenSSL/libffi: libraries `bzip2-1.0.8`, `sqlite-3.49.1.0`, `xz-5.2.5`, `zlib-1.3.1` (`:54-62`) and binaries `libffi-3.4.4`, `openssl-bin-3.0.16.2` (`:79-80`). The OrcaSlicer build passes `--no-tkinter` (`python3.cmake:174`) and supplies these through `EXTERNALS_DIR` (`:129`) instead of letting `get_externals.bat` download them.

## 2. `bin-deps`: prebuilt libraries

`python/cpython-bin-deps` is the CPython project's repository of "Binaries that the cpython build process depends on" (its `README.md`). The repository has no license metadata of its own; license text sits beside each binary.

| Archive | Contents (all three of `amd64/`, `arm64/`, `win32/`) | License file |
|---|---|---|
| libffi-3.4.4 | `libffi-8.dll`, `libffi-8.lib`, headers | `LICENSE` at the root: "libffi - Copyright (c) 1996-2022 Anthony Green, Red Hat, Inc and others", MIT-style permission text |
| openssl-bin-3.0.16.2 | `libcrypto-3[-arm64].dll`, `libssl-3[-arm64].dll`, import libs, `.pdb`, headers | `LICENSE.txt` per architecture: **Apache License 2.0** (10,352 bytes) |

Who built these binaries and from which exact source is not stated in the archives. Source of the same versions is in `cpython-source-deps` (`get_externals.bat` lists `libffi-3.4.4` and `openssl-3.0.16` as source options), but the binaries were **not** compared with it.

**Windows differs from Linux here.** On Linux (B5) OpenSSL **1.1.1w** is statically embedded in `_ssl`/`_hashlib`, and libffi comes from the system. On Windows, `_ssl`, `_hashlib` and `_ctypes` load these **OpenSSL 3.0.16** and libffi 3.4.4 DLLs.

## 3. `source-deps`: compiled from source

| Archive | License evidence in the archive |
|---|---|
| bzip2-1.0.8 | `LICENSE`: "copyright (C) 1996-2019 Julian R Seward", BSD-style conditions |
| sqlite-3.49.1.0 | No license file. `sqlite3.c` (amalgamation, version 3.49.1) carries the SQLite "blessing" in place of a legal notice (`:36` onward) |
| xz-5.2.5 | `COPYING`: "liblzma is in the public domain"; other parts (tools, scripts) under LGPLv2.1+/GPLv2+/GPLv3 per that file; `COPYING.GPLv2`, `COPYING.GPLv3`, `COPYING.LGPLv2.1` present |
| zlib-1.3.1 | `LICENSE`: "(C) 1995-2022 Jean-loup Gailly and Mark Adler", zlib license |

CPython's PCbuild compiles only the library parts it needs (liblzma, libbz2, sqlite3, zlib); which files from each archive are compiled was not traced.

## 4. nuget host Python (build time only)

Used only to run CPython's `PCbuild` scripts; the comment at `python3.cmake:12` says it is "pinned because 3.15 cannot run the 3.12 scripts". It is skipped when `DEP_PYTHON_HOST` is set (`:13-25`). The package is extracted to `dep_python3_host-prefix` and `tools/python.exe` is used as `PYTHON` (`:47`, `:128`). Nothing in `deps/python3/` copies it into the deps prefix or the app.

| | |
|---|---|
| Package | `pythonx86` on non-ARM64 hosts (a **32-bit** Python, even on x64 hosts), `pythonarm64` on ARM64 hosts (`:28-34`) |
| `.nuspec` | authors "Python Software Foundation", `<license type="file">tools\LICENSE.txt</license>`, repository `https://github.com/Python/CPython.git` commit `cbc944f` (= tag `v3.13.16`) |
| Contents | a full CPython 3.13.16 runtime (`python.exe`, `python313.dll`, 25 `DLLs/`, 1,033 `Lib/` files, `vcruntime140.dll`), **pip 26.2.1** in `site-packages`, a `.signature.p7s` package signature (not verified) |
| License | `tools/LICENSE.txt` (33,861 bytes); pip and its vendored packages carry their own license files |
| Published | nuget.org catalog: 2026-09-30 (both packages) |

## 5. What ships on Windows (from the build files, not an installed tree)

`stage_windows.cmake` runs CPython's own `PC/layout` with `--include-dev` into `<prefix>/libpython` (`python3.cmake:176-183`). At `v3.12.13`, `PC/layout/main.py` treats `libcrypto*`, `libssl*` and `libffi*` as required DLLs (`:50`) and copies `LICENSE.txt` from the build directory (`:171`). PCbuild's `_RegenLicense` (`PCbuild/regen.targets:115-146`) writes that `LICENSE.txt` by concatenating CPython's `LICENSE`, `PC/crtlicense.txt`, bzip2's `LICENSE`, libffi's `LICENSE` and OpenSSL's `LICENSE.txt`. If it is missing, `stage_windows.cmake` copies CPython's plain `LICENSE` instead.

So, as read: the libffi and OpenSSL DLLs from `bin-deps` ship, and an aggregated license file probably goes with them. Whether the app's Windows packaging then copies the staged `libpython` tree, and which `LICENSE.txt` actually ends up in it, were **not verified**. The xz, sqlite and zlib texts are not in the `_RegenLicense` list.

## 6. Open questions

1. Build provenance of the `bin-deps` DLLs (who built them, from which source and toolchain) is not documented in the archives.
2. OpenSSL differs by platform: 3.0.16 DLLs on Windows, static 1.1.1w on Linux (B5 open question 2).
3. Confirm on a real Windows build which `LICENSE.txt` ends up in the shipped `libpython` tree and whether the packaging includes it.
4. The nuget package signature was not verified; the hash and catalog SHA-512 match.

## 7. Approval

**Not approved.** This records what the files say. A maintainer sign-off is still needed.
