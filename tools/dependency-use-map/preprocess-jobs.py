#!/usr/bin/env python3
"""Turn Release compile_commands.json entries into preprocessor-only `-M` runs.

The precompiled header (both -include-pch and the forced cmake_pch.hxx include)
is removed so each .d file lists only what that translation unit includes itself;
with PCH, every TU of a target appears to include everything in pchheader.hpp.
Defines, include paths and platform flags are left exactly as CMake generated
them, so conditional compilation is resolved the way the real build resolves it.
"""
import hashlib, json, shlex, sys


def depscan_args(command):
    """Return (object path, argv for a -M run) or None for non-Release entries."""
    a = shlex.split(command)
    if '-o' not in a:
        return None
    obj = a[a.index('-o') + 1]
    if '/Release/' not in obj:      # Ninja Multi-Config lists every config
        return None
    out, i = [], 0
    while i < len(a):
        t = a[i]
        if t == '-Winvalid-pch':
            i += 1; continue
        if t == '-Xclang' and i + 3 < len(a) and a[i + 1] in ('-include-pch', '-include') and \
                'cmake_pch' in a[i + 3]:
            i += 4; continue
        if t == '-o':
            i += 2; continue
        if t == '-c':
            i += 1; continue
        out.append(t); i += 1
    return obj, out


def jobs_for(entries, depdir):
    jobs = []
    for e in entries:
        r = depscan_args(e['command'])
        if not r:
            continue
        obj, argv = r
        dep = depdir + '/' + hashlib.md5(obj.encode()).hexdigest() + '.d'
        argv = argv + ['-M', '-MF', dep, '-MT', e['file']]
        jobs.append('cd %s && %s >/dev/null 2>>%s/errors.log || echo %s >> %s/failed.log' % (
            shlex.quote(e['directory']), shlex.join(argv), depdir, shlex.quote(e['file']), depdir))
    return jobs


if __name__ == '__main__':
    build, depdir = sys.argv[1], sys.argv[2]
    sys.stdout.write('\n'.join(jobs_for(json.load(open(build + '/compile_commands.json')), depdir)) + '\n')
