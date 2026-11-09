#!/usr/bin/env bash
# Reproduce the dependency/use-map scan (quality-first-slicer#47 AC1/AC2).
#
# Usage: run.sh <OrcaSlicer checkout> <output dir> <runner image>
#
# <runner image> is the image the fork's Linux CI job runs in (the self-hosted
# `orcaslicer-build-runner`); use the same image that built deps/build.
#
# Runs entirely inside the OrcaSlicer CI runner image, against an existing
# dependency prefix (deps/build/OrcaSlicer_dep) produced by the same image.
# Nothing is compiled: CMake configures (graphviz + File API + compile
# commands) and clang runs every Release TU with -M only. The checkout is
# mounted read-only at the CI workspace path so absolute paths in the
# installed CMake package configs resolve exactly as in CI.
set -euo pipefail
SRC=$(realpath "$1"); OUT=$(realpath "$2")
IMAGE=${3:?runner image required}
WS=/__w/OrcaSlicer/OrcaSlicer
HERE=$(dirname "$(realpath "$0")")
JOBS=${JOBS:-$(( $(nproc) - 2 ))}

test -d "$SRC/deps/build/OrcaSlicer_dep/usr/local" || { echo "no dependency prefix in $SRC/deps/build" >&2; exit 1; }
mkdir -p "$OUT/build/.cmake/api/v1/query" "$OUT/graph" "$OUT/tools"
touch "$OUT/build/.cmake/api/v1/query/codemodel-v2" "$OUT/build/.cmake/api/v1/query/cache-v2"
cp "$HERE/preprocess-jobs.py" "$OUT/tools/"
rm -rf "$OUT/depsnp"; mkdir -p "$OUT/depsnp"

docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$SRC:$WS:ro" -v "$OUT:/out" -w "$WS" "$IMAGE" bash -euo pipefail -c "
    cmake --version | head -1
    clang++ --version | head -1
    # Same configure as build_linux.sh -istrlL on the CI runner (clang, PCH, tools, tests).
    cmake -S . -B /out/build -G 'Ninja Multi-Config' \
      -DCMAKE_C_COMPILER=/usr/bin/clang -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
      -DSLIC3R_PCH=ON -DORCA_TOOLS=ON -DBUILD_TESTS=ON \
      -DCMAKE_PREFIX_PATH=$WS/deps/build/OrcaSlicer_dep/usr/local \
      -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
      --graphviz=/out/graph/orca.dot > /out/configure.log
    # Headers generated at build time, not configure time, must exist before -M.
    # 2.5.0 adds git_commit_hash.h (included by src/slic3r/GUI/BuildCommit.cpp),
    # written by a custom target that only runs cmake -P; nothing is compiled.
    # (Target list goes to a file: grep -q in a pipe SIGPIPEs ninja under pipefail.)
    ninja -C /out/build -f build-Release.ninja -t targets all > /out/build/targets.txt
    for t in git_commit_hash_header; do
      if grep -q \"^\$t: \" /out/build/targets.txt; then
        cmake --build /out/build --config Release --target \$t >> /out/configure.log
      fi
    done
    python3 /out/tools/preprocess-jobs.py /out/build /out/depsnp > /out/preprocess-jobs.sh
    echo \"TUs: \$(wc -l < /out/preprocess-jobs.sh)\"
    tr '\n' '\0' < /out/preprocess-jobs.sh | xargs -0 -P $JOBS -n 1 bash -c
    echo \"dep files: \$(ls /out/depsnp/*.d | wc -l)\"
    if [ -s /out/depsnp/failed.log ]; then echo 'preprocessing failures:'; cat /out/depsnp/failed.log; exit 1; fi
    echo SCAN-COMPLETE"
python3 "$HERE/analyze.py" "$OUT" "$WS" "$SRC" > "$OUT/dependency-use-map.json"
echo "wrote $OUT/dependency-use-map.json"
