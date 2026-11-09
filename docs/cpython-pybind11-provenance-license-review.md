# CPython 3.12.13 and pybind11 provenance and license review (OrcaSlicer 2.5.0)

**Status:** Source, license-file and Linux bundle review. Not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off. The product question is O8 (Python plugin system) in the [use map](dependency-use-map.md#4-ranked-decision-list-re-checked-on-250), and is not decided here. The supply-chain risk of plugins installing packages at runtime is **out of scope** for this license review. Windows build inputs (`source-deps`, `bin-deps`, nuget host Python) and the bundled `uv` binary are slice C.
**Slice:** B5 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (build files identical to upstream v2.5.0 `40ecc66f`)
**Method:** read `deps/python3/python3.cmake`; extracted the hash-verified CPython archive; read the CI-image deps build (`deps/build/dep_python3-prefix`) `Makefile` and its installed `libpython/` tree, `readelf -d` on every extension module; compared every vendored pybind11 file with upstream by Git blob ID through the GitHub API. Linux x86_64 only.
**Reviewed:** 2026-11-09

## 1. CPython: source and build

| | |
|---|---|
| URL | `https://www.python.org/ftp/python/3.12.13/Python-3.12.13.tar.xz` (`deps/python3/python3.cmake:4-7`) |
| SHA-256 (declared and verified) | `c08bc65a81971c1dd5783182826503369466c7e67374d1646519adf05207b684` (`:8`) |
| Linux configure (`:329-339`) | `--enable-shared --enable-optimizations --with-openssl=<prefix> --without-static-libpython --disable-test-modules`, `_tkinter` n/a |
| Installed to | `<prefix>/libpython/` (`bin/`, `include/`, `lib/libpython3.12.so*`, `lib/python3.12/` with 62 extension modules in `lib-dynload/`) |
| Local patches | none to CPython source; `relocate_linux.cmake` rewrites the RUNPATH after install |

Not built on Linux: `_curses`, `_curses_panel`, `_dbm`, `_gdbm`, `nis`, `readline` (their libraries were not found at configure time on the runner), `_tkinter` (n/a), and the test modules (disabled).

## 2. Third-party code in the Linux bundle

| Library | How it gets in | Version / evidence |
|---|---|---|
| OpenSSL | **statically embedded** in `_ssl` and `_hashlib` from the deps prefix | `_ssl` contains "OpenSSL 1.1.1w"; `_hashlib` defines 521 local `EVP_*` symbols and has no `libcrypto` in `NEEDED`; built with hidden visibility for this reason (`deps/OpenSSL/OpenSSL.cmake:57-67`) |
| expat | bundled in CPython (`Modules/expat`, `LIBEXPAT_A` in the `Makefile`) | 2.7.4 (`expat.h`); `Modules/expat/COPYING` |
| libmpdec | bundled in CPython (`Modules/_decimal/libmpdec`, `LIBMPDEC_A`) | 2.5.1 (`mpdecimal.h`) |
| HACL* | bundled in CPython (`Modules/_hacl`) for hash functions | not examined further |
| zlib | **system** `libz.so.1` (`zlib`, `binascii` modules) | runner's library; not the Assimp copy |
| bzip2, xz/lzma, SQLite, libffi, libcrypt, libuuid | **system** shared libraries (`_bz2`, `_lzma`, `_sqlite3`, `_ctypes`, `_crypt`, `_uuid`) | runner's libraries |

Whether the system libraries above are copied into the shipped AppImage, or expected from the user's system, depends on the image script (`src/dev-utils/platform/unix/build_linux_image.sh.in`) and was **not traced**.

## 3. CPython license files

`LICENSE` contains, in order: the **Python Software Foundation License Version 2** (`:73`), the BeOpen.com (`:123`, `:126`), CNRI (`:173`) and CWI (`:244`) agreements for historical versions, and a **Zero-Clause BSD** license for code in the documentation (`:267`). `Doc/license.rst` § "Licenses and Acknowledgements for Incorporated Software" calls itself "an incomplete, but growing list" and lists, among others: Mersenne Twister, SipHash24, strtod and dtoa, OpenSSL, expat, libffi, zlib, cfuhash, libmpdec, the W3C C14N test suite, Audioop and asyncio.

## 4. pybind11 (vendored in `deps_src/pybind11`)

| | |
|---|---|
| What the tree holds | 54 files: `LICENSE`, `README.rst`, `include/pybind11/**` |
| Version | 3.0.1 (`include/pybind11/detail/common.h:20-28`) |
| Upstream match | **All 54 files are byte-identical** (Git blob IDs) to `pybind/pybind11` tag `v3.0.1` → commit `f5fbe867d2d26e4a0a9177a51f6e568868ad3dc8`. No upstream `include/` file is missing. No local modification |
| License | `LICENSE` (29 lines): "Copyright (c) 2016 Wenzel Jakob", BSD-3-Clause-style text with an added paragraph about external contributions |
| How it is used | header-only; root `CMakeLists.txt:1041-1044` defines a minimal `pybind11::embed` target from these headers; 27 app TUs ([use map §3.1](dependency-use-map.md#31-vendored-deps_src-components)) |

## 5. Open questions

1. Which files the Linux image ships (the `libpython` tree, `lib-dynload`, any system `.so`) and which notices go with them.
2. OpenSSL 1.1.1w is embedded in the Python modules as well as linked by the application. OpenSSL 1.1.1 reached upstream end of life in 2023; that is a security and maintenance point, recorded here only because it affects what ships.
3. HACL*, SipHash and the other incorporated code were not reviewed file by file.
4. Windows (`source-deps`, `bin-deps`, nuget host) is slice C3. macOS was not examined.

## 6. Approval

**Not approved.** This records what the files say. A maintainer sign-off, and the O8 product decision, are still needed.
