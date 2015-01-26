#!/usr/bin/env python
import sys
import os
import re
from distutils.core import setup, Extension, Command

DESCRIPTION = "Python wrapper for Google's RE2 using Cython"

DISTNAME = 're2'
LICENSE = 'New BSD License'
EMAIL = "nick.conway@wyss.harvard.edu"
URL = ""
DOWNLOAD_URL = ''
CLASSIFIERS = [
    'Development Status :: 1 - Beta',
    'Environment :: Console',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Cython',
    'License :: OSI Approved :: BSD License',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

from distutils.core import setup, Extension
# from Cython.Distutils import Extension
from Cython.Build import cythonize
import os
from os.path import join as pjoin
import sys
import shutil

PACKAGE_PATH =          os.path.abspath(os.path.dirname(__file__))
MODULE_PATH =           pjoin(PACKAGE_PATH, 're2')
RE2_SRC_PATH =          pjoin(MODULE_PATH, 'src', 're2_cpp', 'usr', 'local')

def get_long_description():
    with open(pjoin(PACKAGE_PATH, "README.rst")) as readme_f:
        readme = readme_f.read()
    return readme

def get_authors():
    author_re = re.compile(r'^\s*(.*?)\s+<.*?\@.*?>', re.M)
    with open(pjoin(PACKAGE_PATH, "AUTHORS")) as authors_f:
        authors = [match.group(1) for match in author_re.finditer(authors_f.read())]
    return ', '.join(authors)


class TestCommand(Command):
    description = 'Run packaged tests'
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from tests import re2_test
        re2_test.testall()


cmdclass = {'test': TestCommand}

# # Locate the re2 module
# _re2_prefixes = [
#     ''
#     '/usr',
#     '/usr/local',
#     '/opt/',
# ]

# for re2_prefix in _re2_prefixes:
#     if os.path.exists(os.path.join(re2_prefix, "include", "re2")):
#         break
# else:
#     re2_prefix = ""


re2_ext = Extension( "re2._re2",
        sources=['re2/_re2.pyx'],
        language="c++",
        include_dirs=[pjoin(RE2_SRC_PATH, "include"), pjoin('re2', 'src')],
        libraries=["re2"],
        library_dirs=[pjoin(RE2_SRC_PATH, "lib")],
        runtime_library_dirs=[pjoin(RE2_SRC_PATH, "lib")],
        extra_compile_args=['-Wno-unused-function']
    )

# re2_ext = Extension( "re2.tester",
#         sources=['re2/tester.pyx'],
#         language="c++",
#         include_dirs=[pjoin(RE2_SRC_PATH, "include"), pjoin('re2', 'src')],
#         libraries=["re2"],
#         library_dirs=[pjoin(RE2_SRC_PATH, "lib")],
#         runtime_library_dirs=[pjoin(RE2_SRC_PATH, "lib")],
#     )

is_py_3 = int(sys.version_info[0] > 2)
cython_ext_list = cythonize(re2_ext, compile_time_env={'IS_PY_THREE': is_py_3})

setup(
    name="re2",
    maintainer=get_authors(),
    packages=['re2'],
    ext_modules=cython_ext_list,
    version="0.2.20",
    description=DESCRIPTION,
    long_description=get_long_description(),
    license=LICENSE,
    maintainer_email = EMAIL,
    url = "http://github.com/Wyss/pyre2/",
    classifiers = CLASSIFIERS
)

