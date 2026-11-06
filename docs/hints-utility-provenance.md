# Hints utility provenance review

**Status:** Source lineage and recorded downstream changes documented; original authorship and copyright ownership remain unverified  
**Reviewed OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (v2.4.2)

## Finding

The `hints` directory is not an independently sourced third-party library. It is an internal build utility that generates gettext `.pot` entries from `resources/data/hints.ini`. Its CMake file creates the `hintsToPot` executable and an interface target; the executable uses Boost APIs.

The directory was moved under `deps_src/` during a 2025 source-tree reorganization, but its history predates that move and places it in the original BambuStudio application source tree.

## History evidence

1. The file first appears in the reviewed Git path history in commit [`1555904beffef41195003f184dec0af46b308eee`](https://github.com/OrcaSlicer/OrcaSlicer/commit/1555904beffef41195003f184dec0af46b308eee), dated 2022-07-15. The commit message is **“Add the full source of BambuStudio using version 1.0.10”** and its author is recorded as `lane.wei@bambulab.com`.
2. The initial file blob in that commit is `c93dc274c78007fa3831c4e46403d500bcd71b5d`. The same blob is present at the same commit in the BambuStudio repository, confirming the initial source snapshot identity.
3. Later changes in December 2022 are attributed in Git history to Zhaofeng Li and include the Boost.Nowide stream change and an MSVC compilation fix. The current file is therefore not byte-identical to the initial imported file.
4. Commit [`883607e1d4a0b2bb719f2f4bcd9fd72f8c2174fa`](https://github.com/OrcaSlicer/OrcaSlicer/commit/883607e1d4a0b2bb719f2f4bcd9fd72f8c2174fa), dated 2025-08-22, moved the file from `src/hints/` to `deps_src/hints/` as part of a broad source-tree reorganization. The commit is verified as signed by GitHub.
5. The repository's root `LICENSE` at the initial source-import commit contains the GNU Affero General Public License version 3 text. This is project-level licensing context; it is not a substitute for confirming file-level copyright attribution or reviewing the full source history.

## Classification and remaining work

- Classify `hints` as an **internal project utility**, not a third-party dependency, in the dependency inventory.
- Do not count it as one of the third-party libraries merely because it is listed under `deps_src/CMakeLists.txt`.
- The file has no individual copyright, author, SPDX, or license header in the reviewed revision.
- The initial import commit is authored by account `lanewei120`; two later changes are authored by `zhaofengli` and committed by `SoftFever`. These are commit-history attributions, not proof of original authorship or copyright ownership.
- The repository root contains the GNU AGPLv3 text at the initial import commit, but the precise file-level attribution/licensing statement still requires confirmation. Do not invent an SPDX identifier or copyright holder.
- The initial, reviewed, and later BambuStudio file blob IDs and the observed source changes are recorded in [hints attribution review](hints-attribution-review.md).

## Fixed-revision references

- [Current `HintsToPot.cpp`](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hints/HintsToPot.cpp)
- [Current hints CMake file](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hints/CMakeLists.txt)
- [Initial BambuStudio source import](https://github.com/OrcaSlicer/OrcaSlicer/commit/1555904beffef41195003f184dec0af46b308eee)
- [December 2022 Boost.Nowide change](https://github.com/OrcaSlicer/OrcaSlicer/commit/ab03a10621562b85ea2bc66e514b66a2c3ccf423)
- [December 2022 MSVC fix](https://github.com/OrcaSlicer/OrcaSlicer/commit/5e5dea82b64c0be384dbdee2f00cd4dba4257dbf)
- [2025 directory reorganization](https://github.com/OrcaSlicer/OrcaSlicer/commit/883607e1d4a0b2bb719f2f4bcd9fd72f8c2174fa)

No local build or legal review was performed.
