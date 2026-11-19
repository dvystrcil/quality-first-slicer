# FFmpeg Windows prebuilt binaries: provenance and license review (OrcaSlicer 2.5.0)

**Status:** Hash, build-recipe, source-traceability and license review of the two **prebuilt** Windows FFmpeg zips. Not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off. The Linux/macOS source build is [B3](ffmpeg-source-build-license-review.md). The printer-integration question O6 in the [use map](dependency-use-map.md#4-ranked-decision-list-re-checked-on-250) is not decided here.
**Slice:** C1 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (build files identical to upstream v2.5.0 `40ecc66f`)
**Method:** hash-verified both zips with [`tools/verify-source-archives.py`](../tools/verify-source-archives.py) and the [binary manifest](../audit/orcaslicer-v2.5.0-binary-artifacts.json); compared with the release's `checksums.sha256` and the GitHub asset digests; listed the zips and read `LICENSE.txt`, the `.pc` files, the configure string and license string embedded in the DLLs (`strings`) and the DLL import tables (`objdump -p`). Nothing was executed. Recipe and run facts come from the GitHub API for `Noisyfox/FFmpeg-Builds-Orca` and `FFmpeg/FFmpeg`. No Windows build of OrcaSlicer was run.
**Reviewed:** 2026-11-19

## 1. Pin and integrity

| | x64 | arm64 |
|---|---|---|
| URL (`deps/FFMPEG/FFMPEG.cmake:17-20`) | `…/autobuild-2026-09-18-16-50/ffmpeg-n7.0.3-33-g887d4b4919-win64-orca-shared-7.0.zip` | `…/winarm64-orca-shared-7.0.zip` (same release) |
| Declared SHA-256 | `85da19da…9c6dae` | `da480cbb…14b4c1` |
| Downloaded bytes | 5,152,939, **PASS** | 4,729,688, **PASS** |
| Release `checksums.sha256` | same digest | same digest |
| GitHub asset `digest` | same digest | same digest |

Selected by `DEPS_ARCH` under `if (MSVC)` (`:14-33`). The zip's `bin/`, `lib/` and `include/` are copied into the deps prefix (`:29-31`); nothing is built.

No GitHub artifact attestation exists for these assets (`gh attestation verify` returns HTTP 404 for the x64 digest), so the binary-to-run link below rests on names and timestamps, not on a signature.

## 2. Build recipe and source traceability

| Fact | Evidence |
|---|---|
| Builder | `Noisyfox/FFmpeg-Builds-Orca`, a fork of `FFmpeg-Builds/FFmpeg-Builds` (BtbN's scripts); repository license MIT (the scripts, not FFmpeg) |
| Run that produced the release | Actions run [35353500443](https://github.com/Noisyfox/FFmpeg-Builds-Orca/actions/runs/35353500443) "Build FFmpeg", `workflow_dispatch` on branch `orca` at **`eadd8235d9c4eae8c621713e17cfac3dd229372f`**, started 2026-09-18 13:59:48 UTC, finished 16:50:55 UTC; all nine jobs succeeded, including "Publish release". The release was published at 16:50:52 UTC |
| Release tag commit | The tag points at `1f74efed` on `master`, **not** the recipe commit. The workflow creates every release with `gh release create … --target "master"` (`.github/workflows/build.yml` at `eadd8235`), and `master` predates the orca variants (`1f74efed` is 7 commits behind `orca`). The tag therefore does not identify the recipe |
| Variant | `win64-orca-shared` / `winarm64-orca-shared` → `variants/defaults-orca.sh` + `--enable-shared --disable-static`; addin `7.0` sets `GIT_BRANCH="release/7.0"` |
| FFmpeg source | `build.sh` clones `https://github.com/FFmpeg/FFmpeg.git` at **branch head** `release/7.0` at build time (no commit pin). The binaries name the result: `n7.0.3-33-g887d4b4919` = commit `887d4b49194fce2772c9bd8ea1cd4cba679ad905` (2026-08-15), **33 commits after tag `n7.0.3`**. `release/7.0` has since moved 7 commits further |
| Toolchain (from the embedded configure string) | x64: `x86_64-w64-mingw32-gcc` (the DLLs carry "GCC: (crosstool-NG 1.28.0.23_185f348) 15.2.0"); arm64: `aarch64-w64-mingw32-clang`. `--extra-version=20260918` |
| Source shipped with the release | none: the release holds only the two zips and `checksums.sha256` |

So the source can be traced to a public FFmpeg commit and public build scripts, but the scripts do not pin the FFmpeg revision, and the reproducibility of the zip from `eadd8235` + `887d4b49` was **not tested**.

### Configure flags as built

Identical on both architectures apart from toolchain and `--arch`/`--cpu`. From the string embedded in `avutil-59.dll`, which matches `FF_CONFIGURE` in `variants/defaults-orca.sh` at `eadd8235`:

```text
--enable-gpl --enable-version3 --disable-debug --disable-doc --enable-small
--disable-outdevs --disable-filters --enable-filter='*null*,afade,*fifo,*format,*resample,aeval,allrgb,allyuv,atempo,pan,*bars,color,*key,crop,draw*,eq*,framerate,*_qsv,*_vaapi,*v4l2*,hw*,scale,volume,test*'
--enable-schannel --disable-protocols --enable-protocol='file,fd,pipe,http,https,rtp,tcp,udp'
--disable-muxers --enable-muxer=rtp --disable-encoders --disable-decoders --enable-decoder='*aac*,h264*,mp3*,mjpeg,rv*'
--disable-demuxers --enable-demuxer='h264,mp3,mov,mpjpeg,rtsp,sdp' --disable-zlib --disable-avdevice
--enable-shared --disable-static --disable-w32threads --enable-pthreads
```

`--enable-nonfree` is absent. No external codec library is enabled, and the recipe's commit `dab5658c` is titled "Don't build extra libs". TLS is Windows Schannel.

## 3. License of the build

| Evidence | What it says |
|---|---|
| Configure | `--enable-gpl --enable-version3` |
| `LICENSE.txt` in both zips | GNU GPL **version 3** text (35,147 bytes, SHA-256 `8ceb4b9e…5eb65b903`); `build.sh` copies `COPYING.GPLv3` because the variant sets `LICENSE_FILE="COPYING.GPLv3"` |
| License string compiled into each shipped DLL | `libavutil`, `libavcodec`, `libavformat`, `libswscale`, `libswresample`: "**license: GPL version 3 or later**" (x64 and arm64) |
| GPL-only components built | `postproc-58.dll` is in the zip; FFmpeg's `configure` at `887d4b49` has `postproc_deps="avutil gpl"`. The filter pattern `eq*` matches `eq`, which `configure` marks `eq_filter_deps="gpl"` (whether it is compiled in was not confirmed) |

**This differs from the source build.** B3 found the Linux build reports `FFMPEG_LICENSE "LGPL version 2.1 or later"` with `CONFIG_GPL 0`. On Windows the same five libraries report GPL v3 or later. Recorded, not concluded: what this means for the application is a maintainer and licensing question.

## 4. What ships

The Windows app build copies five DLLs from the deps prefix next to the executable (root `CMakeLists.txt:1141-1147`; the same five are in `_dll_list` at `:1154-1158`): `avformat-61.dll`, `avcodec-61.dll`, `swresample-5.dll`, `swscale-8.dll`, `avutil-59.dll`. `postproc-58.dll`, `avfilter-10.dll`, `ffmpeg.exe` and `ffprobe.exe` reach the deps prefix but are not in that list. Whether any other packaging step picks them up was **not traced**.

The shipped DLLs import only each other and Windows system/UCRT DLLs (`KERNEL32`, `ADVAPI32`, `bcrypt`, `ole32`, `USER32`, `Secur32`, `WS2_32`, `api-ms-win-crt-*`); no third-party DLL is needed. The mingw-w64 runtime and winpthreads code linked statically into them was not reviewed.

No FFmpeg license or notice file is installed with the DLLs by the lines above, and `git grep -i ffmpeg` finds no FFmpeg notice under `resources/`, `doc/` or any `LICENSE*` in the tree.

## 5. Availability

The builder has two releases (`autobuild-2026-07-17-14-28` and this one). Its `util/prunetags.sh`, run after each release, keeps the latest 14 `autobuild-*` tags plus the newest one of each month for up to 24 months. A later September 2026 release, or enough newer releases, could therefore prune this one, which would break the pinned URL. The workflow's triggers are `push` and `workflow_dispatch` (no `schedule`), and `publish_release` runs only for `schedule` or `doRelease == 'true'`, so a new release needs a manual run.

## 6. Open questions

1. GPL v3 Windows build versus LGPL 2.1 source build: is that intended, and what does it mean for distribution of the Windows app? (Maintainer / licensing question; not answered here.)
2. The release ships no corresponding source, and the recipe does not pin the FFmpeg commit. The binary names `887d4b49` and the run names `eadd8235`; a written source offer or source archive is not part of what OrcaSlicer downloads.
3. No notice file for FFmpeg is installed with the Windows app (from the lines read).
4. Reproducing the zip from the recipe was not attempted.

## 7. Approval

**Not approved.** This records what the files and build metadata say. A maintainer sign-off is still needed.
