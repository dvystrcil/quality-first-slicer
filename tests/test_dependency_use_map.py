"""Tests for tools/dependency-use-map (quality-first-slicer#47)."""
import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest

TOOLS = os.path.join(os.path.dirname(__file__), '..', 'tools', 'dependency-use-map')
WS = '/__w/OrcaSlicer/OrcaSlicer/'


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(TOOLS, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pre = load('preprocess_jobs', 'preprocess-jobs.py')
ana = load('analyze', 'analyze.py')


class PreprocessJobsTest(unittest.TestCase):
    CMD = ('/usr/bin/clang++ -DSLIC3R_GUI -I/x -Winvalid-pch '
           '-Xclang -include-pch -Xclang /b/Release/cmake_pch.hxx.pch '
           '-Xclang -include -Xclang /b/Release/cmake_pch.hxx '
           '-o src/CMakeFiles/t.dir/Release/a.cpp.o -c /s/a.cpp')

    def test_release_entry_drops_pch_output_and_compile_flags(self):
        obj, argv = pre.depscan_args(self.CMD)
        self.assertEqual(obj, 'src/CMakeFiles/t.dir/Release/a.cpp.o')
        joined = ' '.join(argv)
        for gone in ('cmake_pch', '-Winvalid-pch', ' -o ', ' -c '):
            self.assertNotIn(gone, ' ' + joined + ' ')
        # Defines and include paths must survive: they decide conditional compilation.
        self.assertIn('-DSLIC3R_GUI', argv)
        self.assertIn('-I/x', argv)
        self.assertEqual(argv[-1], '/s/a.cpp')

    def test_non_release_configs_are_skipped(self):
        self.assertIsNone(pre.depscan_args(self.CMD.replace('/Release/', '/Debug/')))

    def test_job_writes_depfile_and_records_failures(self):
        jobs = pre.jobs_for([{'directory': '/b', 'file': '/s/a.cpp', 'command': self.CMD}], '/out/d')
        self.assertEqual(len(jobs), 1)
        self.assertIn(' -M -MF /out/d/', jobs[0])
        self.assertIn('/out/d/failed.log', jobs[0])


class ComponentTest(unittest.TestCase):
    def setUp(self):
        ana.SRC = WS
        ana.PREFIX = WS + 'deps/build/OrcaSlicer_dep/usr/local/include/'

    def test_classification(self):
        p = ana.PREFIX
        cases = {
            WS + 'deps_src/nlohmann/json.hpp': 'deps_src/nlohmann',
            WS + 'deps_src/admesh/../mdns/cxmdns.h': 'deps_src/mdns',   # the admesh/.. include path
            p + 'boost/optional.hpp': 'prefix/boost',
            p + 'jpeglib.h': 'prefix/jpeg',
            p + 'oneapi/tbb.h': 'prefix/tbb',
            '/usr/include/expat.h': 'system/expat',
            '/usr/include/x86_64-linux-gnu/sys/types.h': None,
            '/usr/include/stdio.h': None,
            WS + 'src/glad/include/glad/gl.h': 'src/glad',
            WS + 'src/libslic3r/Model.hpp': None,
        }
        for path, want in cases.items():
            self.assertEqual(ana.component(path), want, path)


class AnalyzeCompositionTest(unittest.TestCase):
    """Run analyze.main() on a miniature scan: the AC2 case is a header-only
    library with no link edge that is still reported as used."""

    def build_fixture(self, d):
        reply = os.path.join(d, 'build/.cmake/api/v1/reply')
        os.makedirs(reply)
        os.makedirs(os.path.join(d, 'graph'))
        os.makedirs(os.path.join(d, 'depsnp'))

        def target(name, typ, srcs, deps=()):
            f = 'target-%s.json' % name
            json.dump({'id': name + '::@1', 'name': name, 'type': typ, 'paths': {'source': 'src'},
                       'sources': [{'path': s} for s in srcs],
                       'dependencies': [{'id': x + '::@1'} for x in deps]},
                      open(os.path.join(reply, f), 'w'))
            return {'jsonFile': f}
        targets = [target('OrcaSlicer', 'EXECUTABLE', ['src/main.cpp'], ['libslic3r']),
                   target('libslic3r', 'STATIC_LIBRARY', ['src/libslic3r/a.cpp']),
                   target('expat', 'STATIC_LIBRARY', ['deps_src/expat/xmlparse.c'])]
        json.dump({'configurations': [{'name': 'Release', 'targets': targets}]},
                  open(os.path.join(reply, 'codemodel-v2-x.json'), 'w'))
        json.dump({'objects': [{'kind': 'codemodel', 'jsonFile': 'codemodel-v2-x.json'}]},
                  open(os.path.join(reply, 'index-1.json'), 'w'))
        open(os.path.join(d, 'graph/orca.dot'), 'w').write(
            '"node0" [ label = "OrcaSlicer" ];\n"node1" [ label = "libslic3r" ];\n'
            '"node2" [ label = "nlohmann_json" ];\n"node3" [ label = "expat" ];\n'
            '"node0" -> "node1"\n')
        open(os.path.join(d, 'depsnp/1.d'), 'w').write(
            WS + 'src/libslic3r/a.cpp: ' + WS + 'src/libslic3r/a.cpp \\\n  '
            + WS + 'deps_src/admesh/../nlohmann/json.hpp /usr/include/stdio.h\n')
        open(os.path.join(d, 'depsnp/2.d'), 'w').write(
            WS + 'deps_src/expat/xmlparse.c: ' + WS + 'deps_src/expat/expat.h\n')

    def test_header_only_use_without_link_edge(self):
        with tempfile.TemporaryDirectory() as d:
            self.build_fixture(d)
            argv, sys.argv = sys.argv, ['analyze.py', d, WS]
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    ana.main()
            finally:
                sys.argv = argv
            out = json.loads(buf.getvalue())
        self.assertEqual(out['release_tus_scanned'], 2)
        self.assertEqual(out['app_link_closure'], ['libslic3r'])
        self.assertIn('nlohmann_json', out['graph_nodes_not_in_app_closure'])
        nl = out['components']['deps_src/nlohmann']
        self.assertEqual(nl['consumer_tus_in_app'], 1)
        self.assertEqual(nl['consumer_files'], ['src/libslic3r/a.cpp'])
        # A component's own TUs are not consumers: vendored expat has none.
        self.assertNotIn('deps_src/expat', out['components'])
        self.assertFalse(out['targets']['expat']['in_app_link_closure'])


if __name__ == '__main__':
    unittest.main()
