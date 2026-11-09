# Assimp provenance and license review (OrcaSlicer 2.5.0)

**Status:** Source and license-file review of what the 2.5.0 build compiles. Not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off. The keep/optionalize question is [goals Q17](goals.md) and is not answered here.
**Slice:** B1 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (build files identical to upstream v2.5.0 `40ecc66f`)
**Method:** read `deps/Assimp/Assimp.cmake`; extracted the two hash-verified archives ([archive verification](archive-verification.md#250-verification-result)); listed the object files and the `ninja -t deps` header closure of the CI-image deps build (`deps/build/dep_Assimp-prefix`, built by `build_linux.sh -drlL` for the [use map](dependency-use-map.md)); read license files and headers. Linux x86_64 only.
**Reviewed:** 2026-11-09

## 1. Source and pin

| | Primary (CMake ≥ 3.22) | Fallback (CMake < 3.22) |
|---|---|---|
| URL | `https://github.com/assimp/assimp/archive/refs/tags/v5.4.3.tar.gz` | `…/v5.3.1.tar.gz` |
| SHA-256 (declared and verified) | `66dfbaee288f2bc43172440a55d0235dfc7bf885dda6435c038e8000e79582cb` | `a07666be71afe1ad4bc008c2336b7c688aca391271188eb9108d0c6db1be53f1` |
| Tag → commit (GitHub API) | lightweight tag → `c35200e38ea8f058812b83de2ef32c6093b0ece2` | lightweight tag → `6a08c39e3a91ef385e76515cfad86aca4bfd57ff` |
| Evidence | `deps/Assimp/Assimp.cmake:1-7` | same |

Upstream is the canonical `assimp/assimp` repository. No local patch is applied. The build options (`deps/Assimp/Assimp.cmake:20-39`) turn all importers off by default and turn on only **glTF, OBJ and FBX**; exporters, tools, tests and samples are off. `ASSIMP_BUILD_ZLIB` is ON on non-Apple platforms and OFF on macOS (`:14-18`).

The rest of this review covers 5.4.3. For 5.3.1, the root `LICENSE` is byte-identical and `contrib/zlib` is also 1.2.13; the rest of 5.3.1 was not examined.

## 2. What the build compiles

The Linux deps build produced objects for these importers: FBX (15 objects), glTF/glTF2 (3), OBJ (3), plus Assimp's core, which includes a STEP file parser (2 `STEPParser` objects). The third-party code under `contrib/` that was compiled or included:

| `contrib/` dir | In the build as | License file / header (what it says) |
|---|---|---|
| `zlib` (**1.2.13**, `zlib.h:40`) | 15 objects → **separate `libzlibstatic.a`** in the prefix | `contrib/zlib/LICENSE`: zlib license, "(C) 1995-2022 Jean-loup Gailly and Mark Adler" |
| `unzip` (minizip) | 2 objects (`unzip.c`, `ioapi.c`) | Header: Gilles Vollant et al.; decryption code "Copyright (c) 1990-2000 Info-ZIP", "See the accompanying file LICENSE" (`unzip.c:21-26`). **No LICENSE file is present in `contrib/unzip/`** |
| `Open3DGC` | 5 objects | File headers: "Copyright (c) 2013 Khaled Mammou - Advanced Micro Devices, Inc.", MIT-style permission text. No separate license file |
| `openddlparser` | 6 objects | `LICENSE`: MIT, "Copyright (c) 2014 Kim Kulling" |
| `poly2tri` | 5 objects | `LICENSE`: BSD-3-Clause-style, "Copyright (c) 2009-2018, Poly2Tri Contributors" |
| `clipper` | 1 object | `License.txt`: Boost Software License 1.0 |
| `rapidjson` | headers only (108 includes) | `license.txt`: MIT, Tencent and Milo Yip; it names msinttypes (BSD) and `bin/jsonchecker` (JSON License) as third-party parts. `bin/jsonchecker` is not compiled |
| `utf8cpp` | headers only | Header: "Copyright 2006 Nemanja Trifunovic", Boost Software License 1.0 text |

`pugixml` and `stb` are present in the archive but no compiled file in this configuration includes them.

The application links `assimp::assimp` (`libassimp.a`, `src/libslic3r/CMakeLists.txt:629`, `:767`) and, through it, `libzlibstatic.a`. Consumer: `.glb`/`.gltf`/`.fbx` textured import ([use map §3.2](dependency-use-map.md#32-the-six-dependency-projects-added-in-250)).

## 3. Assimp's own license

`LICENSE` (78 lines) is the "Open Asset Import Library (assimp)" license: "Copyright (c) 2006-2021, assimp team", a three-condition BSD-style text (source notice, binary notice in documentation, no-endorsement clause). It adds an exception for `test/models-nonbsd` (not compiled) and appends the Poly2Tri BSD text. GitHub's license detection reports `NOASSERTION` for the repository; that is a detection result, not a license fact.

## 4. The bundled zlib becomes the application's zlib (Linux)

The [use map §3.4](dependency-use-map.md#34-system-libraries-duplicates-and-new-provenance-observations) found that the application's `find_package(ZLIB)` resolves to `<prefix>/lib/libzlibstatic.a`, while the include directory is the system `/usr/include` (zlib 1.3). This review confirms the archive's provenance: the installed `libzlibstatic.a` carries the strings "deflate 1.2.13 Copyright 1995-2022 Jean-loup Gailly and Mark Adler" and "inflate 1.2.13 Copyright 1995-2022 Mark Adler", matching `contrib/zlib` in the verified 5.4.3 archive.

Separately, the bundled CPython's `zlib` and `binascii` modules link the **system** `libz.so.1` ([CPython review](cpython-pybind11-provenance-license-review.md)), so on Linux there are at least two zlib copies in the process.

## 5. Open questions

1. `contrib/unzip` refers to an Info-ZIP `LICENSE` file that is not in the archive. Which terms apply to the decryption code, and whether it is reached by the glTF/OBJ/FBX importers, is not determined.
2. Open3DGC has a license only in file headers. Whether all 5 compiled files carry it was not checked file by file.
3. Notice staging: none of these `contrib/` licenses is installed into the deps prefix or the application bundle by the build files read here. Where release notices would come from is open (same question as for the existing [vendored components](vendored-source-and-patch-inventory.md)).
4. Whether the app's zlib provider (1.2.13 archive, 1.3 headers) is intended upstream, and which archive resolves each `deflate*`/`inflate*` symbol, is not traced.
5. Windows and macOS were not examined. macOS builds without the bundled zlib.

## 6. Approval

**Not approved.** This records what the files say. A maintainer sign-off, and the Q17 keep/optionalize decision, are still needed.
