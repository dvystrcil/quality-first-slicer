# fast_float 2.0.0 provenance and license review

**Status:** Upstream version and license identified; exact flattened-header reproduction, consumer include propagation, and release notice staging remain open  
**OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (`v2.4.2`)  
**Upstream project:** [fastfloat/fast_float](https://github.com/fastfloat/fast_float)  
**Scope:** `deps_src/fast_float`, its CMake interface target, import history, source call sites, and About dialog entry  
**Method:** Remote inspection of the fixed OrcaSlicer tag, upstream commit, Git history, and CMake/source references. No configured build, generated compile command, binary, or release artifact was inspected.

## 1. Version and provenance

The vendored `deps_src/fast_float/README.md` explicitly identifies the directory as the **fast_float 2.0.0** source distribution and records upstream short commit `fe1ce58`.

That short identifier resolves in `fastfloat/fast_float` to:

- Full commit: `fe1ce5805331d9edae6fe71f10e0b38c3ac4bbe7`
- Commit message: “Candidate release.” (merge of the v2.0.0 candidate)
- Upstream repository: `https://github.com/fastfloat/fast_float`

The initial OrcaSlicer import is traceable to commit `ad65366ac7c4a8fa527bf87369d781029c858ee4`, titled “Added fast_float library as a replacement for std::from_chars and strtod.” That commit introduced a 2,449-line amalgamated header at `src/fast_float/fast_float.h`, changed G-code numeric parsing to use `fast_float::from_chars`, and added an About-dialog attribution entry naming Daniel Lemire, João Paulo Magalhaes, and contributors.

A later commit, `9e3e565bb66bf2b0b523bccb14dbacd9b24e1a44`, added the README containing the explicit 2.0.0 / `fe1ce58` source-distribution statement. The current v2.4.2 tree retains the amalgamated header at `deps_src/fast_float/fast_float.h`.

The upstream modular header at the pinned commit is not byte-identical to the OrcaSlicer amalgamated header. The README pin is useful provenance evidence, but this review did not reconstruct the amalgamation from all upstream files or verify an archive checksum. The exact generated-header derivation and any local edits therefore remain open.

## 2. License and attribution

The vendored `fast_float.h` begins with the complete MIT permission grant and warranty disclaimer. Its attribution block names:

- Daniel Lemire
- João Paulo Magalhaes
- Contributors Eugene Golushkov, Maksim Kita, Marcin Wojdyr, Neal Richardson, Tim Paine, and Fabio Pellacini

The upstream repository at the pinned commit also contains `LICENSE-MIT`, whose permission and disclaimer text matches the grant embedded in the vendored header.

No separate license-named file was found in the vendored `deps_src/fast_float` subtree during this review. The full license text is nevertheless present in the single vendored header, alongside the author/contributor attribution. Preserve that header notice in any source redistribution and ensure the required notice is retained in applicable distributions.

The current OrcaSlicer v2.4.2 About-dialog row lists fast_float and its upstream URL but leaves the copyright/attribution field empty. The original import commit had populated that field with Daniel Lemire, João Paulo Magalhaes, and contributors. The header itself still carries the attribution and license text; the UI row is not a substitute for the header notice.

## 3. Build integration and active use

The v2.4.2 `deps_src/CMakeLists.txt` unconditionally adds the `fast_float` subdirectory as one of its header-only/interface components.

`deps_src/fast_float/CMakeLists.txt` defines an interface target named `fast_float` and declares:

- Its source directory as a SYSTEM interface include directory.
- `fast_float.h` as an interface source.
- C++14 as an interface compile feature.

The application source contains direct `fast_float/fast_float.h` includes and `fast_float::from_chars` calls in the following files:

- `src/libslic3r/LocalesUtils.cpp`
- `src/libslic3r/GCodeReader.cpp`
- `src/libslic3r/Format/3mf.cpp`
- `src/libslic3r/GCode/PressureEqualizer.cpp`
- `src/slic3r/GUI/DeviceCore/DevUtil.cpp`
- `src/slic3r/GUI/DeviceCore/DevCalib.cpp`
- `src/slic3r/GUI/DeviceManager.cpp`
- `src/slic3r/Utils/EmbossStyleManager.cpp`

These call sites cover locale-independent numeric conversion, G-code parsing, 3MF attribute parsing, pressure-equalizer parsing, and GUI/device/calibration/emboss paths.

**Build-graph caveat:** The interface target and application includes are present, but this pass did not find an explicit `target_link_libraries(... fast_float)` consumer in the reviewed root, `src/CMakeLists.txt`, or `src/libslic3r/CMakeLists.txt`. Nor did it inspect generated compile commands. The mechanism by which the interface include directory reaches every consuming target must be resolved before claiming that the interface target is the effective include provider in each platform build.

## 4. Findings and remaining work

Established:

- The vendored README pins fast_float 2.0.0 and upstream commit `fe1ce5805331d9edae6fe71f10e0b38c3ac4bbe7`.
- The original import and later README addition are traceable in OrcaSlicer Git history.
- The vendored header contains the complete MIT grant/disclaimer and named attribution.
- The upstream pinned repository contains a matching `LICENSE-MIT`.
- The project defines a header-only CMake interface target and has eight identified application source files that include and call fast_float APIs.
- The current About-dialog attribution field is blank, although the original import populated it.

Still open:

1. Reconstruct the amalgamated header from the pinned upstream source distribution, compare it file-for-file, and document any differences or local modifications.
2. Capture configured build evidence (including generated compile commands) to establish how the interface include path reaches the eight consumers on supported platforms.
3. Verify source and binary release notice handling; no release artifact was inspected.
4. Decide whether the About-dialog attribution field should be restored when implementation work begins. The source header's MIT notice must be preserved regardless.

This is a technical provenance and notice review, not a legal determination. No source, build, dependency, or license files were changed.
