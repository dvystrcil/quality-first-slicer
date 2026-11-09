# wxInspector provenance and license review (OrcaSlicer 2.5.0)

**Status:** Source and license-file review. Not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off. The keep/Release-off proposal is O7 in the [use map](dependency-use-map.md#4-ranked-decision-list-re-checked-on-250) and is not decided here.
**Slice:** B6 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (build files identical to upstream v2.5.0 `40ecc66f`)
**Method:** read `deps/wxInspector/wxInspector.cmake`; extracted the hash-verified archive and searched every file for license or copyright text; GitHub API for repository and tag metadata.
**Reviewed:** 2026-11-09

## 1. Source and pin

| | |
|---|---|
| URL | `https://github.com/Noisyfox/wxInspector/archive/refs/tags/v1.0.0.zip` (`deps/wxInspector/wxInspector.cmake:26`) |
| SHA-256 (declared and verified) | `0ba163956f2d468b19a91b96c5aba66ee9610843ea41dda628ea44cdafde7db7` (`:27`) |
| Tag → commit | annotated tag `b1f2c9c5…` → commit **`f634a2708ba568766c280417ab4019f8abe77994`**, tagged 2026-07-26, signature: unsigned. That commit is also the HEAD of the default branch |
| Repository | `Noisyfox/wxInspector`: a GitHub **user** account, not an organisation; not a fork; GitHub license detection: **none** |
| Build options | `-DwxDEBUG_LEVEL=0`, PIC; Windows path hints (`:1-22`, `:28-32`) |

## 2. Contents

The archive holds `CMakeLists.txt`, `cmake/`, `include/wx/inspector/*.h` (12 headers), `src/*.cpp` (10 sources), `samples/minimal`, `README.md`, `.gitignore`, and `docs/` (a design document, a screenshot, and dated planning and specification notes under `docs/superpowers/`).

## 3. License evidence

| Where | What it says |
|---|---|
| `LICENSE` / `COPYING` file | **None in the archive.** `docs/design.md:266` shows a planned `LICENSE` in the intended layout, but no such file exists at the tag |
| Source and header files | **No copyright or license notice in any `.h` or `.cpp` file** |
| `README.md:74-76` | "## License" followed by "wxWindows License (same as wxWidgets)" |
| `README.md` (top) | "Ported from [wxPython's `wx.lib.inspection`](https://github.com/wxWidgets/Phoenix)." |

So the only license statement is one README line, with no license text, no copyright holder and no year.

## 4. What the application links

From the [use map §3.2](dependency-use-map.md#32-the-six-dependency-projects-added-in-250): `DPIAware<P>` (the base of most windows) inherits `wxInspector::wxInspectable` in 229 app TUs. In Release, `WXINSPECTOR_DISABLE` turns the API into empty inline stubs, but `libwxInspector.a` is still linked, and so is `libwx_gtk3u_propgrid-3.3.a` ("propgrid is required by wxInspector"). The plugins in `src/slic3r/Utils/wxInspectorPlugins/` are compiled. Which library objects a Release link actually extracts was not traced (proposed validation in O7).

## 5. Open questions

1. **No license text and no copyright notice in the distributed files.** Whether one README line is a sufficient license grant, and who the copyright holder is, are questions for the maintainer or a qualified reviewer. The step that would settle it is asking upstream to add a `LICENSE` file with the full text and a copyright line.
2. **"Ported from" wxPython's `wx.lib.inspection`.** If code was translated from that module, its own copyright and license notices may apply. wxPython states the wxWindows Library Licence, but that was not checked against `wx.lib.inspection` here, and the port was not compared with it.
3. The header stubs stay in 229 TUs even if the library is dropped from Release, so the header's own licensing matters either way.

## 6. Approval

**Not approved.** This records what the files say. Given open question 1, it is the weakest-documented of the six new components. A maintainer sign-off and the O7 decision are still needed.
