#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import sys

import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

from eleanor_tools import __version__


# The following are helper functions for building the pybind11 extension for
# interpolation used by the background estimation. This is based on the
# pybind11 example found at: https://github.com/pybind/python_example
class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    flags = ['-std=c++17', '-std=c++14', '-std=c++11']

    for flag in flags:
        if has_flag(compiler, flag):
            return flag

    raise RuntimeError('Unsupported compiler -- at least C++11 support '
                       'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="{0}"'.format(
                self.distribution.get_version()))
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"{0}\\"'.format(
                self.distribution.get_version()))
        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
        build_ext.build_extensions(self)


ext_modules = [
    Extension(
        'eleanor_tools.fill_grid',
        ['eleanor_tools/fill_grid.cpp'],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True)
        ],
        language='c++'
    ),
]


setup(
    name='eleanor_tools',
    version=__version__,
    license='MIT',
    author='Adina D. Feinstein',
    author_email='adina.d.feinstein@gmail.com',
    packages=['eleanor_tools'],
    ext_modules=ext_modules,
    include_package_data=True,
    url='http://github.com/afeinstein20/eleanor-tools',
    description='Scripts for the eleanor package',
    long_description='Scripts for the eleanor package',
    long_description_content_type="text/markdown",
    package_data={'': ['README.md', 'LICENSE']},
    install_requires=['numpy', 'pybind11>=2.3'],
    setup_requires=['numpy', 'pybind11>=2.3'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.0',
        ],
    cmdclass={'build_ext': BuildExt},
    scripts=['scripts/eleanor-postcards',
             'scripts/eleanor-backgrounds']
    )
