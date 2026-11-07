# mDNS / DNS-SD provenance and license review

**Status:** Targeted source/provenance review; upstream-to-vendor source deltas and release-notice staging are documented, but artifact distribution and a full technical validation remain open  
**Reviewed upstream revision:** OrcaSlicer v2.4.2 commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`  
**Component:** `deps_src/mdns`  
**Scope:** Four vendored source files, component CMake integration, application call site, import history, and upstream source comparisons  
**Method:** GitHub source/blob comparison and commit-history inspection. No local build, binary/package inspection, network-behavior testing, or legal determination was performed.

## 1. Findings

- The component is a composite of two separately attributed sources:
  - `mdns.h` and `mdns.c`: Mattias Jansson's mDNS/DNS-SD library, described in its source header and the component notice as public domain.
  - `cxmdns.h` and `cxmdns.cpp`: a C++ discovery wrapper copied from CrealityPrint v7.1.1, identified in the notice as GNU AGPL-3.0.
- The four vendored files are byte-identical to the corresponding files in `CrealityOfficial/CrealityPrint` tag `v7.1.1`. This establishes the immediate source snapshot, not the full upstream origin of the modified mDNS library files.
- The upstream mDNS repository revision used for a targeted comparison is commit `a569c4759bd47e0f2a7bfc4d4c19620445782806`. The vendored header and implementation are not byte-identical to that revision. The local snapshot is a CrealityPrint-derived fork/split, with several source changes described below.
- OrcaSlicer first imported the files in commit `d6cffbba264d557f5f0f551e951167b4ac9c753c` (2026-05-19), initially under `src/slic3r/Utils/mdns/`. Commit `d643701529ac79233a508a4785e6887f8ebfc823` moved the files into `deps_src/mdns/` and created a static-library target.
- The wrapper is actively used by `CrealityHostDiscovery.cpp`, which calls `cxnet::syncDiscoveryService({"Creality", "creality"})`. The GUI target links `mdns`; `deps_src/CMakeLists.txt` unconditionally adds the component.
- `NOTICE.md` provides source and license attribution for both parts. The full OrcaSlicer root `LICENSE.txt` is AGPL-3.0, but the component subtree does not include a separate copy of the upstream mDNS `LICENSE` file. The mDNS header itself carries the public-domain statement.
- No conclusion is made here about the legal effect of the mixed-source component, the wrapper's relationship to the larger application, or distribution compliance.

## 2. Pinned provenance and blob comparison

### 2.1 Immediate CrealityPrint source snapshot

The following Git blob IDs match exactly between OrcaSlicer v2.4.2 and CrealityPrint v7.1.1:

| File | OrcaSlicer blob | CrealityPrint v7.1.1 blob | Result |
|---|---|---|---|
| `mdns.h` | `c32fd7f5057a85ce23e0a4994e8ee8c6a6839853` | `c32fd7f5057a85ce23e0a4994e8ee8c6a6839853` | Exact |
| `mdns.c` | `089b495176e64f421ea75ea0a96ae8cca2f87338` | `089b495176e64f421ea75ea0a96ae8cca2f87338` | Exact |
| `cxmdns.h` | `e0f9c1c3dcd104b0cfe8fe37af67d156377e3cb0` | `e0f9c1c3dcd104b0cfe8fe37af67d156377e3cb0` | Exact |
| `cxmdns.cpp` | `f505eaa0b27000ccee168d0192adf5132556cffb` | `f505eaa0b27000ccee168d0192adf5132556cffb` | Exact |

The source snapshot is therefore reproducible at the CrealityPrint tag. The OrcaSlicer notice identifies the wrapper's origin as `src/slic3r/GUI/print_manage/utils/cxmdns.{h,cpp}` and identifies the mDNS files as taken from the same CrealityPrint v7.1.1 snapshot.

### 2.2 Comparison with mjansson/mdns

The mDNS project source was compared with upstream commit `a569c4759bd47e0f2a7bfc4d4c19620445782806`:

| File | CrealityPrint-derived blob | Upstream blob | Result |
|---|---|---|---|
| `mdns.h` | `c32fd7f5057a85ce23e0a4994e8ee8c6a6839853` | `d0794bfaa6210cebc1a07a7e08e9050ae4295362` | Modified |
| `mdns.c` | `089b495176e64f421ea75ea0a96ae8cca2f87338` | `f1903aaca0d6c7918e961695c8f352110ad4d6fd` | Modified |

The reviewed `mdns.h` differences include:

- Added `mdns_ip_mac_str` and `discoveryServiceC()` declarations.
- Added external declarations for helper functions used by the split implementation and C++ wrapper, including socket discovery, address formatting, and query callback helpers.
- Modified socket setup behavior and related declarations compared with the upstream header-only implementation.
- The local file has 1,642 lines versus 1,622 lines upstream at the pinned comparison revision.

The reviewed `mdns.c` retains the upstream 1,264-line structure but has a small set of differences, including removal of `static` from functions that need external linkage, changing the sample entry point from `main` to `__main`, a type adjustment in query handling, a removed include, and minor diagnostic-string/formatting changes. These changes are present in the CrealityPrint snapshot; their individual authorship and rationale are not established by the Orca import.

The local `mdns.h` / `mdns.c` split and the added wrapper should not be represented as a pristine copy of a single upstream mjansson/mdns release. The upstream comparison commit is a pinned comparison point, not proof that it is the precise base revision used by CrealityPrint.

## 3. License and notice observations

### mDNS library

- The header identifies Mattias Jansson and 2017 and explicitly states that the library is public domain and may be redistributed or modified without restrictions.
- The upstream repository at the comparison commit also contains a separate `LICENSE` file with a public-domain dedication. That file is not present in the OrcaSlicer `deps_src/mdns` subtree.
- The vendored `NOTICE.md` records the public-domain status and links to the upstream project. The embedded header statement and notice are the evidence present in the component subtree.

### CrealityPrint wrapper

- `cxmdns.h` and `cxmdns.cpp` are exact copies of the CrealityPrint v7.1.1 files.
- The OrcaSlicer `NOTICE.md` identifies these files as GNU AGPL-3.0 and attributes their source to CrealityPrint v7.1.1.
- The wrapper files do not contain individual copyright/license headers. The Orca import commit message and notice record the source relationship; the top-level OrcaSlicer `LICENSE.txt` contains the GNU AGPL version 3 license text.
- The CrealityPrint source snapshot is an immediate provenance reference, not an independent legal opinion about authorship or licensing.

## 4. Active build and application integration

- `deps_src/CMakeLists.txt` adds the `mdns` subdirectory.
- `deps_src/mdns/CMakeLists.txt` builds `mdns.h`, `mdns.c`, `cxmdns.h`, and `cxmdns.cpp` into a static `mdns` target and exposes the component directory as a public include directory.
- On MSVC, the target links `Iphlpapi` and `Ws2_32`, matching the source's use of `GetAdaptersAddresses` and Winsock2.
- `src/slic3r/CMakeLists.txt` links `mdns` into `libslic3r_gui`.
- `src/slic3r/Utils/CrealityHostDiscovery.cpp` includes `cxmdns.h` and calls `cxnet::syncDiscoveryService` with Creality service-name prefixes. The result is deduplicated by IP and optionally enriched by an HTTP `/info` request.
- The import commit introduced the vendored sources before callers; the following application integration commit added the K-series discovery flow. A later move commit made the component a dedicated static library.
- The move commit reports a clean Linux build, but this review did not independently reproduce that build or validate Windows/macOS behavior.

## 5. Remaining evidence and limitations

1. Determine whether `NOTICE.md`, the AGPL license text, and the mDNS public-domain attribution are included in each actual Windows, macOS, Linux/AppImage, and source-release notice bundle. No release artifact was inspected.
2. Identify the precise mjansson/mdns revision or archive used by CrealityPrint v7.1.1 and map the local mDNS changes to upstream commits or vendor patches. The comparison against commit `a569c4759bd47e0f2a7bfc4d4c19620445782806` is informative but does not prove the exact base revision.
3. Trace copyright/authorship for the CrealityPrint wrapper and for the local mDNS modifications beyond the immediate source snapshot and Orca import history.
4. Validate the mDNS discovery behavior and build/link behavior on each supported platform if this component remains in the product.
5. Review the component's mixed public-domain / AGPL provenance with qualified counsel as appropriate; this document makes no legal conclusion.

## 6. Pinned references

- [OrcaSlicer mDNS import commit](https://github.com/OrcaSlicer/OrcaSlicer/commit/d6cffbba264d557f5f0f551e951167b4ac9c753c)
- [OrcaSlicer application integration commit](https://github.com/OrcaSlicer/OrcaSlicer/commit/598df9ff0b53ec1dba243350d448179e058a8fa5)
- [OrcaSlicer move into deps_src commit](https://github.com/OrcaSlicer/OrcaSlicer/commit/d643701529ac79233a508a4785e6887f8ebfc823)
- [CrealityPrint v7.1.1 mDNS header](https://github.com/CrealityOfficial/CrealityPrint/blob/v7.1.1/src/slic3r/GUI/print_manage/utils/mdns.h)
- [CrealityPrint v7.1.1 mDNS implementation](https://github.com/CrealityOfficial/CrealityPrint/blob/v7.1.1/src/slic3r/GUI/print_manage/utils/mdns.c)
- [CrealityPrint v7.1.1 C++ wrapper](https://github.com/CrealityOfficial/CrealityPrint/tree/v7.1.1/src/slic3r/GUI/print_manage/utils)
- [mjasson/mdns upstream comparison commit](https://github.com/mjansson/mdns/commit/a569c4759bd47e0f2a7bfc4d4c19620445782806)
- [mjasson/mdns upstream license at comparison commit](https://github.com/mjansson/mdns/blob/a569c4759bd47e0f2a7bfc4d4c19620445782806/LICENSE)

**Scope limitation:** Documentation-only review. No source, build, dependency, or license file was changed; no local build, binary/package inspection, SBOM generation, network-behavior test, or legal review was performed.
