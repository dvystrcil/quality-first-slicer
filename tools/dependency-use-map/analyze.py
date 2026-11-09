#!/usr/bin/env python3
"""Summarise a dependency/use-map scan produced by run.sh.

Inputs (all under OUT):
  build/.cmake/api/v1/reply  CMake File API codemodel (targets, sources, links)
  graph/orca.dot             cmake --graphviz target graph (incl. INTERFACE libs)
  depsnp/*.d                 clang -M output per Release TU, PCH force-include removed
Output: JSON on stdout. Paths are relative to the OrcaSlicer checkout.
"""
import collections, glob, json, os, re, sys

OUT = None
SRC = '/__w/OrcaSlicer/OrcaSlicer/'          # source root as seen inside the container
PREFIX = SRC + 'deps/build/OrcaSlicer_dep/usr/local/include/'
SRC_TREE = None                               # host checkout, for vendored file counts
ROOT = 'OrcaSlicer'


def codemodel():
    r = OUT + '/build/.cmake/api/v1/reply'
    idx = json.load(open(sorted(glob.glob(r + '/index-*.json'))[-1]))
    cm = next(o for o in idx['objects'] if o['kind'] == 'codemodel')
    c = json.load(open(r + '/' + cm['jsonFile']))
    cfg = next(x for x in c['configurations'] if x['name'] == 'Release')
    t = {}
    for ref in cfg['targets']:
        d = json.load(open(r + '/' + ref['jsonFile']))
        t[d['name']] = d
    return t


def graph():
    txt = open(OUT + '/graph/orca.dot').read()
    nodes = {m[0]: m[1].split('\\n')[0] for m in re.findall(r'"(node\d+)" \[ label = "([^"]+)"', txt)}
    e = collections.defaultdict(set)
    for a, b in re.findall(r'"(node\d+)" -> "(node\d+)"', txt):
        e[nodes[a]].add(nodes[b])
    return set(nodes.values()), e


def closure(e, root):
    seen, st = set(), [root]
    while st:
        for y in e[st.pop()]:
            if y not in seen:
                seen.add(y); st.append(y)
    return seen


def component(h):
    h = os.path.normpath(h)
    if h.startswith(SRC + 'deps_src/'):
        return 'deps_src/' + h[len(SRC + 'deps_src/'):].split('/')[0]
    p = os.path.normpath(PREFIX)
    if h.startswith(p + '/'):
        r = h[len(p) + 1:].split('/')
        n = r[0] if len(r) > 1 else re.sub(r'(_.*|\..*)$', '', r[0])
        n = {'jconfig': 'jpeg', 'jerror': 'jpeg', 'jmorecfg': 'jpeg', 'jpeglib': 'jpeg',
             'pngconf': 'png', 'pnglibconf': 'png', 'libqhull_r': 'qhull', 'libqhullcpp': 'qhull',
             'gmpxx': 'gmp', 'oneapi': 'tbb'}.get(n, n)
        return 'prefix/' + n
    # deps/python3 (2.5.0+) installs CPython under <prefix>/libpython, not <prefix>/include.
    if h.startswith(os.path.normpath(PREFIX + '../libpython') + '/'):
        return 'prefix/python3'
    if h.startswith('/usr/include/'):
        r = h[len('/usr/include/'):].split('/')
        if r[0] == 'x86_64-linux-gnu':
            r = r[1:]
        if r[0] in ('c++', 'bits', 'sys', 'asm', 'asm-generic', 'linux', 'gnu') or len(r) == 1 and r[0].endswith('.h') and r[0][:-2] in LIBC:
            return None
        n = r[0] if len(r) > 1 else re.sub(r'\..*$', '', r[0])
        return 'system/' + n
    if h.startswith(SRC + 'src/'):
        r = h[len(SRC + 'src/'):].split('/')
        return 'src/' + r[0] if r[0] in ('glad', 'libvgcode') else None
    return None


LIBC = set('''alloca arpa assert ctype dirent dlfcn elf endian errno fcntl features features-time64 fenv glob ifaddrs
inttypes libintl limits link locale math memory net netdb netinet poll pthread pwd rpc sched setjmp signal stdc-predef
stdint stdio stdlib string strings termios time unistd utime wchar wctype'''.split())


def main():
    global OUT, SRC, PREFIX, SRC_TREE
    OUT = sys.argv[1]
    SRC = sys.argv[2].rstrip('/') + '/'
    PREFIX = SRC + 'deps/build/OrcaSlicer_dep/usr/local/include/'
    SRC_TREE = sys.argv[3] if len(sys.argv) > 3 else None
    tg = codemodel()
    nodes, e = graph()
    src2t = {s['path']: n for n, d in tg.items() for s in d.get('sources', [])}
    linked = closure(e, ROOT)
    use = collections.defaultdict(lambda: collections.defaultdict(set))
    ntu = 0
    for f in glob.glob(OUT + '/depsnp/*.d'):
        tu, _, rest = open(f).read().replace('\\\n', ' ').partition(': ')
        tu = tu.strip().replace(SRC, ''); ntu += 1
        for h in rest.split():
            c = component(h)
            if c and not tu.startswith(c + '/') and not tu.startswith(c + '.'):
                use[c][tu].add(os.path.normpath(h).replace(SRC, '').replace(PREFIX.replace(SRC, ''), 'PREFIX/'))
    comps = {}
    for c in sorted(use):
        tus = use[c]
        by_t = collections.Counter(src2t.get(t, '?') for t in tus)
        hdrs = sorted({h for hs in tus.values() for h in hs})
        comps[c] = {'consumer_tus': len(tus),
                    'consumer_tus_in_app': sum(v for k, v in by_t.items() if k in linked or k == ROOT),
                    'by_target': dict(sorted(by_t.items())),
                    'consumer_files': sorted(tus) if len(tus) <= 40 else sorted(tus)[:40] + ['... (%d more)' % (len(tus) - 40)],
                    'headers_used': len(hdrs),
                    'headers': hdrs if len(hdrs) <= 60 else hdrs[:60] + ['... (%d more)' % (len(hdrs) - 60)]}
        if SRC_TREE and c.startswith('deps_src/'):
            n = sum(1 for _ in glob.glob(SRC_TREE + '/' + c + '/**/*.h*', recursive=True))
            comps[c]['headers_available'] = n
    targets = {}
    for n, d in tg.items():
        if d['type'] == 'UTILITY':
            continue
        targets[n] = {'type': d['type'], 'source_dir': d['paths']['source'],
                      'sources': sum(1 for s in d.get('sources', []) if not s.get('isGenerated')),
                      'direct_target_deps': sorted(tg_n for tg_n in (x['id'].split('::')[0] for x in d.get('dependencies', []))),
                      'in_app_link_closure': n in linked or n == ROOT}
    print(json.dumps({'root_target': ROOT, 'release_tus_scanned': ntu,
                      'app_link_closure': sorted(linked),
                      'graph_nodes_not_in_app_closure': sorted(nodes - linked - {ROOT}),
                      'targets': targets, 'components': comps}, indent=1))


if __name__ == '__main__':
    main()
