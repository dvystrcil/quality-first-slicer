# Expat duplicate-vendoring and provider-resolution review

**Status:** Source-tree and build-selection review; exact configured provider and release artifact notices remain unresolved  
**OrcaSlicer revision:** `8500fcdccaa10b5099ac20d252af3a7c560046f1` (`v2.4.2`)  
**Scope:** `deps_src/expat`, `deps/EXPAT/expat`, root dependency selection, and application XML parser call sites  
**Method:** Remote inspection of README/version/license files, CMake configuration, and application source. No configured build, generated link command, binary inspection, or release artifact inspection was performed.

## 1. Two distinct vendored source trees

The v2.4.2 repository contains two separate Expat source trees:

| Location | Version stated by its README/header | Integration |
|---|---|---|
| `deps_src/expat` | Expat 2.2.0 | Added unconditionally by `deps_src/CMakeLists.txt`; its CMake file defines a static target named `expat` from `xmlparse.c`, `xmlrole.c`, and `xmltok.c` |
| `deps/EXPAT/expat` | Expat 2.5.0 | Used as the source directory for the `dep_EXPAT` ExternalProject fallback when the dependency build cannot find Expat |

The older `deps_src/expat/README` begins with an explicit integration note: “Release 2.2.0, stripped and modified for inclusion into Slic3r. Only the library sources needed for static linking were left.” Its own README then identifies the upstream release as Expat 2.2.0.

The separate `deps/EXPAT/expat/README.md` identifies Expat 2.5.0 and says that only library-related files were selected for Bambu Studio and built as a static library. Its `expat.h` reports version 2.5.0 and carries a longer, current-to-2022 MIT copyright list.

These are not simply two directory names for one identical version. They are distinct source snapshots and must be tracked independently until the actual build provider and any remaining call sites are established.

## 2. License and attribution evidence

Both copies identify the MIT/X Consortium-style permissive license.

### Expat 2.2.0 under `deps_src/expat`

- The component contains a standalone `COPYING` file.
- It lists Thai Open Source Software Center Ltd and Clark Cooper (1998–2000), and Expat maintainers (2001–2016).
- The permission and warranty terms are the MIT-style grant.
- `expat.h` and `expat_external.h` refer readers to `COPYING`.

### Expat 2.5.0 under `deps/EXPAT/expat`

- The inspected `expat.h` embeds the full MIT license text and an expanded copyright list, including 2022 contributors.
- Its README identifies the source as Expat 2.5.0.
- The exact standalone license-file path and its inclusion in generated package/install outputs were not established in this pass.

The two copies' MIT license family is clear from the checked-in texts. This does not make their source provenance interchangeable: preserve the correct notices for the actual provider and inspect all files in each selected source subset.

## 3. Build selection and application use

The root project CMake states that it will find Expat or use a bundled version, with a comment that Linux should always use the system Expat:

- Root `CMakeLists.txt` calls `find_package(EXPAT)`.
- If Expat is not found, it creates a static target from `${LIBDIR}/expat/xmlparse.c`, `xmlrole.c`, and `xmltok.c`, and sets `EXPAT_INCLUDE_DIRS` and `EXPAT_LIBRARIES`.
- Separately, `deps/CMakeLists.txt` calls `find_package(EXPAT)` and, when absent, includes `deps/EXPAT/EXPAT.cmake`, which declares the `dep_EXPAT` ExternalProject with source directory `deps/EXPAT/expat`.
- The application `libslic3r` target adds `${EXPAT_INCLUDE_DIRS}` and links `${EXPAT_LIBRARIES}`.

At the same time, `deps_src/CMakeLists.txt` unconditionally adds the `expat` subdirectory. Its CMake file defines a static target also named `expat`. This is a potential overlap with the root fallback target of the same name if that fallback branch is reached. The inspected source alone does not establish which configurations reach both definitions or how the project avoids a target-name collision; this requires generated build-system evidence.

Confirmed application-level parser API use includes:

- `src/libslic3r/Format/AMF.cpp` — `XML_ParserCreate` and Expat parser callbacks.
- `src/libslic3r/Format/3mf.cpp` — `XML_ParserCreate` and parser callback setup.
- `src/slic3r/GUI/SkipPartCanvas.cpp` — `XML_ParserCreate` for parsing GUI-side data.

This confirms active Expat API use, but does not identify the concrete library binary or headers resolved in every supported build configuration.

## 4. Findings and remaining work

Established:

- Two distinct vendored Expat source snapshots exist: 2.2.0 in `deps_src/expat` and 2.5.0 in `deps/EXPAT/expat`.
- The older README explicitly describes its source as stripped and modified for Slic3r.
- Both inspected license declarations are MIT-style.
- The 2.2.0 copy is exposed through an unconditional CMake interface directory and static target.
- The root build selects system Expat or a bundled fallback; the ExternalProject fallback points at the separate 2.5.0 tree.
- AMF, 3MF, and GUI sources actively call Expat APIs.

Still open:

1. Capture actual configured build evidence for Linux, macOS, Windows/MSVC, and MinGW, identifying the resolved `EXPAT_INCLUDE_DIRS`, `EXPAT_LIBRARIES`, target dependencies, and final link inputs.
2. Resolve whether the unconditional `deps_src/expat` target is linked, redundant, or only retained for a separate consumer; investigate the apparent target-name overlap with the root fallback.
3. Identify the original upstream commit/tag and checksums for each copy; the README version statements alone are not an exact source pin.
4. Compare the retained files against upstream Expat 2.2.0 and 2.5.0 respectively, documenting local modifications and omitted files.
5. Verify which license/copyright notices are included in each source distribution and binary release artifact for the actual selected provider.
6. Confirm whether any system-Expat build path omits the vendored Expat copies from the shipped product and whether dependency packaging includes the bundled fallback.

This is a technical source/provenance review, not a legal determination. No source, build, dependency, or license files were changed.
