# libdatachannel provenance and license review (OrcaSlicer 2.5.0)

**Status:** Source pinning and license-file review. Not a legal determination. **Not approved** ([AGENTS.md](../AGENTS.md) §6) until the maintainer signs off. It belongs to the printer-integration question O6 in the [use map](dependency-use-map.md#4-ranked-decision-list-re-checked-on-250), which this review does not decide.
**Slice:** B2 of [#55](https://github.com/dvystrcil/quality-first-slicer/issues/55)
**OrcaSlicer revision:** fork `baseline-2.5.0` `665552c1` (build files identical to upstream v2.5.0 `40ecc66f`)
**Method:** read `deps/DataChannel/DataChannel.cmake`; resolved the tag and the submodule pins through the GitHub API; compared them with the Git clone in the CI-image deps build (`deps/build/dep_DataChannel-prefix/src/dep_DataChannel`); listed compiled objects and the `ninja -t deps` header closure; read license files. Linux x86_64 only.
**Reviewed:** 2026-11-09

## 1. Source and pin

`deps/DataChannel/DataChannel.cmake:16-21` clones `https://github.com/paullouisageneau/libdatachannel.git` at `GIT_TAG v0.24.5`, `GIT_SHALLOW ON`, `GIT_SUBMODULES_RECURSE ON`. **No commit or archive hash is declared.** Flatpak builds use a pre-cloned `SOURCE_DIR` instead (`:11-14`).

The tag resolves to one commit, and three sources agree on it:

| Anchor | Result |
|---|---|
| GitHub API `git/ref/tags/v0.24.5` | annotated tag object `61204eb4…` → commit **`443f6934d9007eb7076ab7825ba330f355fcbead`**, tagged 2026-06-12, signature: unsigned |
| Clone in the deps build | `HEAD` = `443f6934…` |
| Submodule pins | the API's `contents/deps/*?ref=v0.24.5` and the clone's `git submodule status` give the same five SHAs (below) |

A Git tag can be moved upstream. The build would then fetch different code with no hash to catch it. Pinning the commit above is the reproducibility fix; this review does not change the build.

## 2. Submodules and what the build uses

Build options (CMake cache): `NO_MEDIA=ON`, `NO_WEBSOCKET=ON`, `NO_EXAMPLES=ON`, `NO_TESTS=ON`, `USE_NICE=OFF`, `USE_GNUTLS=OFF`, `USE_MBEDTLS=OFF`, and every `USE_SYSTEM_*` OFF. TLS/DTLS comes from the prefix's static OpenSSL 1.1.1w (`-DOPENSSL_ROOT_DIR`, `OPENSSL_USE_STATIC_LIBS=ON`).

| Submodule (`.gitmodules` URL) | Pinned commit | In the build | License file (what it says) |
|---|---|---|---|
| libdatachannel itself | `443f6934` | 62 objects → `libdatachannel.a` | `LICENSE`: Mozilla Public License 2.0; source headers carry the MPL-2.0 notice (e.g. `src/peerconnection.cpp:5-6`) |
| `deps/libjuice` (`paullouisageneau/libjuice`) | `3c40a3545b6b1b62c7adee7f8f2bd58aa290afd6` (`v1.7.2`) | 21 objects → `libjuice.a` | `LICENSE`: Mozilla Public License 2.0 |
| `deps/usrsctp` (`paullouisageneau/usrsctp`) | `fec583d54493f879d2ae44a743423bf8a04371ab` (2025-06-26) | 23 objects → `libusrsctp.a` | `LICENSE.md`: BSD-3-Clause-style, "Copyright (c) 2015, Randall Stewart and Michael Tuexen" |
| `deps/plog` (`SergiusTheBest/plog`) | `94899e0b926ac1b0f4750bfbd495167b4a6ae9ef` | headers only (223 includes) | `LICENSE`: MIT, "Copyright (c) 2022 Sergey Podobry" |
| `deps/json` (`nlohmann/json`) | `55f93686c01528224f448c19128836e7df245f72` | cloned; **not included** by any compiled file | `LICENSE.MIT`: MIT, Niels Lohmann |
| `deps/libsrtp` (`cisco/libsrtp`) | `24b3bf8f19b6f5ab4cd2bcceb4f4064efca86fd5` | cloned; **not compiled** (`NO_MEDIA=ON`) | `LICENSE`: BSD-style, Cisco Systems |

The prefix holds `libdatachannel.a`, `libjuice.a` and `libusrsctp.a`; the application links `LibDataChannel::LibDataChannel` ([use map §3.2](dependency-use-map.md#32-the-six-dependency-projects-added-in-250)). Consumer: WebRTC printer camera (`S/GUI/WebRtcMediaController.cpp`).

**usrsctp comes from the libdatachannel author's fork**, not from `sctplab/usrsctp`. The GitHub API reports the fork's parent as `sctplab/usrsctp`. Comparing `sctplab:master` with `fec583d5`: diverged, 2 commits ahead and 7 behind, and the only file that differs is `CMakeLists.txt`.

## 3. Open questions

1. MPL-2.0 is file-level copyleft. What it requires when two MPL-2.0 libraries are statically linked into this application, including source availability for the MPL-covered files, is a question for a qualified reviewer. No conclusion is drawn here.
2. Notice staging: no license file from these six repositories is installed by the build files read here.
3. The usrsctp fork's two extra commits change only `CMakeLists.txt`; their content was not reviewed line by line.
4. The deps build clones `json` and `libsrtp` although it does not use them. They are not in the binary, but they are in the source the build fetches.
5. Windows and macOS were not examined.

## 4. Approval

**Not approved.** This records what the files say. A maintainer sign-off, and the O6 printer-integration decision, are still needed.
