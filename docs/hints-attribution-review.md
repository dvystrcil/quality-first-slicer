# Hints utility attribution and licensing evidence

**Status:** Source lineage and recorded downstream changes documented; original authorship and copyright ownership remain unverified  
**Reviewed OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (v2.4.2)  
**File:** `deps_src/hints/HintsToPot.cpp`

## 1. Findings

`HintsToPot.cpp` is an internal build-time localization utility, not a third-party dependency. It reads hint entries from INI files and appends corresponding gettext entries to the project's POT catalog. The current CMake file builds it as the `hintsToPot` executable.

The file has no individual copyright, author, SPDX, or license header. Git history gives a traceable import and two named downstream code-change authors, but it does **not** establish the original programmer(s), copyright owner, employer ownership, or a complete list of contributors. A commit author is evidence of who made or recorded that commit, not proof that the person owns all copyright in the file.

The initial import commit also contains the repository-level GNU AGPL version 3 license document. That is relevant project-level licensing context, but the history and lack of a file-specific notice do not by themselves establish the precise file-level licensing/copyright statement that should be added. Do not manufacture a copyright line or SPDX tag.

## 2. Traceable history

| Event | Evidence | What it establishes |
|---|---|---|
| Initial source-tree import, 2022-07-15 | [OrcaSlicer commit `1555904beffef41195003f184dec0af46b308eee`](https://github.com/OrcaSlicer/OrcaSlicer/commit/1555904beffef41195003f184dec0af46b308eee), message “Add the full source of BambuStudio using version 1.0.10”; author account `lanewei120` | The file first appears in this reviewed Git path history as part of a bulk BambuStudio source import. The imported file blob is `c93dc274c78007fa3831c4e46403d500bcd71b5d`. This does not identify its original author. |
| Project license present at import | [Root LICENSE at the import commit](https://github.com/OrcaSlicer/OrcaSlicer/blob/1555904beffef41195003f184dec0af46b308eee/LICENSE), blob `dba13ed2ddf783ee8118c6a581dbf75305f816a3` | The repository snapshot includes the GNU AGPL version 3 license text. This is not an independently evidenced file-level copyright attribution. |
| Boost.Nowide stream change, 2022 | [Commit `ab03a10621562b85ea2bc66e514b66a2c3ccf423`](https://github.com/OrcaSlicer/OrcaSlicer/commit/ab03a10621562b85ea2bc66e514b66a2c3ccf423), message “Use fstream from boost::nowide”; author account `zhaofengli`, committer account `SoftFever` | A recorded downstream contributor changed the output stream implementation for Boost compatibility. |
| MSVC compilation fix, 2022 | [Commit `5e5dea82b64c0be384dbdee2f00cd4dba4257dbf`](https://github.com/OrcaSlicer/OrcaSlicer/commit/5e5dea82b64c0be384dbdee2f00cd4dba4257dbf), message “HintsToPot: Fix compilation on MSVC”; author account `zhaofengli`, committer account `SoftFever` | A second recorded change is attributed in Git history to the same account. |
| Directory relocation, 2025-08-22 | [Commit `883607e1d4a0b2bb719f2f4bcd9fd72f8c2174fa`](https://github.com/OrcaSlicer/OrcaSlicer/commit/883607e1d4a0b2bb719f2f4bcd9fd72f8c2174fa) | The file moved from `src/hints/` to `deps_src/hints/` as part of a source-tree reorganization. This is a path move, not evidence of new authorship or third-party origin. |

## 3. Source comparison

At the initial import commit, the file is `src/hints/HintsToPot.cpp` with blob SHA:

`c93dc274c78007fa3831c4e46403d500bcd71b5d`

At the reviewed OrcaSlicer v2.4.2 revision, the relocated file has blob SHA:

`a2ff5ddfa49b994dac6c36f0a1c79b8ac52bb2d9`

The inspected source differences include:

- the output stream now uses `boost::nowide::ofstream` with `path.string()` rather than `boost::filesystem::ofstream` with a moved path;
- the output catalog name changes from `BambuStudio.pot` to `OrcaSlicer.pot`.

The source file at the later BambuStudio snapshot `355d71eee5a9ebc794693fe57e63674806019770` has blob SHA `0d17e5fdc3b9a4274bef820b6de89cc543e7c3cd`; it has further functional changes (additional INI input, improved file-open error handling, and parameterized catalog references). This later snapshot confirms the utility continued to evolve in BambuStudio, but it is not byte-identical to the reviewed OrcaSlicer file and does not identify the original author or owner.

Pinned source references:

- [Initial OrcaSlicer import version](https://github.com/OrcaSlicer/OrcaSlicer/blob/1555904beffef41195003f184dec0af46b308eee/src/hints/HintsToPot.cpp)
- [Reviewed OrcaSlicer v2.4.2 version](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hints/HintsToPot.cpp)
- [Later BambuStudio version](https://github.com/bambulab/BambuStudio/blob/355d71eee5a9ebc794693fe57e63674806019770/src/hints/HintsToPot.cpp)
- [Reviewed OrcaSlicer hints CMake](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hints/CMakeLists.txt)

## 4. Attribution disposition

The evidence supports the following record:

- **Component classification:** internal project build utility.
- **Initial recorded source-tree import:** BambuStudio 1.0.10 bulk import, commit authored by account `lanewei120`.
- **Recorded downstream modifications:** two commits authored by account `zhaofengli` and committed by `SoftFever`.
- **Original source author(s):** unknown from the inspected public history.
- **Copyright holder / employer rights:** not established.
- **License context:** repository root contained the GNU AGPLv3 license at the initial import; exact file-level attribution and licensing treatment should be confirmed rather than inferred from the bulk-import commit alone.
- **SPDX / copyright header:** do not add until the responsible project/rights holder confirms the intended attribution and license statement.

The next useful evidence would be an upstream BambuStudio/PrusaSlicer file-history record that predates the bulk import, or written confirmation from the relevant maintainers identifying the original authorship, rights holder, and intended license. The inspected public snapshots do not settle those points.

## 5. Scope and limitations

This is a documentation-only provenance review. It does not add or alter a source header, make a copyright ownership finding, make a legal determination, or claim that the two recorded downstream commit authors are the only contributors. No local build was run.
