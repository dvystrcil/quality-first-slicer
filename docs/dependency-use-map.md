# Dependency/use map and keep/remove/optionalize ranking

**Status:** Current map for the 2.5.0 baseline ([0002](decisions/0002-base-on-orcaslicer-2.5.0.md) step 2). Slice 1 of [#47](https://github.com/dvystrcil/quality-first-slicer/issues/47) (AC1: dependency/use map; AC2: no "unused" claim from a missing include alone). Read-only analysis; **no source, build file or notice has been removed.**
**Analysed source:** fork [`dvystrcil/OrcaSlicer`](https://github.com/dvystrcil/OrcaSlicer) branch `baseline-2.5.0`, commit [`665552c1e4b950b32707953cbca67e178e219366`](https://github.com/dvystrcil/OrcaSlicer/commit/665552c1e4b950b32707953cbca67e178e219366) (upstream v2.5.0 `40ecc66f` plus the fork's CI changes from [OrcaSlicer#3](https://github.com/dvystrcil/OrcaSlicer/pull/3); no slicer source changes)
**Configuration:** Linux x86_64, the fork's CI configure: clang 18.1.3, CMake 3.28.3, `Ninja Multi-Config`, Release, `SLIC3R_GUI=ON`, `SLIC3R_STATIC=ON`, `SLIC3R_PCH=ON`, `SLIC3R_CAD=ON` (default), `ORCA_TOOLS=ON`, `BUILD_TESTS=ON`, `ORCA_BUILD_PYTHON_STUBGEN_MODULE=ON` (default), GTK3. Dependency prefix `deps/build/OrcaSlicer_dep` built by `build_linux.sh -drlL` in the same runner image, `harbor.sirddail.net/arc/orcaslicer-runner@sha256:d3b7f3805ad002e98cf449915557e3ce556a825acfa007024ee43358734639a3`, with the checkout at the CI workspace path
**Reviewed:** 2026-11-08
**Machine-readable result:** [`audit/dependency-use-map-linux-x86_64.json`](../audit/dependency-use-map-linux-x86_64.json)
**Reproduce:** [`tools/dependency-use-map/run.sh`](../tools/dependency-use-map/run.sh)
**History:** the v2.4.2 analysis is kept unchanged in [dependency-use-map-v2.4.2.md](dependency-use-map-v2.4.2.md) and [`audit/dependency-use-map-linux-x86_64-v2.4.2.json`](../audit/dependency-use-map-linux-x86_64-v2.4.2.json). The R/O item IDs below carry over from it.

This is an engineering reachability analysis. Where it mentions license text, it records what the files say so that qualified reviewers know where to look. It does not reach legal conclusions. Provenance and license review of the new components is [0002](decisions/0002-base-on-orcaslicer-2.5.0.md) step 3 and is **not** done here.

## 0. What changed since the v2.4.2 map

| | v2.4.2 (`5ed77f50`) | 2.5.0 (`665552c1`) |
|---|---:|---:|
| Release TUs scanned (`clang -M`, PCH excluded) | 801, 0 failures | **1123**, 0 failures |
| Graph nodes in the `OrcaSlicer` link closure | 238 | 253 (the JSON lists 254: the 2.5.0 graph has an `OrcaSlicer -> OrcaSlicer` self-edge, so the root appears in its own closure) |

- **R1 (OpenCSG + GLEW) is gone.** `deps/OpenCSG`, `deps/GLEW` and `sandboxes/opencsg` no longer exist, and no CMake file in the tree mentions either. Neither appears in the graph or in any TU closure.
- **Legacy Clipper is gone.** `deps_src/clipper` (118 app TUs on 2.4.2) no longer exists. Polygon clipping is Clipper2 only, through `L/ClipperUtils.cpp` and `L/ClipperZUtils.cpp`.
- **FreeType is gone** from the deps superbuild and the link closure.
- **GStreamer is no longer included by any TU.** `wxMediaCtrl2.cpp` and `gstbambusrc.c` were replaced by the FFmpeg-based `wxMediaCtrl3.cpp`. The GStreamer `.so` files are still on the link line, through the wxWidgets media library.
- **OpenCV's bundled libpng is gone** (`deps/OpenCV/OpenCV.cmake:40-42`: `BUILD_PNG=OFF`, "Share Orca's libjpeg and libpng"). This closes part (b) of O5.
- **Six new dependency projects**, all with real consumers in this configuration (section 3.2). None is unused.
- **New finding: zlib now resolves to Assimp's bundled copy** (section 3.4). This is a provenance change, not a removal candidate.
- **New candidate O7: wxInspector**, a developer UI inspector. It is compiled to no-ops in Release, but it is still linked.
- **Still present and unchanged in substance:** R2, R3, R4, O1 (mdns), O2 (hidapi + libspnav), O3 (OpenVDB only for SLA hollowing), O4 (MCUT). Section 4 re-checks each one.

## 1. Method

Unchanged from [v2.4.2 §1](dependency-use-map-v2.4.2.md#1-method): CMake `--graphviz` and the File API give the link graph, and `clang -M` on every Release TU from `compile_commands.json`, with the PCH force-include removed, gives each TU's own preprocessor closure. Symbol spot checks (`grep` for API calls in the consumer TUs that layer 2 found) cover every decision-relevant entry. The coverage limits in [v2.4.2 §1](dependency-use-map-v2.4.2.md#coverage-limits-ac2) still apply: one platform and one configuration, runtime-loaded code not mapped, and header-level is not object-level.

Tool changes made for 2.5.0, in this same change:

- **Build-time generated header.** 2.5.0 adds `git_commit_hash.h`, included by `src/slic3r/GUI/BuildCommit.cpp`. A custom target (`git_commit_hash_header`) writes it at **build** time, not configure time, so the first 2.5.0 run had 1 preprocessing failure (`'git_commit_hash.h' file not found`) and exited without SCAN-COMPLETE. `run.sh` now runs that one target, which only runs `cmake -P GitCommitHash.cmake` and compiles nothing, before the `-M` pass. It is skipped when the target does not exist, as on 2.4.2. The generated value was `665552c1`, not dirty.
- **Bundled CPython.** `deps/python3` installs CPython under `<prefix>/libpython/`, not `<prefix>/include/`, so `analyze.py` silently dropped those headers. It now classifies them as `prefix/python3`, with a unit test.

Configure is not network-free in 2.5.0. With `ORCA_BUNDLED_UV_EXECUTABLE` unset (the default), the root `CMakeLists.txt` downloads a SHA-256-pinned prebuilt `uv` 0.11.21 binary (about 60 MB) into `build/.uv/` during configure, and that binary ships inside the application. Section 3.4 records this as a binary-provenance item for step 3.

## 2. Build-graph findings

### 2.1 Targets built but not in the application link closure

| Target | Kind | Change since 2.4.2 | Consequence |
|---|---|---|---|
| `agg`, `ankerl`, `earcut`, `fast_float`, `nanosvg`, `nlohmann_json`, `stb_dxt` | Header-only INTERFACE | unchanged | **Not unused.** Reached through `deps_src/admesh/..` (2.2); section 3 shows 1–445 app TUs each |
| `expat` (`deps_src/expat`) | STATIC, 16 sources | unchanged | No consumer: 0 TUs include its headers. R2 |
| `Shiny` | STATIC, 20 sources | unchanged | Linked only with `SLIC3R_PROFILE` (`src/libslic3r/CMakeLists.txt:809-810`). R4 |
| `orca_stubgen` | MODULE | **new** | Python module used by `pybind11-stubgen` to generate plugin type stubs (`ORCA_BUILD_PYTHON_STUBGEN_MODULE`, default ON). Not shipped in the app closure. Part of O8 |
| `generate_system_cache`, `profile_include_dump`, `texture_unwrap_dump` | Executables in `src/dev-utils` | **new** | Developer tools. Keep |
| `hints`/`hintsToPot`, `encoding-check`, `OrcaSlicer_profile_validator`, `*_tests`, `Catch2*` | Tools / tests | unchanged | Keep |

### 2.2 The `deps_src/admesh/..` include path

Unchanged (`deps_src/admesh/CMakeLists.txt:17`). Every target that links `admesh` can include any vendored component under `deps_src/` without a CMake edge, so removal PRs must check the TU closure, not only the graph.

### 2.3 Dependency-superbuild (`deps/`) projects with no consumer

**None in 2.5.0.** Every project in `_dep_list` (`deps/CMakeLists.txt:462-496`) is reached by at least one application TU or is a transitive build dependency of one that is (GMP, MPFR, Blosc, OpenEXR). The 2.4.2 case, OpenCSG + GLEW, was removed upstream.

## 3. Use map (application consumers)

Columns and abbreviations are as in v2.4.2: **App TUs** counts TUs in the `OrcaSlicer` link closure whose own include closure reaches the component, with the PCH excluded. `L/` means `src/libslic3r/`, `S/` means `src/slic3r/`.

### 3.1 Vendored `deps_src/` components

| Component | App TUs (2.4.2 → 2.5.0) | Callers / main consumers | Feature |
|---|---:|---|---|
| admesh | 292 → 328 | via `TriangleMesh.hpp` | STL load + repair (core) |
| agg | 5 → 5 | FDM support, SLA raster, emboss font preview | Rasterisation |
| ankerl | 6 → 7 | Arachne, concentric fill | Arachne walls |
| clipper | 118 → **removed** | — | Legacy Clipper removed upstream |
| clipper2 | 2 → 2 | `L/ClipperUtils.cpp`, `L/ClipperZUtils.cpp` (was `Clipper2Utils.cpp`, `FillBase.cpp`) | Polygon clipping (core: now the only clipper) |
| earcut | 1 → 1 | `S/GUI/SkipPartCanvas.cpp` | Part-skip canvas |
| fast_float | 9 → 10 | 3MF, G-code parsing | Number parsing (core) |
| glu-libtess | 1 → 1 | `L/Tesselate.cpp` | Polygon triangulation |
| hidapi | 5 → 5 | `S/GUI/Mouse3DController.cpp` (+ `GLCanvas3D`, `GUI_App`, `MainFrame`, `Plater` through `Mouse3DController.hpp`) | 3D mouse (O2) |
| imgui | 280 → 270 | GUI-wide | GUI (core) |
| imguizmo | 1 → 1 | `S/GUI/GLCanvas3D.cpp` | View gizmo |
| libigl | 42 → **288** | `L/AABBTreeIndirect.hpp` now includes libigl headers, so every TU that includes it is counted. 170 vendored headers reached | Mesh algorithms |
| libnest2d | 8 → 9 | Arrange | Arrange (core) |
| mcut | 1 → 1 | `L/MeshBoolean.cpp`; callers `L/Model.cpp`, `S/GUI/Plater.cpp`, `S/GUI/Gizmos/GLGizmoMeshBoolean.cpp` | Mesh boolean / cut (O4) |
| md4c | 1 → 1 | `S/GUI/ReleaseNote.cpp` | Release-notes rendering |
| mdns | 1 → 1 | `S/Utils/CrealityHostDiscovery.cpp` (`cxnet::syncDiscoveryService`, line 89) ← `CrealityDiscoveryDialog` ← `PhysicalPrinterDialog.cpp:184` | Creality LAN discovery (O1) |
| **minilzo** | 1 → 1 | `S/Utils/minilzo_extension.cpp` only; still **0 callers** of `lzo_compress`/`lzo_decompress` outside it | **None** (R3) |
| miniz | 27 → 28 | 3MF, archive I/O | Project files (core) |
| nanosvg | 257 → 270 | GUI icons, emboss | SVG (core) |
| nlohmann | 360 → 445 | ubiquitous | JSON (core) |
| **pybind11** (new) | — → **27** | Python plugin host (`S/plugin/*`), `S/GUI/PostProcessor.cpp`, `TerminalDialog.cpp`, `PluginsConfigDialog.cpp`, `PluginPermissionValidation.cpp`, `GUI_App.cpp`, `S/Utils/NetworkAgentFactory.cpp`; +14 test TUs, +1 `orca_stubgen` | Python plugins (O8) |
| qoi | 1 → 1 | `L/GCode/Thumbnails.cpp` | QOI thumbnails |
| semver | 494 → 629 | ubiquitous | Version handling (core) |
| Shiny | 4 → 4 | `L/GCode.cpp`, `GCodeReader.cpp`, `PrintObject.cpp`, `pchheader.cpp`; macros empty without `SLIC3R_PROFILE` | **None** in default build (R4) |
| stb_dxt | 1 → 1 | `S/GUI/GLTexture.cpp` | Texture compression |
| expat (vendored) | 0 → **0** | — | **None** (R2) |
| qhull (vendored) | 0 → **0** | — | **None on Linux**; prefix Qhull is used |

### 3.2 The six dependency projects added in 2.5.0

All six have real consumers in this configuration. None is a "remove: unused" candidate. Each is a G4 keep/optionalize/remove question ([goals Q17](goals.md)), so each needs a product decision as well as the provenance review in step 3.

| Project | Version / source (from `deps/<name>/*.cmake`) | App TUs | Consumer → feature | Call check | How it is linked (Linux) | Gate |
|---|---|---:|---|---|---|---|
| **Assimp** | v5.4.3 (v5.3.1 when CMake < 3.22), GitHub tag tarball, SHA-256 pinned | 1 | `L/Format/AssimpImport.cpp` ← `L/Model.cpp:441-448`: **`.glb`, `.gltf`, `.fbx` import** with textures, handed to the texture-to-colour dialog | `load_assimp_textured_model` called from `Model.cpp:448`; `Assimp::Importer` used | `assimp::assimp` (`libassimp.a`) + `assimp::zlibstatic` (Assimp's bundled zlib, see 3.4) | none (always on) |
| **DataChannel** (libdatachannel) | v0.24.5, **git clone by tag** (`deps/DataChannel/DataChannel.cmake:18`), not a hashed archive | 1 | `S/GUI/WebRtcMediaController.cpp` ← `S/GUI/MediaPlayCtrl.cpp:216` (`CameraStreamMode::webrtc`): **printer camera over WebRTC** | 21 `rtc::` uses | `LibDataChannel::LibDataChannel` (`libdatachannel.a`, plus bundled `libjuice.a` and `libusrsctp.a` in the prefix) | none |
| **FFMPEG** | n7.0.3 source build on Linux/macOS; **prebuilt shared zip from `Noisyfox/FFmpeg-Builds-Orca` on MSVC** (`deps/FFMPEG/FFMPEG.cmake`) | 2 | `S/GUI/AVVideoDecoder.cpp`, `S/GUI/wxMediaCtrl3.cpp` ← `MediaPlayCtrl`, `StatusPanel`: **printer camera / timelapse decoding** (replaces GStreamer) | 30 `av*`/`sws_` uses in `AVVideoDecoder.cpp`, 17 in `wxMediaCtrl3.cpp` | **Shared**: `libavformat/avcodec/swscale/avutil.so` from the prefix via pkg-config (`PkgConfig::LIBAV`, `src/slic3r/CMakeLists.txt:1049-1056`). Static on macOS, prebuilt DLLs on Windows | none |
| **SLVS** (SolveSpace solver) | `deps/SLVS` | 1 | `L/CAD/SketchSolver.cpp` ← `L/CAD/CadDocument.cpp`, `S/GUI/CAD/DesignPanel.cpp`, `DesignSketchTool.cpp`: **parametric Design/CAD tab** | 46 `Slvs_` uses | `SLVS::slvs` (`libslvs.a`) | **`SLIC3R_CAD`** (default ON, root and `deps/` must match). The same option also pulls in the OCCT modelling modules (`TKBool`, `TKFillet`, `TKOffset`, new in the closure) |
| **python3** + **pybind11** | CPython 3.12.13 built into `<prefix>/libpython` (`deps/python3`); pybind11 vendored in `deps_src/pybind11` | 27 (pybind11) / 27 (`prefix/python3`) | **Python plugin system**: plugin manager, plugin host bindings (mesh, slicing, presets, UI), script and printer-agent plugin types, post-processor, terminal dialog; `NetworkAgentFactory` registers **Python printer-agent plugins** | real pybind11 API use across `S/plugin/*` | `pybind11::embed` → `Python3::Python` (bundled **shared** libpython); `uv` binary bundled for package installs (3.4) | none for the plugin host; `ORCA_BUILD_PYTHON_STUBGEN_MODULE` only for `orca_stubgen` |
| **wxInspector** | v1.0.0, `github.com/Noisyfox/wxInspector` tag zip, SHA-256 pinned (`deps/wxInspector/wxInspector.cmake:26-27`) | 229 (header) | `S/GUI/GUI_Utils.hpp:107`: `DPIAware<P>` (base of most windows) inherits `wxInspector::wxInspectable`; `GUI_App.cpp:3215` calls `RegisterOrcaInspectorPlugins()`; plugins in `S/Utils/wxInspectorPlugins/*` | **In Release, `WXINSPECTOR_DISABLE` is defined** (`CMakeLists.txt:102`), so `RegisterPlugin` and `wxInspectable` become empty inline stubs (`<prefix>/include/wx/inspector/inspector.h:15-23, 56-66`) | `wxInspector::wxInspector` (`libwxInspector.a`), linked by both `OrcaSlicer` (`src/CMakeLists.txt:194`) and the wx library list (`:110`). It also pulls `libwx_gtk3u_propgrid-3.3.a` into the closure (`src/CMakeLists.txt:36`: "propgrid is required by wxInspector") | Release: functionally off. Debug: on. See O7 |

### 3.3 Other dependency-prefix (`deps/`) components

| Component | App TUs (2.4.2 → 2.5.0) | Callers / main consumers | Feature |
|---|---:|---|---|
| Boost, Eigen, oneTBB, cereal | 435–572 → 542–743 | ubiquitous | Core |
| OpenSSL / curl | 396 / 242 → 452 / **17** | curl headers are no longer included transitively by most GUI TUs | Network, updates |
| wxWidgets 3.3 | 323 → 416 | GUI | Core GUI |
| OCCT | 247 → 265 (include dir renamed `opencascade` → `occt`; STEP toolkits now `TKDESTEP`/`TKDE`; `TKBool`/`TKFillet`/`TKOffset` added for CAD) | `L/Format/STEP.*`, CAD | STEP import, CAD tab |
| CGAL (+ GMP, MPFR) | 5 → 9 | cut, boolean, Voronoi checks, triangulation | Core modelling |
| OpenCV `world` | 6 → 6 | `L/ObjColorUtils.cpp`, **`L/TexturePainting.cpp`, `L/TextureToColor/TextureToColor.cpp`, `src/OrcaSlicer.cpp`** (new), `S/GUI/PartSkipDialog.cpp`, `SkipPartCanvas.cpp` | Colour clustering, texture-to-colour, part-skip |
| NLopt | 5 → 4 | libnest2d, `L/Arrange.cpp`, `L/SLA/SupportTree*.cpp` | Arrange |
| Qhull (prefix) | 1 → 1 | `L/TriangleMesh.cpp` | Convex hull |
| OpenVDB (+ Blosc, OpenEXR) | 2 → 2 | `L/OpenVDBUtils.cpp`, `L/SLA/Hollowing.cpp` only. The FDM tree-support OpenVDB path is still compiled out (`L/Support/TreeSupport3D.cpp:80` defines `TREE_SUPPORT_ORGANIC_NUDGE_NEW`) | **SLA hollowing only** (O3 / [0003](decisions/0003-remove-sla.md)) |
| Draco | 1 → 1 | `L/Format/DRC.cpp` | `.drc` import |
| libnoise | 1 → 1 | `L/Feature/FuzzySkin/FuzzySkin.cpp` | Fuzzy skin |
| libjpeg-turbo / libpng | 1 / 2 → 1 / 2 | `L/GCode/Thumbnails.cpp`; `L/PNGReadWrite.cpp`, `L/EdgeGrid.cpp` | Thumbnails, PNG I/O |
| GLFW | 1 → 1 | `src/OrcaSlicer.cpp:7526` (`glfwInit`) | CLI thumbnails |
| FreeType | link only → **removed** | — | — |
| OpenCSG + GLEW | 0 → **removed** | — | R1 done upstream |

### 3.4 System libraries, duplicates and new provenance observations

| Item | Observation |
|---|---|
| libspnav | Still linked statically when found (`/usr/lib/libspnav.a` on the runner; `CMakeLists.txt:1073-1084`, `src/slic3r/CMakeLists.txt:1009-1010`). Only consumer `S/GUI/Mouse3DController.cpp` (O2) |
| webkit2gtk-4.1, libsoup-3.0 | 1 → 2 TUs: `S/GUI/PrinterWebView.cpp`, `S/GUI/WebViewDialog.cpp` |
| GStreamer | 2 → **0** TUs. Still on the link line through `libwx_gtk3u_media`. Whether any GStreamer symbol is still resolved was not traced |
| libsecret | Still link-only (wx `wxSecretStore`) |
| D-Bus | 1 TU, `S/GUI/InstanceCheck.cpp` |
| Wayland client | **New**: 1 TU, `S/GUI/LinuxDisplayBackend.cpp` |
| Expat (system) | 7 app TUs, `/usr/lib/x86_64-linux-gnu/libexpat.so` (`EXPAT_LIBRARY_RELEASE` in the CMake cache) |
| **zlib** | **Changed provider.** The app's `find_package(ZLIB)` now resolves `ZLIB_LIBRARY_RELEASE` to `<prefix>/lib/libzlibstatic.a`, while `ZLIB_INCLUDE_DIR` is the runner's `/usr/include` (zlib.h `1.3`). `libzlibstatic.a` was installed by `dep_Assimp` (its `install_manifest.txt`), which builds Assimp's **bundled `contrib/zlib`** on non-Apple platforms (`deps/Assimp/Assimp.cmake:14-18`, `ASSIMP_BUILD_ZLIB=ON`). Its strings report **deflate/inflate 1.2.13**. On 2.4.2 the closure linked system `libz.so`. The wxWidgets link list also names this archive. Result: on Linux the whole application likely uses Assimp's vendored zlib 1.2.13, compiled against 1.3 headers. Which archive resolves each `deflate*`/`inflate*` symbol was not traced. **For step 3**, not a removal |
| **`uv` binary** | **New.** A prebuilt `uv` 0.11.21 executable is downloaded at configure time from `github.com/astral-sh/uv` releases, with per-triple SHA-256 pins in the root `CMakeLists.txt:125-197`. It is installed into the app's resources (`CMakeLists.txt:1293`, `:1318`; copied next to the binary by `src/CMakeLists.txt:370-374`) for Python package installation by plugins. Binary-provenance item like the [Windows binaries](windows-binary-provenance.md). **For step 3** |
| **FFmpeg on Windows** | Prebuilt shared zip from a third-party GitHub account (`Noisyfox/FFmpeg-Builds-Orca`, `deps/FFMPEG/FFMPEG.cmake`). Already flagged in [0002](decisions/0002-base-on-orcaslicer-2.5.0.md). **For step 3** |
| Duplicates | Polygon clipping is now **one** implementation (Clipper2). Triangulation is still three (glu-libtess, earcut, CGAL). PNG is now **one** copy (OpenCV no longer bundles libpng). Expat is still duplicated (vendored 2.2.0 unused, R2). Qhull is still duplicated (vendored unused on Linux). zlib: see above |

## 4. Ranked decision list, re-checked on 2.5.0

Maintainer decisions: SLA is to be removed ([0003](decisions/0003-remove-sla.md)), Creality discovery is to be removed ([0004](decisions/0004-remove-creality-lan-discovery.md)), and the 3D mouse becomes an option that is off in project builds ([0005](decisions/0005-3d-mouse-optional-off.md)). Ranking, burden and risk wording for the unchanged items are in [v2.4.2 §4](dependency-use-map-v2.4.2.md#4-ranked-decision-list); only what 2.5.0 changes is repeated here.

### Remove: no consumer in the analysed configuration

| Rank | Candidate | 2.5.0 status | Evidence on 2.5.0 | Validation for the removal PR |
|---|---|---|---|---|
| **R1** | OpenCSG 1.4.2 + GLEW | **Done upstream** | Directories gone; no CMake file mentions either; not in the graph or in any TU closure | none: nothing to remove |
| **R2** | `deps_src/expat` (vendored 2.2.0) + dead root fallback | **Still applies** | Target still built (`deps_src/CMakeLists.txt:19`), 0 consumer TUs, not linked. The root fallback moved to `CMakeLists.txt:899-913` and still points at `${LIBDIR}/expat` = `src/expat`, **which does not exist**. `deps/CMakeLists.txt:368-372` still builds `dep_EXPAT` when not found | unchanged: needs a Windows x64 configure first ([0001](decisions/0001-supported-platforms.md)) |
| **R3** | minilzo | **Still applies** | Still linked (`src/slic3r/CMakeLists.txt:969`, sources `:789-790`); `minilzo_extension.cpp` is still its only includer; no callers of `lzo_compress`/`lzo_decompress` anywhere else in `src/` | unchanged: linker trace, then remove |
| **R4** | Shiny | **Still applies** | Still `add_subdirectory(Shiny)` unconditionally (`deps_src/CMakeLists.txt:16`); linked only under `SLIC3R_PROFILE` | unchanged |

### Optionalize: real consumer, behind an optional feature

| Rank | Candidate | 2.5.0 status | Evidence / change on 2.5.0 |
|---|---|---|---|
| **O1** | mdns / Creality LAN discovery | **Still applies; decided: remove ([0004](decisions/0004-remove-creality-lan-discovery.md))** | Same single call site and the same caller chain (section 3.1). Removal unit unchanged: `deps_src/mdns`, `CrealityHostDiscovery.*`, `CrealityDiscoveryDialog.*`, the branch in `PhysicalPrinterDialog.cpp`, and `mdns` in the `libslic3r_gui` link line (`src/slic3r/CMakeLists.txt:969`) |
| **O2** | hidapi + libspnav / 3D mouse | **Still applies; decided: option, off in project builds ([0005](decisions/0005-3d-mouse-optional-off.md))** | `hid_*` and `spnav_*` calls still only in `Mouse3DController.cpp`; header still included by `GLCanvas3D`, `GUI_App`, `MainFrame`, `Plater` (stub needed). `Mouse3DHandlerMac.mm` still present |
| **O3** | OpenVDB (+ Blosc, OpenEXR) / SLA | **Still applies; decided: remove SLA ([0003](decisions/0003-remove-sla.md))** | OpenVDB still only in `OpenVDBUtils.cpp` and `SLA/Hollowing.cpp`. `Plater.cpp:7211` still holds an `SLAPrint`; `src/libslic3r/SLA/` has 34 files. All 276 `printer_technology` entries in bundled profiles are `FFF` (2.4.2: 239) |
| **O4** | MCUT → CGAL | **Still applies** | Still 1 TU (`L/MeshBoolean.cpp`). Callers are now `L/Model.cpp`, `S/GUI/Plater.cpp` and `S/GUI/Gizmos/GLGizmoMeshBoolean.cpp` |
| **O5** | OpenCV | **Half done upstream** | (b) **done**: no bundled libpng (`BUILD_PNG=OFF`). (a) **still applies**: `WITH_IPP=ON` on MSVC, now x64 only (`deps/OpenCV/OpenCV.cmake:1-10` excludes ARM64) |
| **O6** | Printer-integration GUI stack | **Grew** | Now webkit2gtk/libsoup (2 TUs), **FFmpeg** (camera/timelapse decode, replaces GStreamer), **libdatachannel** (WebRTC camera), libsecret. FFmpeg and DataChannel join this item rather than being separate ranks: they share one consumer path (`MediaPlayCtrl` / `StatusPanel`) and one product question (printer integration, [product vision](product-vision.md) "Offline-first core"). Still deferred to that decision |
| **O7** (new) | **wxInspector** | **New** | Developer-only UI inspector. In Release builds its API compiles to empty stubs (`WXINSPECTOR_DISABLE`, section 3.2), yet `libwxInspector.a` and `libwx_gtk3u_propgrid` are linked and the plugin TUs in `S/Utils/wxInspectorPlugins/` are compiled. Proposal: keep it for Debug, and do not build or link it in Release. **Risk: low–medium.** `DPIAware<P>` inherits `wxInspectable`, so the stub header must stay reachable (or move into the tree) even when the library is not linked. **Validation:** a linker trace (`--why-extract`) to see which `libwxInspector.a` objects a Release link extracts today; a Release build without it; Debug inspector still works |
| **O8** (new) | **Python plugin system** (CPython 3.12 + pybind11 + bundled `uv`) | **New** | Large new feature with 27 app TUs, a bundled shared CPython, a downloaded `uv` binary, and runtime package installation by plugins. Python printer-agent plugins also plug into `NetworkAgentFactory`. Needs a product decision (keep, make optional, or remove) before any technical work; the security and supply-chain questions (code execution from plugins, packages fetched at runtime) are larger than the license question. Not proposed for removal here |

### Keep: core or required by a core feature

admesh, clipper2, libigl, CGAL + GMP + MPFR, libnest2d + NLopt, Qhull (prefix), glu-libtess, earcut, agg, ankerl, fast_float, nanosvg, nlohmann, miniz, md4c, qoi, stb_dxt, imgui, imguizmo, semver, glad, GLFW (CLI thumbnails), libjpeg-turbo, libpng, Draco, libnoise, OCCT, Boost, Eigen, oneTBB, cereal, wxWidgets, curl, OpenSSL, system Expat.

Changes from v2.4.2: **clipper** and **FreeType** left the list (removed upstream).

**New projects without a decision yet** ([goals Q17](goals.md)): **Assimp** (`.glb`/`.gltf`/`.fbx` textured import) and **SLVS** (CAD tab, already behind `SLIC3R_CAD`) have a single clear consumer each. Each becomes a keep or an optionalize once the product decides on those features. FFmpeg and DataChannel are under O6, wxInspector is O7, and python3 + pybind11 are O8.

**Undecided, needs platform evidence:** vendored `deps_src/qhull` (unchanged; `deps/CMakeLists.txt:489-491` still comments out `dep_qhull` for MSVC).

## 5. Platform caveats for the ranked items

| Item | Linux x86_64 (this run) | Windows x64 |
|---|---|---|
| R2 vendored expat | verified unused | depends on `find_package(EXPAT)`. **Unverified** |
| R3 minilzo | verified uncalled | same source list |
| O2 hidapi | `linux/hid.c` | `win/hid.c` |
| O5 OpenCV IPP | `WITH_IPP=OFF` | `WITH_IPP=ON` (x64) |
| FFmpeg | source build, shared `.so` | **prebuilt DLLs** from a third-party build |
| zlib | Assimp `contrib/zlib` 1.2.13 (3.4) | `ASSIMP_BUILD_ZLIB=ON` there as well. **Unverified** which zlib the app resolves |
| deps_src/qhull | unused | MSVC likely active. **Unverified** |

## 6. Follow-ups

The removal and option PRs listed in [v2.4.2 §6](dependency-use-map-v2.4.2.md#6-proposed-follow-up-prs-small-independent) still apply, **except R1 (done upstream) and O5(b) (done upstream)**. Each removal PR re-runs `run.sh` and commits the updated JSON. New items from this run:

- **Step 3 (provenance delta review):** the six new projects, plus three binary or vendored-copy items this run found: the bundled `uv` binary, Assimp's `contrib/zlib` becoming the app's zlib, and the bundled libjuice/usrsctp inside libdatachannel. Not started here.
- **O7 wxInspector** and **O8 Python plugins**: product decisions first.
- **Assimp** and **SLVS**: keep/optionalize decisions ([goals Q17](goals.md)).

## 7. Reproducing

```bash
# OrcaSlicer checkout with a CI-built dependency prefix at deps/build/OrcaSlicer_dep,
# built in the same runner image with the checkout at /__w/OrcaSlicer/OrcaSlicer
# (the prefix is not relocatable). Output dir needs ~320 MB (60 MB of it is the uv download).
tools/dependency-use-map/run.sh ~/src/OrcaSlicer /scratch/qfs-depmap <runner-image>
```

On 2.5.0 with 10 parallel jobs the run took about 5.5 minutes. It must print `SCAN-COMPLETE`, and `depsnp/failed.log` must be absent or empty. Configure needs network access (uv download, section 1).
