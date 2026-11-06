# NanoSVG embedded-code attribution and notice review

**Status:** Targeted attribution/license-scope review; not a legal determination  
**Reviewed OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (v2.4.2)  
**NanoSVG upstream revision:** SoftFever `Orca-deps-nanosvg` commit `863f6aa97ef62028126fa2c19bd4350394c2e15e`

## 1. Findings

The pinned NanoSVG fork carries its own three-condition permissive license, but its headers explicitly identify code or modifications derived from other projects. Those attributions must be treated as separate provenance leads; the NanoSVG license alone does not establish the license status of any copied third-party portions.

- `nanosvg.h` says the SVG parser is based on the Anti-Grain Geometry (AGG) 2.4 SVG example and attributes Maxim Shemanarev (2002–2004).
- `nanosvgrast.h` says its polygon rasterization is heavily based on Sean Barrett's `stb_truetype` rasterizer. It also records that FLTK modified the file to support non-square X/Y scaling.
- `nanosvg.h` additionally attributes arc calculation code to canvg and a bounding-box calculation to a 2009 blog post. These attributions were not independently traced in this pass.

The headers preserve these attribution statements. This review does **not** establish the exact extent of source-code copying versus algorithmic influence, so it does not assign separate SPDX identifiers or conclude that a particular third-party license notice is legally required or missing.

## 2. AGG 2.4 attribution

NanoSVG's parser header explicitly identifies the AGG 2.4 SVG example as its basis. AGG 2.4 published two license alternatives:

- the Anti-Grain Geometry Public License, with a 2002–2004 copyright notice; and
- the Modified BSD license, with a 2002–2005 copyright notice and source/binary notice conditions.

The historical AGG license page documents both alternatives: [AGG 2.4 licenses](https://franko.github.io/antigrain/license/index.html). The current NanoSVG headers do not state which AGG alternative, if either, was selected for the material described as based on the AGG example. The attribution is clear; the copied-code boundary and license election are not.

**Follow-up:** Compare the relevant parser routines against the AGG 2.4 SVG example and establish whether protectable source expression was carried over. If so, identify the applicable AGG license election and preserve its required notices in source and binary distributions. Do not infer that NanoSVG's own grant supersedes an upstream license.

## 3. stb_truetype attribution

The rasterizer header states: “The polygon rasterization is heavily based on stb_truetype rasterizer by Sean Barrett.” The upstream stb project describes its libraries as public-domain or MIT-licensed and says each source file contains an explicit dual-license choice. The upstream `stb_truetype.h` includes the MIT alternative and the Unlicense/public-domain dedication:

- [Upstream stb_truetype.h](https://github.com/nothings/stb/blob/master/stb_truetype.h)
- [stb project licensing FAQ](https://github.com/nothings/stb#whats-the-license)

NanoSVG's rasterizer header retains Sean Barrett's attribution, but it does not reproduce the stb_truetype dual-license text or record which alternative was selected for any derived code. Because “heavily based” does not by itself identify the exact copied portions or prove a particular license election, this is an unresolved scope question rather than a concluded license violation.

**Follow-up:** Compare the NanoSVG rasterizer implementation with relevant historical stb_truetype revisions, identify copied/adapted routines, and determine whether the public-domain dedication or MIT alternative was relied upon. Preserve the corresponding attribution and notices where required.

## 4. FLTK modification attribution

The rasterizer header separately states that FLTK modified NanoSVG to support non-square X/Y scaling and added `nsvgRasterizeXY()`. This is distinct from the stb_truetype derivation. The FLTK change history and the license/notice basis for those modifications have not been established here.

**Follow-up:** Trace the FLTK-origin change to a fixed FLTK revision and determine whether the modified code was contributed under NanoSVG's terms or is covered by FLTK's project licensing. Retain the existing FLTK attribution unless stronger source history justifies a more precise statement.

## 5. NanoSVG's own altered-source condition

The NanoSVG license requires altered source versions to be plainly marked as altered and not misrepresented as original. The reviewed OrcaSlicer parser contains a functional local change in `nsvg__parseTransform()`:

- pinned upstream: `float t[6];`
- OrcaSlicer v2.4.2: `float t[6] = {0.0};`

At the reviewed source revision, the changed declaration has no adjacent comment identifying it as an OrcaSlicer modification. The provenance document records the difference, but no source-level alteration marker was found at the change site in the reviewed header. This is a concrete compliance question under NanoSVG condition 2; the appropriate source-distribution marking should be reviewed and, if needed, added by the source maintainer. No source change is made by this audit PR.

## 6. Fixed-revision references

All OrcaSlicer links below are pinned to `8500fcdccaa10b5099ac20d252af3a7c560046f1`.

- [Vendored NanoSVG parser header](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/nanosvg/nanosvg.h)
- [Vendored NanoSVG rasterizer header](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/nanosvg/nanosvgrast.h)
- [Pinned SoftFever NanoSVG commit](https://github.com/SoftFever/Orca-deps-nanosvg/commit/863f6aa97ef62028126fa2c19bd4350394c2e15e)
- [NanoSVG fork license](https://github.com/SoftFever/Orca-deps-nanosvg/blob/863f6aa97ef62028126fa2c19bd4350394c2e15e/LICENSE.txt)
- [AGG 2.4 license alternatives](https://franko.github.io/antigrain/license/index.html)
- [stb_truetype upstream license and attribution](https://github.com/nothings/stb/blob/master/stb_truetype.h)

## 7. Limitations and conclusion

This review records the upstream attributions and the relevant license alternatives, but does not settle whether the NanoSVG parser/rasterizer contains copied code from AGG or stb_truetype, which license alternatives were selected, the FLTK modification's precise source history, or the canvg/bounding-box attributions. Those require source-to-source comparison and, where necessary, upstream clarification or legal review.

The NanoSVG parser's local zero-initialization change is real and is not visibly marked at its source location in the reviewed revision. That should remain an explicit open item. No source was imported, no source was modified, no build was run, and no legal conclusion is made.
