import os.path
from os.path import join as pjoin
import subprocess
from os import rename, makedirs
import shutil

PACKAGE_PATH =          os.path.abspath(os.path.dirname(__file__))
MODULE_PATH =           pjoin(PACKAGE_PATH, 're2')

RE2_SRC_PATH =          pjoin(PACKAGE_PATH, 're2_cpp')

RE2_INSTALL_PATH = pjoin(MODULE_PATH, 'src', 're2_cpp')

INSTALL_H_FILES = [ "filtered_re2.h",
                    "re2.h",
                    "set.h",
                    "stringpiece.h",
                    "variadic_function.h"]
INSTALL_LIB_FILES = ["libre2.a"]

def re2Clean():
    re2clean = subprocess.Popen(['make clean'], shell=True, 
                               cwd=RE2_SRC_PATH)
    re2clean.wait()
    if os.path.exists(RE2_INSTALL_PATH):
        shutil.rmtree(RE2_INSTALL_PATH)


def re2Build():
    e_cmd = 'make -j4 obj/libre2.a;'    # only build the static libs
    re2build = subprocess.Popen([e_cmd],
                                shell=True, 
                                cwd=RE2_SRC_PATH)
    re2build.wait()
    # copy files to install
    install_include_path = pjoin(RE2_INSTALL_PATH, "include", "re2")
    if not os.path.exists(install_include_path):
        makedirs(install_include_path)
    for f in INSTALL_H_FILES:
        shutil.copyfile(pjoin(RE2_SRC_PATH, "re2", f), 
                        pjoin(install_include_path, f))

    install_lib_path = pjoin(RE2_INSTALL_PATH, "lib")
    if not os.path.exists(install_lib_path):
        makedirs(install_lib_path)
    for f in INSTALL_LIB_FILES:
        shutil.copyfile(pjoin(RE2_SRC_PATH, "obj", f), 
                        pjoin(install_lib_path, f))

    # RE2_LIB_PATH = pjoin(RE2_INSTALL_PATH, 'usr', 'local', 'lib')
    RE2_LIB_PATH = pjoin(RE2_INSTALL_PATH, 'lib')
    if not os.path.exists(RE2_LIB_PATH):
        makedirs(RE2_LIB_PATH)
    rename(pjoin(RE2_LIB_PATH, 'libre2.a'), 
            pjoin(RE2_LIB_PATH, 'libre2_static.a'))

if __name__ == '__main__':
    re2Clean()
    re2Build()
