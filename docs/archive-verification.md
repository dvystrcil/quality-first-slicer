# Source archive verification procedure

The source archive manifest records the URLs and SHA-256 values declared by OrcaSlicer v2.4.2 dependency CMake. The verification utility downloads the bytes and independently recalculates SHA-256; it does not extract or execute downloaded content.

## Run

From the repository root, with Python 3.9+:

```sh
python3 -m unittest discover -s tests -v
python3 -m json.tool audit/orcaslicer-v2.4.2-source-archives.json >/dev/null
python3 tools/verify-source-archives.py \
  --cache-dir /tmp/orcaslicer-v2.4.2-source-archives \
  --report /tmp/orcaslicer-v2.4.2-archive-verification.json
```

To verify a subset:

```sh
python3 tools/verify-source-archives.py --artifact boost --artifact openvdb
```

The manifest contains 25 source archive entries. MPFR has two mirror URLs for the same expected archive digest. A failed URL is recorded and the next mirror is attempted.

## Evidence handling

- Preserve the generated JSON report; it records the UTC timestamp, manifest, expected and observed digests, byte counts, final URL, and mirror attempts.
- Review any mismatch against the exact CMake declaration at upstream commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`. Do not silently update the manifest to match downloaded bytes.
- A successful match verifies only that the downloaded bytes match the declared SHA-256. It does not establish the source's authenticity, license, provenance, or safety.
- Do not extract archives as part of this hash-only step. Archive inspection should happen in a separate, isolated process after digest verification.
- The manifest explicitly excludes the shallow wxWidgets tag, the Apple cross-compile PNG Git checkout, and prebuilt Windows GMP/MPFR/WebView2 binaries. Those need separate immutable-source or binary verification.
- The tool uses only the Python standard library. It does not modify the manifest and does not commit generated reports automatically.

## Current limitations

This repository's manifest was transcribed from upstream CMake source. The expected values are therefore still declarations until the downloaded bytes have been independently checked. No archive verification has been run in this review environment.
