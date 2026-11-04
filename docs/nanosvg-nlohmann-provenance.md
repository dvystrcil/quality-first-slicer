# NanoSVG and nlohmann/json source provenance review

**Status:** Fixed-revision source and blob-identity review; not a complete license or legal determination  
**Reviewed OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (v2.4.2)

## 1. nlohmann/json 3.10.4

The vendored `deps_src/nlohmann` tree is an exact Git-blob match for the canonical `nlohmann/json` repository at release tag `v3.10.4`.

- The annotated tag object is `c800c002b37744fc1aa39738d1e046d05a955f07`; it resolves to commit `fec56a1a16c6e1c1b1f4e116a20e79398282626c`.
- The release commit is unsigned according to GitHub's tag verification metadata. The tag is a fixed source reference, not independent proof of publisher authenticity.
- Compared the complete vendored component tree against upstream `include/nlohmann/`: all **41 files** match by Git blob SHA, including `json.hpp`, `json_fwd.hpp`, nested `detail/` headers, and Hedley headers. The only additional OrcaSlicer file is its local `CMakeLists.txt` integration file.
- `json.hpp` declares version 3.10.4 and embeds SPDX MIT plus the complete MIT notice.

This establishes exact file identity for the component at the reviewed revisions. It does not prove the authenticity of the upstream tag or settle the license status of other components that may include or bundle related code.

## 2. NanoSVG fork and local modification

OrcaSlicer's archive manifest pins the NanoSVG source to SoftFever repository commit `863f6aa97ef62028126fa2c19bd4350394c2e15e` in `SoftFever/Orca-deps-nanosvg`. The commit is unsigned according to GitHub's verification metadata.

Compared the two vendored headers with that exact upstream commit:

| File | OrcaSlicer Git blob | Upstream Git blob | Result |
|---|---|---|---|
| `nanosvg.h` | `b3aa8b78585c3151a0dc5b95d6316169d5d59926` | `32b6bbbe9a5b12f9ac803e659651f0300361da85` | One functional source change plus indentation difference |
| `nanosvgrast.h` | `a4b866bebaca1b7998d5e0b71b07c224ee546ad9` | `a4b866bebaca1b7998d5e0b71b07c224ee546ad9` | Exact blob match |

The functional change in `nanosvg.h` is in `nsvg__parseTransform()`: OrcaSlicer initializes the local array as `float t[6] = {0.0};`, while the pinned upstream file uses `float t[6];`. This is a local modification and should be preserved as an explicit patch/change record if the component is ever imported.

Both vendored headers retain the NanoSVG copyright, warranty disclaimer, and three-condition permissive license notice. The license requires that:
1. the software's origin not be misrepresented;
2. altered source versions be plainly marked as altered and not misrepresented as original; and
3. the notice not be removed or altered from source distributions.

The vendored `nanosvgrast.h` also preserves its attribution to FLTK for the non-square X/Y scaling modification and its stb_truetype rasterizer basis. The parser header attributes its SVG parser basis to Anti-Grain Geometry 2.4 and its arc calculation to canvg.

**Open notice/provenance work:** The embedded Anti-Grain Geometry and stb_truetype-derived portions need a focused review of the corresponding upstream license/attribution requirements and the exact extent of copied code. The current headers' attribution is evidence of derivation, not a completed license analysis. The local parser modification should be clearly marked in any derivative source distribution to satisfy the NanoSVG altered-source condition.

## 3. Fixed-revision references

- OrcaSlicer v2.4.2 source: [`nanosvg.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/nanosvg/nanosvg.h), [`nanosvgrast.h`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/nanosvg/nanosvgrast.h), [`json.hpp`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/nlohmann/json.hpp).
- NanoSVG upstream: [pinned commit](https://github.com/SoftFever/Orca-deps-nanosvg/commit/863f6aa97ef62028126fa2c19bd4350394c2e15e), [license file](https://github.com/SoftFever/Orca-deps-nanosvg/blob/863f6aa97ef62028126fa2c19bd4350394c2e15e/LICENSE.txt), [parser header](https://github.com/SoftFever/Orca-deps-nanosvg/blob/863f6aa97ef62028126fa2c19bd4350394c2e15e/src/nanosvg.h), [rasterizer header](https://github.com/SoftFever/Orca-deps-nanosvg/blob/863f6aa97ef62028126fa2c19bd4350394c2e15e/src/nanosvgrast.h).
- nlohmann/json upstream: [release tag](https://github.com/nlohmann/json/tree/v3.10.4), [resolved commit](https://github.com/nlohmann/json/commit/fec56a1a16c6e1c1b1f4e116a20e79398282626c).

No source was imported, no local build was run, and no legal review was performed.
