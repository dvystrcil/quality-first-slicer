# Windows binary dependency provenance inventory

> **Pinned to v2.4.2.** The 2.5.0 baseline changes this picture; what changed is listed in the [2.4.2 → 2.5.0 dependency delta](dependency-delta-2.4.2-to-2.5.0.md). This document is updated for 2.5.0 in slice C4 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55); until then, read it as the v2.4.2 record.

**Status:** Remote Git-tree and metadata inventory only; binaries have not been downloaded or inspected  
**Upstream baseline:** OrcaSlicer v2.4.2, commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**Reviewed:** 2026-11-03

## 1. Scope

The MSVC build does not build every dependency from the source archives listed in [the platform dependency matrix](platform-dependency-matrix.md). In particular, GMP and MPFR use prebuilt architecture-specific files committed under `deps/`, and the Windows package copies WebView2 loader DLLs. This inventory identifies those tracked files and records their Git tree metadata.

The 40-character object IDs below are Git blob IDs, **not SHA-256 digests of the file contents**. They identify the blobs in the fixed upstream Git tree but are not a substitute for downloading the files and calculating SHA-256.

## 2. GMP prebuilt files

The MSVC branch of `deps/GMP/GMP.cmake` copies `gmp.h`, an import library, and a DLL from `deps/GMP/gmp` based on `DEPS_ARCH`.

| File | Size (bytes) | Git blob ID |
|---|---:|---|
| `deps/GMP/gmp/include/gmp.h` | 86,227 | `4209aa8b3ae813f694883d96c8fdc973362f2fbe` |
| `deps/GMP/gmp/lib/win-arm64/libgmp-10.dll` | 541,696 | `ea927b544e9d4daae6b69a63517496de2e7c0031` |
| `deps/GMP/gmp/lib/win-arm64/libgmp-10.lib` | 125,174 | `afc8909bbe65534cba673551da84a32a4e266f7d` |
| `deps/GMP/gmp/lib/win-x64/libgmp-10.dll` | 543,027 | `f92b2892138b2e71ee8da3cdd5bd1a527cbfe786` |
| `deps/GMP/gmp/lib/win-x64/libgmp-10.lib` | 109,180 | `ed35472388f1a413aee96187464844e95d1a105c` |
| `deps/GMP/gmp/lib/win-x86/libgmp-10.dll` | 498,827 | `387656ca84e3e892ebca78d5af7d5df71a2f6a5e` |
| `deps/GMP/gmp/lib/win-x86/libgmp-10.lib` | 114,286 | `53bb34cc961463ef2d356abd235ee6b95da1d3df` |

Tracked notices and metadata:

- `deps/GMP/gmp/gmp.README` (3,979 bytes; Git blob `03ffb7ff300fcaea7d908625c16650218f065075`)
- `deps/GMP/gmp/gmp.COPYING` (35,147 bytes; Git blob `94a9ed024d3859793618152ea559a168bbcbb5e2`)

The README states that most of GNU MP is under the GNU LGPL and some portions under the GNU GPL, and refers to both `COPYING.LIB` and `COPYING`. The tracked directory inventory at this tag contains `gmp.COPYING` but no `gmp.COPYING.LIB`. This is a concrete notice/provenance gap to resolve; do not infer that the one tracked GPL text fully satisfies the library's licensing and redistribution notices. Confirm the exact upstream GMP 6.2.1 license files and whether the binary bundle was built from that source/version.

## 3. MPFR prebuilt files

The MSVC branch of `deps/MPFR/MPFR.cmake` copies headers, import libraries, and DLLs from `deps/MPFR/mpfr`.

| File | Size (bytes) | Git blob ID |
|---|---:|---|
| `deps/MPFR/mpfr/include/mpfr.h` | 45,657 | `d330e33f7d9407df46d4ee3a32e65b96e8f184b7` |
| `deps/MPFR/mpfr/include/mpf2mpfr.h` | 6,282 | `0d1a4ee1ede7f645789ddbed945b2a24b5feb9f9` |
| `deps/MPFR/mpfr/lib/win-arm64/libmpfr-4.dll` | 455,168 | `b1188e25c07982c9ee7f48daa605b5caf030bc85` |
| `deps/MPFR/mpfr/lib/win-arm64/libmpfr-4.lib` | 85,824 | `9031499e7df88cf24e713ac3fb924dee76a081f2` |
| `deps/MPFR/mpfr/lib/win-x64/libmpfr-4.dll` | 436,011 | `fea68a1c2e814168d049fc45ef438d959934aba1` |
| `deps/MPFR/mpfr/lib/win-x64/libmpfr-4.lib` | 68,992 | `8a1263c50975d4accc637f77e3eb99a0bc012f6c` |
| `deps/MPFR/mpfr/lib/win-x86/libmpfr-4.dll` | 431,519 | `73a0c801d607a63e236afd28924a4253ed350205` |
| `deps/MPFR/mpfr/lib/win-x86/libmpfr-4.lib` | 70,696 | `7b0ad8d2bd86b6896be3a68b25b10faf0dc05c80` |

Tracked notices and metadata:

- `deps/MPFR/mpfr/mpfr.README` (4,054 bytes; Git blob `45a575f39210176f228e2bcae44fe38aa86dd298`)
- `deps/MPFR/mpfr/mpfr.COPYING` (35,147 bytes; Git blob `94a9ed024d3859793618152ea559a168bbcbb5e2`)
- `deps/MPFR/mpfr/mpfr.COPYING.LESSER` (7,639 bytes; Git blob `fc8a5de7edf437cdc98a216370faf7c757279bcb`)

The README identifies MPFR as LGPL v3 or later and describes an exception for certain autotools files. The tracked license files include GPL-3.0 and LGPL-3.0 texts. This is a preliminary notice inventory, not a complete review of MPFR's file-level licensing or the prebuilt binaries' build provenance.

## 4. WebView2 loader files

The v2.4.2 tree contains the following architecture-specific loader and import-library files:

| File | Size (bytes) | Git blob ID |
|---|---:|---|
| `deps/WebView2/lib/win-arm64/WebView2Loader.dll` | 144,960 | `218b485a68caf50ef42cf09f18ac0b5068634357` |
| `deps/WebView2/lib/win-arm64/WebView2Loader.dll.lib` | 2,916 | `15b5a0ae4996a724b4fd0c720f700f8f9db6a6fa` |
| `deps/WebView2/lib/win-arm64/WebView2LoaderStatic.lib` | 10,394,166 | `de2300a23098e0e65e27e1b7cbe8ad8efe7d2043` |
| `deps/WebView2/lib/win-x64/WebView2Loader.dll` | 159,296 | `b19f4b0ee71deff73fc9cafdcabe1467dd01dd04` |
| `deps/WebView2/lib/win-x64/WebView2Loader.dll.lib` | 2,916 | `226d62a73174e8ca23fb36bfe69c85d2b36ccf9e` |
| `deps/WebView2/lib/win-x64/WebView2LoaderStatic.lib` | 10,392,690 | `5d0471f8d011bb500acc7efc4a3f4423626af855` |
| `deps/WebView2/lib/win-x86/WebView2Loader.dll` | 119,904 | `0a1a8fe67500e8f09dc975f1dadaf88a2f497146` |
| `deps/WebView2/lib/win-x86/WebView2Loader.dll.lib` | 2,998 | `b8410e8780eb79dcd8d462c8db39945da85cf68b` |
| `deps/WebView2/lib/win-x86/WebView2LoaderStatic.lib` | 10,357,404 | `4515c0a630a59110d4b5875dac82d6f1a5a525a2` |

The tree also contains WebView2 SDK headers (`WebView2.h`, 2,563,185 bytes; `WebView2EnvironmentOptions.h`, 18,600 bytes). The `deps/WebView2` subtree did not expose a dedicated license, version manifest, package lock, or origin record in this inventory. This does not prove that no applicable license is present elsewhere in the upstream repository or SDK distribution; it means the provenance is not established by the inspected subtree.

## 5. Required follow-up evidence

- [ ] Download each tracked binary and calculate SHA-256; record file type, architecture, version, and PE metadata.
- [ ] Identify the exact upstream packages/releases and build process used for GMP and MPFR binaries; compare DLL exports and versions against official source builds.
- [ ] Resolve the missing GMP `COPYING.LIB` reference and capture all license/exception notices for the exact distributed files.
- [ ] Identify the WebView2 SDK package version and source (for example, the precise Microsoft package/release), and obtain the applicable redistribution license and notices.
- [ ] Verify whether WebView2 runtime installation or only the loader is expected; document the runtime's separate licensing and update behavior.
- [ ] Confirm which of these files are actually copied into release artifacts for each Windows architecture.
- [ ] Include binary files and license texts in the eventual SBOM and third-party notices.
- [ ] Do not redistribute these binaries from the new project until their provenance and license conditions have been reviewed.

## 6. Conclusion

The MSVC path includes a meaningful set of committed binary dependencies, not just source downloads. The GMP and MPFR binary bundles carry some license texts, but GMP's own README references a LGPL notice file that is not present in the inspected directory. WebView2 loader binaries and SDK headers are present without an obvious local provenance/notice record in that subtree. These are specific audit tasks, not grounds to assume the binaries are unlicensed or non-redistributable.
