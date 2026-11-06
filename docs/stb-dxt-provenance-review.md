# stb_dxt provenance and license review

**Status:** Targeted source-provenance review; copyright-holder attribution and distribution-notice completeness remain open  
**Reviewed OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (v2.4.2)  
**Canonical source repository:** [Cyan4973/RygsDXTc](https://github.com/Cyan4973/RygsDXTc)  
**Pinned upstream snapshot:** commit `8b983d43c85f84c1c16665c1661b16acd1f6f429` (message: `Mirror from SVN`)

## 1. Executive findings

The exact origin of the custom compressor is now substantially narrowed and its source snapshot is pinned.

- The vendored OrcaSlicer header identifies itself as based on Fabian "ryg" Giesen's v1.04 implementation and as a custom version modified by Yann Collet.
- The canonical repository named in that header is `Cyan4973/RygsDXTc`. Its pinned commit `8b983d43c85f84c1c16665c1661b16acd1f6f429` contains the corresponding `stb_dxt.h` (Git blob `318e306e3c9fcdd326a3d1b930242ea0902201f5`).
- OrcaSlicer's vendored header has Git blob `db19110f433670550bdad147191e1be4777a8db8`. That exact blob is also present at `bambulab/BambuStudio/src/stb_dxt/stb_dxt.h` in the inspected BambuStudio snapshot (commit `355d71eee5a9ebc794693fe57e63674806019770`). This establishes byte-identical content at those two snapshots, but not by itself the historical commit that introduced the file into either project.
- A line-based comparison of the OrcaSlicer header with the pinned RygsDXTc header found 1,040 identical lines out of 1,050 local and 1,044 upstream lines, with five small difference hunks. The functional differences are limited to the `rygCompress()` wrapper: adding an output parameter for compressed byte count, tracking the destination pointer delta, and passing `STB_DXT_NORMAL` rather than the upstream literal `10`. The remaining differences are the corresponding signature/formatting changes.
- The header contains the full BSD 2-Clause license text. No separate license file was present at the pinned RygsDXTc snapshot. The embedded license text has no explicit copyright-year/holder line, despite requiring preservation of the copyright notice. The source identifies Yann Collet as modifier and Fabian Giesen as the basis author, but it does not itself resolve the copyright-holder notice required for redistribution.

This is a provenance finding, not a legal determination. The BSD-2-Clause label is supported by the embedded license text; the missing explicit copyright attribution and exact historical rights-holder remain open.

## 2. Source lineage

### 2.1 RygsDXTc source

The vendored header explicitly states:

- Based on the original by Fabian "ryg" Giesen, version 1.04.
- Custom version modified by Yann Collet.
- Version history includes v1.05 speed optimizations and v1.06 implementation of Fabian Giesen's comments.

The repository's pinned commit is a GitHub mirror commit titled `Mirror from SVN`. The file is therefore pinned to a reproducible source snapshot, but the mirror commit is not a tagged upstream release and does not identify a semantic version for the custom fork.

- [Pinned RygsDXTc header](https://github.com/Cyan4973/RygsDXTc/blob/8b983d43c85f84c1c16665c1661b16acd1f6f429/stb_dxt.h)
- [Pinned RygsDXTc implementation wrapper](https://github.com/Cyan4973/RygsDXTc/blob/8b983d43c85f84c1c16665c1661b16acd1f6f429/stb_dxt.cpp)
- [Pinned mirror commit](https://github.com/Cyan4973/RygsDXTc/commit/8b983d43c85f84c1c16665c1661b16acd1f6f429)

### 2.2 BambuStudio snapshot relationship

The OrcaSlicer header blob SHA is exactly the same as the BambuStudio `src/stb_dxt/stb_dxt.h` blob at commit `355d71eee5a9ebc794693fe57e63674806019770`:

`db19110f433670550bdad147191e1be4777a8db8`

This is strong evidence that the two inspected snapshots contain byte-identical copies. It is not evidence that the referenced BambuStudio commit introduced or originally imported the file; that commit changes an unrelated source file. A complete historical import path still requires path-specific history.

- [BambuStudio header at inspected snapshot](https://github.com/bambulab/BambuStudio/blob/355d71eee5a9ebc794693fe57e63674806019770/src/stb_dxt/stb_dxt.h)
- [OrcaSlicer header at reviewed revision](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/stb_dxt/stb_dxt.h)

## 3. Source comparison

The comparison was performed line-by-line between the OrcaSlicer header at the fixed v2.4.2 revision and the RygsDXTc header at the pinned mirror commit.

| Measurement | OrcaSlicer | RygsDXTc |
|---|---:|---:|
| Lines | 1,050 | 1,044 |
| Git blob SHA | `db19110f433670550bdad147191e1be4777a8db8` | `318e306e3c9fcdd326a3d1b930242ea0902201f5` |
| Common identical lines (LCS) | 1,040 | 1,040 |

Five difference hunks were found:

1. The declaration of `rygCompress()` adds an `int& compressed_size` output parameter and a comment describing it.
2. The implementation signature adds the same output parameter.
3. OrcaSlicer saves the initial destination pointer before compression.
4. The block compressor call uses `STB_DXT_NORMAL` instead of literal `10`.
5. OrcaSlicer computes `compressed_size = dst - initial_dst` after writing the compressed blocks.

These are consistent with the call site in OrcaSlicer `GLTexture.cpp`, which allocates a destination buffer, invokes `rygCompress(..., compressed_size)`, and resizes the vector to the returned byte count. The implementation is active, not merely a vendored unused directory:

- `deps_src/CMakeLists.txt` adds the `stb_dxt` interface target.
- `GLTexture.cpp` defines `STB_DXT_IMPLEMENTATION`, includes the vendored header, and calls `rygCompress()` in the texture compression path.

[Fixed-revision GLTexture.cpp](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/slic3r/GUI/GLTexture.cpp)

## 4. License and attribution findings

The RygsDXTc header includes the full operative BSD 2-Clause grant and disclaimer, including source and binary redistribution conditions. This supports classifying the inspected source under BSD-2-Clause for inventory purposes.

However:

- The embedded license block contains no explicit `Copyright (c) <year> <holder>` line or other concrete copyright notice.
- The pinned repository snapshot did not contain a separate `LICENSE.txt` at its root.
- The file credits Fabian Giesen as the basis author and Yann Collet as the custom modifier, but those role descriptions do not establish the complete copyright-holder list or years.
- The upstream license text's source and binary conditions require retaining/reproducing the copyright notice. The absence of a concrete notice in the inspected source is therefore a redistribution-notice gap to resolve, not something this audit should fill by guessing.
- The BambuStudio/OrcaSlicer wrapper modifications do not remove or replace the embedded BSD license text.

**Required follow-up:** Determine the appropriate copyright notice and holder/year attribution from the upstream author or reliable historical source records. Preserve the complete BSD-2-Clause text and the confirmed attribution in source distributions and binary third-party notices. Do not invent a copyright line or assume that a generic BSD template itself identifies the rights holders.

## 5. Conclusion and remaining status

The exact custom upstream repository and a fixed source snapshot are now identified. The OrcaSlicer file is a close derivative of that snapshot, with a small, explainable wrapper delta, and the inspected OrcaSlicer/BambuStudio files are byte-identical.

The license family is supported by the embedded BSD 2-Clause text. The outstanding issue is the concrete copyright notice/rights-holder attribution required to preserve that license correctly in distributions. The original Fabian Giesen v1.04 base lineage is explicitly credited in the source, but this review does not independently compare against the original v1.04 source or determine every historical contribution.

No source was imported or modified. No build was run. No binary package or third-party notice bundle was inspected. No legal conclusion is made.
