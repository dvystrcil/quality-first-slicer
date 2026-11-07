# MD4C 0.5.2 provenance and license review

**Status:** Targeted source/provenance review; source-level delta and release-notice staging remain open  
**Reviewed upstream revision:** OrcaSlicer v2.4.2 commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**Upstream component reference:** `mity/md4c` tag `release-0.5.2`, tag commit `729e6b8b320caa96328968ab27d7db2235e4fb47`  
**Scope:** MD4C vendored subtree, its CMake integration, and the application release-note call site  
**Method:** GitHub source/blob comparison and commit-history inspection. No local build, binary/package inspection, or legal determination was performed.

## 1. Findings

- OrcaSlicer imports MD4C in commit [`0683013a7e797d8da43f4f84110f3d88cca3aac6`](https://github.com/OrcaSlicer/OrcaSlicer/commit/0683013a7e797d8da43f4f84110f3d88cca3aac6), dated 2026-02-11, authored by Ocraftyone. The commit adds the complete `deps_src/md4c` subtree, adds it to `deps_src/CMakeLists.txt`, links `md4c-html` into `libslic3r_gui`, and integrates it into the release-note dialog.
- The vendored CMake project declares MD4C version **0.5.2**. The corresponding upstream tag is `release-0.5.2`, commit `729e6b8b320caa96328968ab27d7db2235e4fb47`. The README also describes CommonMark 0.31, consistent with the 0.5.2 release notes.
- The MIT license file is present and byte-identical to the upstream tag's `LICENSE.md`. It identifies copyright © 2016–2024 Martin Mitáš and contains the full MIT grant, conditions, and disclaimer.
- Five of the six reviewed parser/renderer source and header files are byte-identical to the upstream 0.5.2 tag: `md4c.h`, `md4c-html.c`, `md4c-html.h`, `entity.c`, and `entity.h`. The sixth, `md4c.c`, is modified. The vendored `src/CMakeLists.txt` is also modified.
- MD4C is actively used: `src/slic3r/GUI/ReleaseNote.cpp` calls `md_html()` to convert release-note Markdown to HTML. `libslic3r_gui` links `md4c-html`; the MD4C CMake target links `md4c`.
- The local CMake changes comment out upstream install rules for both libraries, public headers, pkg-config files, and the CMake export. The component's `LICENSE.md` remains in the source tree, but no corresponding application release-notice staging was established in this review.

## 2. Source comparison

### 2.1 Exact upstream matches

| File | OrcaSlicer v2.4.2 blob | MD4C `release-0.5.2` blob | Result |
|---|---|---|---|
| `src/md4c.h` | `8d6be1cb4631528e7c387ca2e49ce42d1ef87477` | `8d6be1cb4631528e7c387ca2e49ce42d1ef87477` | Exact |
| `src/md4c-html.c` | `5229de541389567f97426df5946998140b2f6f9f` | `5229de541389567f97426df5946998140b2f6f9f` | Exact |
| `src/md4c-html.h` | `324211da2ad913d867eb484de86813bd9de99545` | `324211da2ad913d867eb484de86813bd9de99545` | Exact |
| `src/entity.c` | `777706647c3aec70325f7e2ead158d7063bb271f` | `777706647c3aec70325f7e2ead158d7063bb271f` | Exact |
| `src/entity.h` | `b5d3868b4a6d3a5c857aa3b78223183d68ab0c39` | `b5d3868b4a6d3a5c857aa3b78223183d68ab0c39` | Exact |
| `LICENSE.md` | `c80b3a95cedc65986c5afaa6d2b895fcbcc6177a` | `c80b3a95cedc65986c5afaa6d2b895fcbcc6177a` | Exact |

### 2.2 Modified parser implementation

The vendored `src/md4c.c` does not match the upstream `release-0.5.2` blob:

- OrcaSlicer blob: `e3f5cf9d026d481ebb09b41ef39eaad79ae6de9d`
- Upstream 0.5.2 blob: `812bde535850dfff546c357ed0ed3e6b9a177cfb`

The differences are substantive, not just formatting. The reviewed diff includes:

- An output budget for link-reference-definition expansion (`max_ref_def_output`), with a cap and a diagnostic when expansion exceeds the budget. This resembles a defensive bound against pathological reference-link expansion, but the exact originating upstream commit or local rationale has not been established.
- Changes to inline parsing, including whitespace and delimiter handling, strikethrough/equation scanning, wiki-link resolution, and link parsing.
- Changes to hard/soft line-break handling and whitespace recognition.
- Additional initialization and boundary checks.

This comparison does not establish whether the local implementation is a deliberate set of upstream cherry-picks, a vendor fork, or a combination. It also does not establish that the modifications are all present in any single upstream release. The component still labels itself 0.5.2 in CMake, so that version string must not be treated as a complete description of the modified parser source.

### 2.3 CMake integration changes

The top-level vendored CMake file keeps version 0.5.2 but comments out the upstream platform defaults for `BUILD_SHARED_LIBS`, the `md2html` executable option, and the executable subdirectory.

The local `src/CMakeLists.txt` preserves the upstream `md4c` and `md4c-html` target definitions and their dependency relationship, but comments out upstream install/export rules for the libraries, headers, pkg-config metadata, and CMake package export.

These are build and packaging adaptations. They do not change the MIT grant, but they mean the upstream install path cannot be relied on to distribute the license or metadata with OrcaSlicer.

## 3. Active application integration

- `deps_src/CMakeLists.txt` adds the `md4c` subdirectory.
- `src/slic3r/CMakeLists.txt` links `md4c-html` into `libslic3r_gui`.
- `src/slic3r/GUI/ReleaseNote.cpp` includes `md4c-html.h` and calls `md_html()` to render release-note Markdown using GitHub-flavored Markdown flags, strikethrough, and wiki links.

This confirms active build/link integration and application use in the reviewed source revision. It does not prove which exact binary artifacts contain the code on every platform or release configuration.

## 4. Notice and remaining evidence

1. Determine whether the full MIT license and copyright notice are included in the actual Windows, macOS, Linux/AppImage, and source-release notice bundles. The vendored license file is present, but the upstream install rules that might have staged it are disabled.
2. Trace the `md4c.c` local delta to its source commits or intermediate vendor snapshot. Record each cherry-pick/patch and rationale; do not silently attribute all modified code to upstream 0.5.2.
3. Reconcile the 0.5.2 CMake version declaration with the modified parser source and any later upstream fixes incorporated.
4. Validate the configured build and release-note rendering on supported platforms if this component remains in the product.
5. No legal conclusion is made. The source contains an MIT license and required notice; this review does not certify distribution compliance.

## 5. Pinned references

- [OrcaSlicer MD4C import commit](https://github.com/OrcaSlicer/OrcaSlicer/commit/0683013a7e797d8da43f4f84110f3d88cca3aac6)
- [MD4C upstream release tag](https://github.com/mity/md4c/tree/release-0.5.2)
- [MD4C upstream release commit](https://github.com/mity/md4c/commit/729e6b8b320caa96328968ab27d7db2235e4fb47)
- [OrcaSlicer vendored parser source](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/md4c/src/md4c.c)
- [Upstream parser source at 0.5.2](https://github.com/mity/md4c/blob/release-0.5.2/src/md4c.c)

**Scope limitation:** Documentation-only review. No source, build, dependency, or license file was changed; no build, binary/package inspection, SBOM generation, or legal review was performed.
