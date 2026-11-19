# Windows binary dependency provenance inventory

**Status:** Inventory, hash and metadata review of the prebuilt Windows binaries committed under `deps/`. Updated for 2.5.0 in slice C4 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55). Not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off. The other 2.5.0 Windows binaries have their own reviews: FFmpeg zips ([C1](ffmpeg-windows-prebuilt-review.md)), `uv` ([C2](uv-binary-review.md)), CPython build inputs ([C3](cpython-windows-build-inputs-review.md)).
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (no differences from upstream v2.5.0 `40ecc66f` under `deps/`). First recorded at v2.4.2 `8500fcdc` on 2026-11-03.
**Method:** `git ls-tree -l` at `665552c1`, and `git diff --stat 8500fcdc 665552c1` over the three directories. Each blob was written out with `git cat-file` into an empty scratch directory and then hashed (SHA-256), with `file`, `strings` (including UTF-16 version resources) and `objdump -p` import tables. Nothing was executed. WebView2 was compared with the official `Microsoft.Web.WebView2` nuget package, which was hash-checked against the nuget.org catalog.
**Reviewed:** 2026-11-19 (v2.4.2 inventory: 2026-11-03)

## 1. Scope and what changed in 2.5.0

The MSVC build does not build GMP or MPFR from the source archives in [the platform dependency matrix](platform-dependency-matrix.md). Under `if (MSVC)` it copies prebuilt files committed under `deps/` (`deps/GMP/GMP.cmake:7-20`, `deps/MPFR/MPFR.cmake:3-17`). The Windows app build copies `libgmp-10.dll`, `libmpfr-4.dll` and `WebView2Loader.dll` for the target architecture next to the executable (root `CMakeLists.txt:1111-1114`) and lists them in `_dll_list` (`:1150-1152`). The WebView2 headers are included by `libslic3r_gui` (`src/slic3r/CMakeLists.txt:942`).

**Nothing in these three directories changed between v2.4.2 and 2.5.0.** `git diff --stat 8500fcdc 665552c1 -- deps/GMP/gmp deps/MPFR/mpfr deps/WebView2` is empty, and every Git blob ID below matches the v2.4.2 inventory. 2.5.0 changed only the **non-MSVC** GMP source pin (6.2.1 → 6.3.0, `deps/GMP/GMP.cmake:62-68`). The MSVC GMP and MPFR binaries are a separate, unchanged set (see §2–3).

One Windows DLL copy was **removed**: v2.4.2 copied `freetype.dll` from the deps prefix into the app (2.4.2 root `CMakeLists.txt:839`, `:874`); 2.5.0 has no `freetype` reference in the root `CMakeLists.txt`, matching FreeType's removal from `deps/` ([delta §4](dependency-delta-2.4.2-to-2.5.0.md#4-removed)). New Windows DLLs from deps (FFmpeg, CPython's libffi/OpenSSL) are covered by C1 and C3.

None of these files has a hash pin in the build files, so they are not in either audit manifest. Their integrity rests on the Git tree.

## 2. GMP prebuilt files

| File | Bytes | Git blob ID | SHA-256 | Metadata |
|---|---:|---|---|---|
| `deps/GMP/gmp/include/gmp.h` | 86,227 | `4209aa8b…` | `6b7a4c57…9e6d6505` | `__GNU_MP_VERSION` 5 / `_MINOR` 0 / `_PATCHLEVEL` 1 (`:2274-2276`) = **5.0.1** |
| `…/lib/win-x64/libgmp-10.dll` | 543,027 | `f92b2892…` | `fec43cb1…3013f009` | PE32+ x86-64; version resource "GNU MP Library", FileVersion **5.0.1.0**, "Free Software Foundation, Inc."; mingw runtime strings; imports `KERNEL32`, `msvcrt` |
| `…/lib/win-x64/libgmp-10.lib` | 109,180 | `ed354723…` | `63fbb59c…2f486f0f` | import library |
| `…/lib/win-x86/libgmp-10.dll` | 498,827 | `387656ca…` | `9be85bd8…bbfa5f20` | PE32 i386; FileVersion **5.0.1.0**; imports `KERNEL32`, `msvcrt` |
| `…/lib/win-x86/libgmp-10.lib` | 114,286 | `53bb34cc…` | `9674fa6d…c38fc533` | import library |
| `…/lib/win-arm64/libgmp-10.dll` | 541,696 | `ea927b54…` | `bfc6046e…a961f47c` | PE32+ ARM64; no version resource; contains the string **`6.3.0`**; imports UCRT (`api-ms-win-crt-*`) and `KERNEL32` |
| `…/lib/win-arm64/libgmp-10.lib` | 125,174 | `afc8909b…` | `cdd06f16…cc7f3cea` | import library |

Full SHA-256 values:

```text
6b7a4c57b819b6c5af8f8255c6e8800694c1b53b8f8e09c167e7d3779e6d6505  deps/GMP/gmp/include/gmp.h
fec43cb18ce0ec8a5dd6ad1db745747167310ccb92b5acff0d445a8b3013f009  deps/GMP/gmp/lib/win-x64/libgmp-10.dll
63fbb59cd3b7879f71cf2d3d9133f6edcd6d6afb122a1fff085afb7c2f486f0f  deps/GMP/gmp/lib/win-x64/libgmp-10.lib
9be85bd8468363703304d0bbd059c9709dba270d0ff5a1a94823cb5dbbfa5f20  deps/GMP/gmp/lib/win-x86/libgmp-10.dll
9674fa6d52911540f62f332a9791413a6bbbb178769e9138e0013a3bc38fc533  deps/GMP/gmp/lib/win-x86/libgmp-10.lib
bfc6046e374a27838b54bde5602851c7cc426ac9438cb65f019b9e67a961f47c  deps/GMP/gmp/lib/win-arm64/libgmp-10.dll
cdd06f164485e6ca4bd826ce5e004aa56fba238e27aaeb65c2648203cc7f3cea  deps/GMP/gmp/lib/win-arm64/libgmp-10.lib
8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903  deps/GMP/gmp/gmp.COPYING
92903b0c50dab829a85c606ca1617984410f565a76ab160b7a1262fe218f13cc  deps/GMP/gmp/gmp.README
```

**The Windows GMP binaries are not the GMP version the other platforms build.** x64 and x86 are GMP **5.0.1** (2010-era, mingw-built against `msvcrt`). ARM64 is a different build that reports **6.3.0** and links the UCRT. The one shared `gmp.h` is the 5.0.1 header. The ARM64 files were added by upstream commit `dbd9c22d80` ("native Windows ARM64 build support", 2026-06-25, before v2.4.2). The build of none of the three is documented.

Notices: `gmp.COPYING` (35,147 bytes) is the GPL v3 text, the same bytes as FFmpeg's `LICENSE.txt` in C1. `gmp.README` (3,979 bytes) opens with an LGPL v3-or-later header. At `:41` it says the library is under "COPYING.LIB and COPYING (most of GNU MP is under the former, some under the latter)". **There is still no `COPYING.LIB` / LGPL text** in `deps/GMP/gmp/`, as found at v2.4.2.

## 3. MPFR prebuilt files

| File | Bytes | Git blob ID | SHA-256 | Metadata |
|---|---:|---|---|---|
| `deps/MPFR/mpfr/include/mpfr.h` | 45,657 | `d330e33f…` | `05d2d1c3…31e7fd95` | `MPFR_VERSION_MAJOR/MINOR/PATCHLEVEL` 3/0/0 (`:27-29`) = **3.0.0** |
| `deps/MPFR/mpfr/include/mpf2mpfr.h` | 6,282 | `0d1a4ee1…` | `656ee5c6…4266dacf` | |
| `…/lib/win-x64/libmpfr-4.dll` | 436,011 | `fea68a1c…` | `09b3b868…391ed927` | PE32+ x86-64; "GNU MPFR Library" FileVersion **3.0.0.0**, string `3.0.0`; imports `libgmp-10`, `KERNEL32`, `msvcrt` |
| `…/lib/win-x64/libmpfr-4.lib` | 68,992 | `8a1263c5…` | `db89bd46…bd2547dc` | import library |
| `…/lib/win-x86/libmpfr-4.dll` | 431,519 | `73a0c801…` | `5a72d472…a3d0f55b` | PE32 i386; FileVersion **3.0.0.0** |
| `…/lib/win-x86/libmpfr-4.lib` | 70,696 | `7b0ad8d2…` | `6f197ddc…1efe384a` | import library |
| `…/lib/win-arm64/libmpfr-4.dll` | 455,168 | `b1188e25…` | `1d40ba1c…0fe09f12` | PE32+ ARM64; no version resource; string **`4.2.2`**; imports `libgmp-10` + UCRT |
| `…/lib/win-arm64/libmpfr-4.lib` | 85,824 | `9031499e…` | `a2aeeae2…0de229a8` | import library |

```text
05d2d1c356fe541c67ba8660efc0384fe56714149cff2bd896c387e931e7fd95  deps/MPFR/mpfr/include/mpfr.h
656ee5c68af6e0b76ed08c5c919ab0f51b8670207f4499c30a55fcf04266dacf  deps/MPFR/mpfr/include/mpf2mpfr.h
09b3b868b96433991fc15c9c5ae6f9a44c62d2e21194110442607917391ed927  deps/MPFR/mpfr/lib/win-x64/libmpfr-4.dll
db89bd46fcbbd99b56197284e5593b3f9ce744ccb8ead9aebee9b714bd2547dc  deps/MPFR/mpfr/lib/win-x64/libmpfr-4.lib
5a72d472e892efd7d94ea287eda354637394805c2f445edec051b5c0a3d0f55b  deps/MPFR/mpfr/lib/win-x86/libmpfr-4.dll
6f197ddc372b946a4c2ba211406892d355a5cd5e74ee72fe694f8b5d1efe384a  deps/MPFR/mpfr/lib/win-x86/libmpfr-4.lib
1d40ba1c45f7d50db814dc6a1ddb8bb3d4d50ade6905b77d39bc764f0fe09f12  deps/MPFR/mpfr/lib/win-arm64/libmpfr-4.dll
a2aeeae2225c566e80b3ad2a0c4125e149931cdb49b377679488b4790de229a8  deps/MPFR/mpfr/lib/win-arm64/libmpfr-4.lib
8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903  deps/MPFR/mpfr/mpfr.COPYING
a853c2ffec17057872340eee242ae4d96cbf2b520ae27d903e1b2fef1a5f9d1c  deps/MPFR/mpfr/mpfr.COPYING.LESSER
2e6f4a0acca5bdfd450409d294e187db48413bf71ac2b4fec3fe9a3287ac505e  deps/MPFR/mpfr/mpfr.README
```

As with GMP, x64/x86 are MPFR **3.0.0** and ARM64 is **4.2.2** (the version the source build uses). The header is 3.0.0. Notices: `mpfr.README` (LGPL v3 or later, "Copyright 2000, …, 2010 Free Software Foundation, Inc."), `mpfr.COPYING` (GPL v3), `mpfr.COPYING.LESSER` (LGPL v3).

## 4. WebView2 loader and SDK headers

| File | Bytes | Git blob ID | SHA-256 | Matches nuget package file |
|---|---:|---|---|---|
| `deps/WebView2/lib/win-arm64/WebView2Loader.dll` | 144,960 | `218b485a…` | `ed612efe…7ce705ba` | **yes** (`build/native/arm64/`, `runtimes/win-arm64/native/`) |
| `…/win-arm64/WebView2Loader.dll.lib` | 2,916 | `15b5a0ae…` | `d70271da…e205e9a2` | **yes** |
| `…/win-arm64/WebView2LoaderStatic.lib` | 10,394,166 | `de2300a2…` | `f7493843…501ca336` | **yes** |
| `…/win-x64/WebView2Loader.dll` | 159,296 | `b19f4b0e…` | `2d64a312…ff00b493` | **yes** |
| `…/win-x64/WebView2Loader.dll.lib` | 2,916 | `226d62a7…` | `bfc8ccaa…d8e15c6d` | **yes** |
| `…/win-x64/WebView2LoaderStatic.lib` | 10,392,690 | `5d0471f8…` | `48d4cbe7…e56b4a25` | **yes** |
| `…/win-x86/WebView2Loader.dll` | 119,904 | `0a1a8fe6…` | `b97b715f…1030b4d7` | **yes** |
| `…/win-x86/WebView2Loader.dll.lib` | 2,998 | `b8410e87…` | `a3ec0ee5…5dffad49` | **yes** |
| `…/win-x86/WebView2LoaderStatic.lib` | 10,357,404 | `4515c0a6…` | `c4668b7c…b130dcf4` | **yes** |
| `deps/WebView2/include/WebView2.h` | 2,563,185 | `7f76a136…` | `9388685f…94ff6f1b` | equal after CRLF→LF |
| `deps/WebView2/include/WebView2EnvironmentOptions.h` | 18,600 | `4156372c…` | `0504ee85…0c0e3160` | equal after CRLF→LF |

The full digests of the nine library files are those of the package files listed in §4.1. Each was compared byte for byte by SHA-256. The two headers are LF in the tree and CRLF in the package, and are identical once line endings are normalised.

### 4.1 Source: `Microsoft.Web.WebView2` 1.0.3351.48

| | |
|---|---|
| Version evidence | each `WebView2Loader.dll` version resource: "Microsoft Edge Embedded Browser WebView Loader", FileVersion **1.0.3351.48**, "Copyright Microsoft Corporation"; `WebView2EnvironmentOptions.h:28` `CORE_WEBVIEW_TARGET_PRODUCT_VERSION L"138.0.3351.48"`; upstream commit `05181779d1` "Update WebView2 to 1.0.3351.48 (#10239)" |
| Package | `https://api.nuget.org/v3-flatcontainer/microsoft.web.webview2/1.0.3351.48/microsoft.web.webview2.1.0.3351.48.nupkg`, SHA-256 `ad98e9d951361e62b6edc137273ec1787242c5c28539c1a101f98a1e07d060f9`; its SHA-512 equals the nuget.org catalog `packageHash`; published 2025-07-01; authors "Microsoft" |
| License | the package declares `licenseFile` `LICENSE.txt` (1,487 bytes): "Copyright (C) Microsoft Corporation. All rights reserved.", followed by a three-clause BSD-style redistribution text |
| Notices | the package also ships `NOTICE.txt` ("NOTICES AND INFORMATION … This software incorporates material from third parties"). **Neither file is in `deps/WebView2/`** |

The loader DLLs import only `KERNEL32`. The WebView2 **runtime** (Edge) is a separate Microsoft component that the loader finds on the user's system. Its licensing and update behaviour were not reviewed here.

## 5. Follow-up evidence (from the v2.4.2 list)

- [x] SHA-256, file type, architecture, version and import tables for every tracked binary (§2–4).
- [ ] Identify the build process and source of the GMP and MPFR binaries. Partly done: versions identified (x64/x86: GMP 5.0.1 / MPFR 3.0.0; ARM64: 6.3.0 / 4.2.2), but who built them and how is still not documented.
- [ ] Resolve the missing GMP `COPYING.LIB`. Still missing at 2.5.0.
- [x] Identify the WebView2 SDK package and its license: `Microsoft.Web.WebView2` 1.0.3351.48; binaries byte-identical; `LICENSE.txt` and `NOTICE.txt` recorded (§4.1). Neither is in the tree.
- [ ] WebView2 runtime licensing and update behaviour.
- [x] Which files reach the app: one `libgmp-10.dll`, one `libmpfr-4.dll` and one `WebView2Loader.dll` per architecture (§1). Whether the installer adds notices was not traced.
- [ ] Include these binaries and their license texts in the eventual SBOM and third-party notices.
- [ ] Do not redistribute these binaries from the new project until their provenance and license conditions are reviewed.

## 6. Open questions

1. **Version split:** x64/x86 Windows builds use GMP 5.0.1 and MPFR 3.0.0. ARM64 and every non-Windows platform use GMP 6.3.0 and MPFR 4.2.2. All Windows architectures compile against the 5.0.1 / 3.0.0 headers. This is a provenance and maintenance point; whether it matters functionally (for example CGAL's exact arithmetic) was not tested.
2. The build provenance of all six GMP/MPFR DLLs is undocumented in the tree.
3. The GMP LGPL text named by `gmp.README` is still absent.
4. The WebView2 `LICENSE.txt` and `NOTICE.txt` from the package are not in `deps/WebView2/`, and no notice for these DLLs was found in the tree.

## 7. Approval

**Not approved.** This records what the files say. A maintainer sign-off is still needed.
