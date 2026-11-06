# HIDAPI provenance and license-election review

**Status:** Source origin and build integration verified; selected license and notice preservation remain unresolved  
**Reviewed OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (v2.4.2)  
**Vendored release identified by its README:** hidapi 0.9.0, upstream commit `7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f`  
**Canonical upstream:** [libusb/hidapi](https://github.com/libusb/hidapi)

## 1. Executive findings

The vendored component is a reproducible copy of the HIDAPI 0.9.0 source distribution identified by its own README. The vendored `include/hidapi.h` has the same Git blob SHA as the header at the pinned upstream commit:

`1819f8de0912f225373f0390dbe582434d9c9dac`

The source headers explicitly preserve an unusual licensing choice: HIDAPI may be used under **one of three alternatives**, at the user's discretion:

1. GNU General Public License version 3 (the upstream `LICENSE-gpl3.txt`);
2. a BSD-style license (the upstream `LICENSE-bsd.txt`); or
3. the original HIDAPI license (the upstream `LICENSE-orig.txt`).

The upstream `LICENSE.txt` is a selection guide, not itself the selected license. It expressly says the choice is at the user's discretion and gives examples of likely choices for GPL and commercial closed-source projects.

All four referenced license documents are absent from OrcaSlicer's vendored `deps_src/hidapi` subset. The source header's menu of alternatives does not identify which alternative the OrcaSlicer maintainers selected. The CMake target, project-level license, or presence of a static library does not independently prove that selection.

**Conclusion:** Do not classify this vendored copy as BSD, GPLv3, or the original HIDAPI license yet. Record the license election as unknown and restore the selected license document and required notices only after the election is supported by reliable evidence or an explicit rights-holder/maintainer confirmation.

## 2. Fixed source identity and file evidence

The vendored README states:

- source distribution: `hidapi-0.9.0`;
- abbreviated upstream commit: `7da5cc9`.

The exact upstream commit matching that abbreviation is:

`7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f`

At that commit, the upstream repository contains all four files named by the source headers:

| Upstream file | Git blob SHA | Purpose |
|---|---|---|
| `LICENSE.txt` | `e1676d4c42d6d58af863c64fbe02e88186f6cae3` | Explains the three alternatives and says the choice is at the user's discretion |
| `LICENSE-bsd.txt` | `538cdf95cf63e6f8fab8e9c4c7222a35357b4ce1` | BSD-style terms; copyright line names Alan Ott / Signal 11 Software (2010) |
| `LICENSE-gpl3.txt` | `94a9ed024d3859793618152ea559a168bbcbb5e2` | GNU GPL version 3 text |
| `LICENSE-orig.txt` | `e3f33808299600e580b63aee36a0eb18daaae916` | Original HIDAPI terms; requires the source-file copyright notice to remain intact |

The upstream `Makefile.am` includes all four documents in `dist_doc_DATA`. This establishes that the original source distribution ships the selection guide and each alternative license text. It does not show which one was selected by the downstream OrcaSlicer project.

The OrcaSlicer vendored `include/hidapi.h` blob SHA is `1819f8de0912f225373f0390dbe582434d9c9dac`, matching the file at the pinned upstream commit. Its header and the platform implementation headers refer to the three alternatives and the four root-level license documents. The vendored subset omits those four documents.

Evidence links, all pinned:

- [Vendored README](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hidapi/README.md)
- [Vendored public header](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hidapi/include/hidapi.h)
- [Vendored Linux implementation](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hidapi/linux/hid.c)
- [Vendored macOS implementation](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hidapi/mac/hid.c)
- [Vendored Windows implementation](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hidapi/win/hid.c)
- [Upstream selection guide](https://github.com/libusb/hidapi/blob/7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f/LICENSE.txt)
- [Upstream BSD-style license](https://github.com/libusb/hidapi/blob/7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f/LICENSE-bsd.txt)
- [Upstream GPLv3 license](https://github.com/libusb/hidapi/blob/7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f/LICENSE-gpl3.txt)
- [Upstream original license](https://github.com/libusb/hidapi/blob/7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f/LICENSE-orig.txt)
- [Upstream distribution manifest](https://github.com/libusb/hidapi/blob/7da5cc91fc0d2dbe4df4f08cd31f6ca1a262418f/Makefile.am)

## 3. Build integration and active use

At the reviewed OrcaSlicer revision:

- `deps_src/CMakeLists.txt` adds the `hidapi` subdirectory.
- `deps_src/hidapi/CMakeLists.txt` creates a static `hidapi` target and selects one platform implementation: `win/hid.c` on Windows, `mac/hid.c` on Apple platforms, or `linux/hid.c` otherwise.
- The GUI build links `hidapi` into `libslic3r_gui`.
- `Mouse3DController.cpp` uses HIDAPI for 3D mouse device discovery and access.

This confirms an active GUI build dependency and platform-specific source selection. It does not reveal a licensing election: the CMake file contains no license-selection definition, metadata, or reference to one of the three license documents.

Pinned integration references:

- [deps_src/CMakeLists.txt](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/CMakeLists.txt)
- [HIDAPI CMakeLists.txt](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/deps_src/hidapi/CMakeLists.txt)
- [GUI CMake integration](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/slic3r/CMakeLists.txt)
- [3D mouse consumer](https://github.com/OrcaSlicer/OrcaSlicer/blob/8500fcdccaa10b5099ac20d252af3a7c560046f1/src/slic3r/GUI/Mouse3DController.cpp)

## 4. What the license alternatives mean for this audit

The upstream BSD-style text contains a 2010 copyright notice for Alan Ott / Signal 11 Software and requires preservation of the copyright notice, conditions, and disclaimer in source distributions and reproduction of those items in binary-distribution documentation/materials. The original HIDAPI license instead permits use for any reason so long as the copyright notice in source files remains intact. The GPL option is the full GNU GPL version 3 text.

The upstream GPLv3 text includes section 13, which expressly permits combining a GPLv3-covered work with an AGPLv3-covered work under the stated conditions. This is a fact about the alternative's text, not evidence that OrcaSlicer elected it and not a legal compatibility determination for the complete application.

Because the project has its own licensing context, selecting the most permissive-looking alternative after the fact would be inappropriate. The election must be established from maintainers' contemporaneous records, release/source-distribution notices, or written confirmation from the relevant rights holder/maintainer. If no reliable historical record exists, the maintainers should obtain confirmation before recording an explicit election and adding the corresponding notices.

## 5. Required follow-up

1. Search OrcaSlicer/BambuStudio release source archives and third-party notice bundles for a contemporaneous HIDAPI license election. The reviewed source tree alone does not establish one.
2. If no reliable record exists, obtain written confirmation from the relevant maintainers or rights holder identifying the chosen alternative for this vendored 0.9.0 source.
3. Confirm that the election covers the complete platform source set shipped by this dependency.
4. Restore the selection guide and the selected license text (and any additional notices required by that election) to the derivative source distribution and generated third-party notices.
5. Verify that release packaging actually includes the required notices for source and binary distributions.

Until those steps are complete, retain **license election unknown / notice files omitted** as an explicit blocker. Do not infer a BSD election merely because the project is not intended to be GPL-only, or infer a GPL election from the presence of a GPLv3 option in the header.

## 6. Scope and limitations

This review is documentation-only. It does not modify or import HIDAPI source, make a license election, determine legal compatibility, inspect a built binary/package, or verify the release notice bundle. The fixed source identity, available upstream alternatives, omitted local license files, and active CMake integration are documented; the selected alternative remains unresolved.
