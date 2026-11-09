# FFmpeg source build license review (OrcaSlicer 2.5.0)

**Status:** Build-configuration and license-file review of the **source** build (Linux and macOS). Not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off. The prebuilt Windows zips are a separate binary item (slice C1). The printer-integration question O6 in the [use map](dependency-use-map.md#4-ranked-decision-list-re-checked-on-250) is not decided here.
**Slice:** B3 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (build files identical to upstream v2.5.0 `40ecc66f`)
**Method:** read `deps/FFMPEG/FFMPEG.cmake`; extracted the hash-verified archive; read `config.h` from the CI-image deps build (`deps/build/dep_FFMPEG-prefix/src/dep_FFMPEG`, an in-source build) and the installed libraries; read `LICENSE.md`. Linux x86_64 only.
**Reviewed:** 2026-11-09

## 1. Source and pin

| | |
|---|---|
| URL | `https://github.com/FFmpeg/FFmpeg/archive/refs/tags/n7.0.3.tar.gz` (`deps/FFMPEG/FFMPEG.cmake:70`) |
| SHA-256 (declared and verified) | `deedcabe339165214a3637df4c86a507aef0d793cf8774ff68735f4737e8ddbc` (`:71`) |
| Platforms | non-MSVC. MSVC downloads prebuilt shared zips instead (`:14-33`, slice C1) |
| Patches | none |

## 2. Configuration as built

`config.h` from the deps build records the effective result:

| Define | Value |
|---|---|
| `FFMPEG_LICENSE` | **"LGPL version 2.1 or later"** (the installed `libavutil.so` also contains "libavutil license: LGPL version 2.1 or later") |
| `CONFIG_GPL` / `CONFIG_GPLV3` | 0 / 0 |
| `CONFIG_VERSION3` / `CONFIG_LGPLV3` | 0 / 0 |
| `CONFIG_NONFREE` | 0 |
| `CONFIG_OPENSSL` | **1** |
| `CONFIG_SMALL` | 1 |

The configure line (`FFMPEG_CONFIGURATION` in `config.h`, from `deps/FFMPEG/FFMPEG.cmake:73-97`) disables all components and re-enables an allow-list:

- **Decoders:** `*aac*`, `h264*`, `mp3*`, `mjpeg`, `rv*`. **Encoders:** none.
- **Demuxers:** `h264`, `mp3`, `mov`, `mpjpeg`, `rtsp`, `sdp`. **Muxers:** `rtp`.
- **Protocols:** `file`, `fd`, `pipe`, `http`, `https`, `rtp`, `tcp`, `udp`.
- **Filters:** an allow-list of mostly format, scaling and test filters. Also `--disable-zlib`, `--disable-avdevice`, `--disable-doc`, `--disable-outdevs`.
- **Linking:** `--enable-shared` on Linux; `--enable-static --disable-shared` and no VideoToolbox/AudioToolbox on macOS (`:38-58`).

No `--enable-gpl`, `--enable-version3` or `--enable-nonfree` appears in the file. `LICENSE.md:9-11` says the GPL parts are "not used by default" and need `--enable-gpl`.

**Installed into the prefix (Linux):** `libavcodec`, `libavformat`, `libavutil`, `libavfilter`, `libswresample` and `libswscale`, each as `.so` and `.a`, plus the `ffmpeg` and `ffprobe` executables under `bin/`. The application links `avformat`, `avcodec`, `swscale` and `avutil` through pkg-config (`src/slic3r/CMakeLists.txt:1049-1056`). No reference to the `ffmpeg`/`ffprobe` executables was found in the application's CMake files.

## 3. License files

The archive has `LICENSE.md`, `COPYING.LGPLv2.1`, `COPYING.LGPLv3`, `COPYING.GPLv2` and `COPYING.GPLv3`. `LICENSE.md` says:

- "Most files in FFmpeg are under the GNU Lesser General Public License version 2.1 or later (LGPL v2.1+). … Some other files have MIT/X11/BSD-style licenses. In combination the LGPL v2.1+ applies to FFmpeg." (`:3-6`)
- On OpenSSL (`:127-129`): "The Fraunhofer FDK AAC and OpenSSL libraries are under licenses which are incompatible with the GPLv2 and v3. To the best of our knowledge, they are compatible with the LGPL."

## 4. Open questions

1. This build enables OpenSSL (1.1.1w from the deps prefix) inside an LGPL FFmpeg that is loaded by an application whose own license is a separate question ([licensing and provenance](licensing-and-provenance.md)). FFmpeg's statement in `LICENSE.md:127-129` is upstream's view, not a conclusion here.
2. LGPL obligations for shared libraries shipped in the AppImage (relinkability, source offer, notices) are not assessed. Which files the Linux image copies is in `src/dev-utils/platform/unix/build_linux_image.sh.in` and was not traced here.
3. Patent questions for H.264/AAC/MP3 decoding are outside a copyright license review and are not assessed.
4. No COPYING or LICENSE file is installed into the prefix by the build files read here.
5. macOS (static) and Windows (prebuilt, slice C1) were not examined.

## 5. Approval

**Not approved.** This records what the files say. A maintainer sign-off, and the O6 printer-integration decision, are still needed.
