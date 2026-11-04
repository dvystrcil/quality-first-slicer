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

To retain archives that fail their expected digest for isolated diagnostics, add:

```sh
--preserve-mismatches-dir /tmp/orcaslicer-v2.4.2-mismatches
```

The option is deliberately opt-in. Without it, mismatched temporary downloads are deleted as before. Retained files are named by artifact and URL-attempt number, and their paths are recorded in the JSON report. They remain failed/untrusted inputs: do not extract or execute them as part of verification. The manual GitHub Actions workflow enables this option and uploads any retained files as a separate, 30-day artifact named `orcaslicer-v2.4.2-mismatched-archives`; the JSON report remains a separate 90-day artifact.

The manifest contains 25 source archive entries. MPFR has two mirror URLs for the same expected archive digest. A failed URL is recorded and the next mirror is attempted.

## Evidence handling

- Preserve the generated JSON report; it records the UTC timestamp, manifest, expected and observed digests, byte counts, final URL, and mirror attempts.
- Review any mismatch against the exact CMake declaration at upstream commit `8500fcdccaa10b5099ac20d252af3a7c560046f1`. Do not silently update the manifest to match downloaded bytes.
- A successful match verifies only that the downloaded bytes match the declared SHA-256. It does not establish the source's authenticity, license, provenance, or safety.
- Do not extract archives as part of this hash-only step. Archive inspection should happen in a separate, isolated process after digest verification or as a deliberately isolated investigation of an untrusted mismatch.
- The manifest explicitly excludes the shallow wxWidgets tag, the Apple cross-compile PNG Git checkout, and prebuilt Windows GMP/MPFR/WebView2 binaries. Those need separate immutable-source or binary verification.
- The tool uses only the Python standard library. It does not modify the manifest and does not commit generated reports automatically.

## Latest verification result

Manual workflow run [41740959467](https://github.com/dvystrcil/quality-first-slicer/actions/runs/41740959467), completed 2026-11-03, downloaded all 25 manifest entries:

- **24 original matches:** each archive matched the SHA-256 declared in the original manifest.
- **NanoSVG redirect mismatch diagnosed:** the old URL `https://github.com/SoftFever/nanosvg/archive/863f6aa97ef62028126fa2c19bd4350394c2e15e.zip` redirected to the renamed repository `SoftFever/Orca-deps-nanosvg`. The resulting archive was 299320 bytes with SHA-256 `1e3f94a052dd2abb139993ed3496c90ed4458d6f907027bf03cbaed889fe2567`, rather than the former declared digest `8d9c1624ad6518dd6dfa31e4f8dc7da9ec243d88bae595c7a037450617fec851`.
- **Content comparison passed:** the preserved ZIP contained 16 files. Each file's size and Git blob SHA-1 matched the recursive Git tree for exact commit `863f6aa97ef62028126fa2c19bd4350394c2e15e`. The archive's top-level directory uses the renamed repository name, explaining why the whole ZIP digest changed while its file payload remained identical.
- The manifest now uses the canonical renamed repository URL and the independently observed SHA-256 for that archive.

**Disposition:** NanoSVG archive bytes now match the corrected manifest pin, and the file payload is verified against the exact Git commit. This resolves the redirect-induced mismatch. It does not establish commit authenticity (the commit is unsigned), license compliance, or archive safety. Hash verification remains byte-integrity evidence only.

## Current limitations

The manifest's expected values were transcribed from upstream CMake source. The 24 matching downloads now have independent byte-level verification evidence against those declarations. NanoSVG remains unresolved as documented above. No archive has been extracted or built as part of this verification run, and no complete SBOM, authenticity review, license review, or legal review has been performed.
