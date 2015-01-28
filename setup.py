#!/usr/bin/env python
import sys
import os
import re
from distutils.core import setup, Extension

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
from distutils.command import install_lib, sdist, build_ext
# from Cython.Distutils import Extension
from Cython.Build import cythonize
import os
from os.path import join as pjoin
import sys
import shutil

class CustomInstallLib(install_lib.install_lib):
    def run(self):
        install_lib.install_lib.run.run(self)
        postinstall()

class CustomBuildExt(build_ext.build_ext):
    def run(self):
        build_ext.build_ext.run(self)
        postinstall()

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

# see:
# http://stackoverflow.com/questions/19123623/python-runtime-library-dirs-doesnt-work-on-mac
RE2_LIB_PATH = pjoin(RE2_SRC_PATH, "lib")
def postinstall():
    print("checking linking")
    import platform
    import subprocess
    if platform.system() == 'Darwin':
        wrong_lib = 'obj/so/libre2.so.0'
        right_lib = pjoin(RE2_LIB_PATH, 'libre2.so.0')
        target_so = pjoin(MODULE_PATH, "_re2.so")
        rename = "install_name_tool -change %s %s %s" % (wrong_lib, right_lib, target_so)
        p_rename = subprocess.Popen([rename], shell=True)
        p_rename.wait()

re2_ext = Extension( "re2._re2",
        sources=['re2/_re2.pyx'],
        language="c++",
        include_dirs=[pjoin(RE2_SRC_PATH, "include"), pjoin('re2', 'src')],
        libraries=["re2"],
        library_dirs=[RE2_LIB_PATH],
        runtime_library_dirs=[RE2_LIB_PATH],
        extra_compile_args=['-Wno-unused-function'],
    )

# re2_ext = Extension( "re2.tester",
#         sources=['re2/tester.pyx'],
#         language="c++",
#         include_dirs=[pjoin(RE2_SRC_PATH, "include"), pjoin('re2', 'src')],
#         libraries=["re2"],
#         library_dirs=[pjoin(RE2_SRC_PATH, "lib")],
#         runtime_library_dirs=[pjoin(RE2_SRC_PATH, "lib")],
#         extra_compile_args=['-Wno-unused-function']
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
    classifiers = CLASSIFIERS,
    cmdclass={'install_lib': CustomInstallLib, 
    'build_ext': CustomBuildExt}
)

