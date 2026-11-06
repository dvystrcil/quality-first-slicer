# Legacy Clipper 6.x license and active-use review

**Status:** Targeted source/build-path review; exact upstream revision and complete source delta remain unresolved  
**OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (`v2.4.2`)  
**Initial source-history reference:** OrcaSlicer/BambuStudio bulk source import `1555904beffef41195003f184dec0af46b308eee` (BambuStudio 1.0.10)  
**Method:** Remote inspection of the pinned source tree, component CMake, application CMake, wrapper translation units, and Git blob identities. No local build, complete upstream comparison, or binary inspection.

## 1. License evidence

The legacy Clipper source declares the Boost Software License 1.0 in the file headers:

- `deps_src/clipper/clipper.hpp` identifies Angus Johnson, copyright 2010–2017, and states that use, modification, and distribution are subject to Boost Software License 1.0.
- `deps_src/clipper/clipper.cpp` carries the same author, copyright, version/date, license, and algorithm attribution block.
- The inspected `deps_src/clipper` tree has no separate top-level license file; the license grant and copyright/attribution statements are embedded in the source files.

This is evidence for the legacy Clipper files inspected here. It should not be generalized to Clipper2 or other geometry code.

## 2. Both legacy variants are actively compiled

The v2.4.2 CMake and wrapper files show two compilation paths:

### 2.1 2D variant using `Slic3r::Point`

- `src/libslic3r/CMakeLists.txt` lists `clipper.cpp` and `clipper.hpp` in the `libslic3r` source set.
- `src/libslic3r/clipper.cpp` is a wrapper that includes the libslic3r header, defines the `Slic3r` namespace prefix and `Slic3r::Point` as Clipper's point type, then includes `<clipper/clipper.cpp>`.
- `src/libslic3r/clipper.hpp` performs the corresponding namespace/type configuration and includes `<clipper/clipper.hpp>`.
- `ClipperUtils.cpp` includes the libslic3r Clipper wrapper and contains active polygon clipping/offsetting implementation code.

### 2.2 3D/Z variant

- `deps_src/clipper/CMakeLists.txt` creates the static `clipper` target from `clipper_z.cpp` and `clipper_z.hpp`; it comments out direct compilation of `clipper.cpp` and `clipper.hpp` because the 2D variant is compiled as part of `libslic3r`.
- `clipper_z.cpp` defines `CLIPPERLIB_USE_XYZ` and includes `clipper.cpp`, compiling the separate Z-coordinate implementation.
- `src/libslic3r/CMakeLists.txt` links the `clipper` target privately into `libslic3r`.
- `ClipperZUtils.hpp` includes `<clipper/clipper_z.hpp>` and uses its Z-coordinate path types and callback API.

Therefore the legacy Clipper dependency is not merely an unused vendored directory: the reviewed build compiles both the customized 2D variant and the Z-enabled variant.

## 3. Version and provenance cautions

The checked-in `clipper.hpp` contains two inconsistent version indicators:

- The file banner says `Version: 6.4.2`.
- The preprocessor macro says `CLIPPER_VERSION "6.2.6"`.

The macro is not a reliable version indicator in this snapshot: the initial BambuStudio import already had `CLIPPER_VERSION "6.2.6"` while its banner said 6.2.9. The later documented 6.4.2 update changed the banner/date/copyright but left that macro unchanged. The 6.4.2 banner is supported by the recorded upgrade history below; the macro is stale metadata, not evidence that the implementation is Clipper 6.2.6.

The source files existed in the initial BambuStudio 1.0.10 bulk import commit listed above. Comparing Git blob IDs at that import commit with the v2.4.2 vendored files shows that `clipper.cpp` and `clipper.hpp` are not byte-identical. By contrast, `clipper_z.cpp`, `clipper_z.hpp`, and the two `src/libslic3r` wrapper files have identical blob IDs between the import snapshot and v2.4.2. The observed identities are:

| File | Initial import blob | v2.4.2 blob | Exact match |
|---|---|---|---|
| `src/clipper/clipper.cpp` → `deps_src/clipper/clipper.cpp` | `84d68b1e66f3ee625f956e2539a62b823f6e761f` | `1f16446ac8da1f0b9c802d8a9dee33f766919f6b` | No |
| `src/clipper/clipper.hpp` → `deps_src/clipper/clipper.hpp` | `b1dae3c2480e2c4609a219119b560e845da614dd` | `06637effce040fa7d87c368437cb32398f19ee92` | No |
| `src/clipper/clipper_z.cpp` → `deps_src/clipper/clipper_z.cpp` | `f26be7089ad1984e655896918b985663be6366c2` | `f26be7089ad1984e655896918b985663be6366c2` | Yes |
| `src/clipper/clipper_z.hpp` → `deps_src/clipper/clipper_z.hpp` | `20596d8e196d46606fd1211d401d92c2220915d3` | `20596d8e196d46606fd1211d401d92c2220915d3` | Yes |
| `src/libslic3r/clipper.cpp` | `8f38ba6215e270ab83a4b9805b45b90777234917` | `8f38ba6215e270ab83a4b9805b45b90777234917` | Yes |
| `src/libslic3r/clipper.hpp` | `b0dd51a4f7f5db546b50bc572a27675a6cb99866` | `b0dd51a4f7f5db546b50bc572a27675a6cb99866` | Yes |

A non-matching blob establishes that the file changed; it does not identify the change, its author, or its license significance. The folder-move commit `883607e1d4a0b2bb719f2f4bcd9fd72f8c2174fa` explains the later move into `deps_src`, but is not itself a complete source-provenance comparison.

## 4. Source lineage and downstream patch chain

The OrcaSlicer history resolves much of the earlier uncertainty. The file was initially imported with BambuStudio 1.0.10 in 2022, then upgraded and substantially adapted in a documented 2025 commit.

### 4.1 Initial imported version

At the initial import commit `1555904beffef41195003f184dec0af46b308eee`, `src/clipper/clipper.hpp` had:

- Banner version `6.2.9`, date 16 February 2015, copyright through 2015.
- Macro `CLIPPER_VERSION "6.2.6"`.

This establishes that the macro/banner disagreement predates the later 6.4.2 update. The macro was already stale or inconsistent in the initial imported source; it should not be used alone to infer the release.

### 4.2 Documented 6.4.2 upgrade and PrusaSlicer-derived adaptations

OrcaSlicer commit [`fe4a72ec94d1675949e55ee334a7aa373dc5cce4`](https://github.com/OrcaSlicer/OrcaSlicer/commit/fe4a72ec94d1675949e55ee334a7aa373dc5cce4), titled **“Upgrade clipper & improve multi-thread performance”**, records the source lineage in its commit message and patch.

It explicitly records these cherry-picks from `prusa3d/PrusaSlicer`:

| PrusaSlicer commit | Recorded change |
|---|---|
| `fa7debf49d0f8f850a64fb2a5a4cf71810612a3c` | Validate int32 coordinate range on input |
| `9dca8403fe1ca4bd4aac67adaad5d1ef0fedd4a1` | Use integer cross products in `PointInPolygon()` |
| `9cde96993e9f996b44f417570ba05455472efa08` | Rework ClipperLib/Polygon allocation around TBB scalable allocators |
| `b67ad6434d1e5b1b54a13e83ceaef4141f9ad35` | Follow-up scalable allocator changes |
| `b3b44681a9461550ee148206f329d55c0c9459eb` | Compiler compatibility follow-up |
| `7e77048593dfa7f31c2bac00d8dd2f7cb8628cb7` | Remove Shiny profiler integration |
| `a7e17df25f66d3fb4fce213574ba25ebea1d238d` | Further allocator optimization and simplify-polygon behavior changes |
| `2e150795b17be285b934c83b6a9157ec07b5ccdd` | Use `emplace_back()` |
| `b39c33414f377a20d60e9430043a3eb603e0b9c8` | Correct 32-bit intersection-point range checking |
| `0a202dcff3b90429021ee7b7376df5d11865aa41` | Fix an out-of-bound assertion |
| `b8b3cccb40f14f582e2e1272543de080543bfd3c` | Update upstream Clipper to 6.4.2 |

The OrcaSlicer upgrade patch changes the header banner from 6.2.9 (2015) to 6.4.2 (27 February 2017) and updates the copyright year range to 2010–2017. It does not update the pre-existing `CLIPPER_VERSION "6.2.6"` macro. The same commit includes substantive downstream changes beyond the version-banner update, including allocator substitutions, integer-range handling, geometry/intersection changes, and simplification behavior.

### 4.3 Cross-check against the PrusaSlicer source snapshot

At PrusaSlicer commit `b8b3cccb40f14f582e2e1272543de080543bfd3c`:

- OrcaSlicer v2.4.2 `clipper.cpp` is byte-identical to PrusaSlicer's `src/clipper/clipper.cpp` (Git blob `1f16446ac8da1f0b9c802d8a9dee33f766919f6b`).
- The headers are not byte-identical. The reviewed Orca header differs from that PrusaSlicer header in two observed places: Orca comments out `CLIPPERLIB_INT32`, and it has the additional `!pg.empty()` guard in the path-processing loop (the latter is also recorded in OrcaSlicer commit `107cd3edb05ef7327d6925aa352082f1168473e0`, “fix a crash bug when generating support”).
- The macro remains `6.2.6` in both the Orca and PrusaSlicer 6.4.2 headers. This confirms that the stale macro was carried through the upgrade lineage rather than synchronized to the banner.

The public `skyrpex/clipper` mirror contains a 6.4.2 header dated 27 February 2017 and a separate `License.txt` with the Boost Software License 1.0 text. It is a useful corroborating copy, not proof that it is the exact archive used by PrusaSlicer or OrcaSlicer. Its header is not byte-identical to the Orca version.

### 4.4 What is now established—and what is not

The defensible lineage is: Angus Johnson Clipper 6.2.9-era source in the BambuStudio 1.0.10 import; a documented OrcaSlicer/PrusaSlicer-derived upgrade to Clipper 6.4.2; then a series of recorded performance, allocator, geometry, and integration adaptations. The 6.4.2 banner is supported by that history, while the 6.2.6 macro is stale.

The exact original upstream archive hash and a complete attribution of every line-level change are not established by this review. The Boost license notice remains embedded in the source headers, but the standalone full-text `License.txt` present in the public mirror was not found in the inspected OrcaSlicer `deps_src/clipper` subtree or the corresponding PrusaSlicer `src/clipper` subtree. Whether the distribution's other notice locations satisfy the applicable requirements remains a separate notice-packaging question.

Pinned lineage evidence:

- [OrcaSlicer upgrade commit and full patch](https://github.com/OrcaSlicer/OrcaSlicer/commit/fe4a72ec94d1675949e55ee334a7aa373dc5cce4)
- [PrusaSlicer 6.4.2 update commit](https://github.com/prusa3d/PrusaSlicer/commit/b8b3cccb40f14f582e2e1272543de080543bfd3c)
- [OrcaSlicer follow-up empty-path guard](https://github.com/OrcaSlicer/OrcaSlicer/commit/107cd3edb05ef7327d6925aa352082f1168473e0)
- [Clipper mirror 6.4.2 header](https://github.com/skyrpex/clipper/blob/master/cpp/clipper.hpp)
- [Clipper mirror Boost license text](https://github.com/skyrpex/clipper/blob/master/License.txt)

## 5. Pinned evidence

OrcaSlicer v2.4.2:

- [Legacy Clipper component CMake](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/clipper/CMakeLists.txt)
- [Clipper header and embedded license/version declarations](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/clipper/clipper.hpp)
- [Clipper implementation and embedded notice](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/clipper/clipper.cpp)
- [Z-enabled wrapper](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/clipper/clipper_z.cpp)
- [2D wrapper translation unit](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/clipper.cpp)
- [Z API integration](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/ClipperZUtils.hpp)
- [Application source and link declarations](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/libslic3r/CMakeLists.txt)

History:

- [Initial BambuStudio 1.0.10 source import](https://github.com/OrcaSlicer/OrcaSlicer/commit/1555904beffef41195003f184dec0af46b308eee)
- [Move third-party source into deps_src](https://github.com/OrcaSlicer/OrcaSlicer/commit/883607e1d4a0b2bb719f2f4bcd9fd72f8c2174fa)

## 6. Remaining work

1. Resolve the exact upstream Clipper source release/commit that corresponds to the imported files.
2. Diff the two non-identical files against that exact upstream source and attribute each downstream change.
3. Reconcile the 6.4.2 banner with the 6.2.6 macro and establish which version metadata is reliable.
4. Confirm the Boost Software License 1.0 text and required copyright/attribution notices are included in the project's source and binary notice distribution.
5. Preserve the distinction between the legacy Clipper 6.x code and the separately reviewed Clipper2 1.5.2 component.

## 7. Limitations

This is a targeted build-path and source-header review. It confirms active use of both legacy variants and embedded Boost Software License 1.0 declarations in the inspected source files. It does not establish the exact original upstream archive checksum, a complete line-by-line source closure, release-package notice contents, or a legal determination. No source code or dependency configuration was changed.
