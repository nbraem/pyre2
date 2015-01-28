import os.path
from os.path import join as pjoin
import subprocess
from os import rename

PACKAGE_PATH =          os.path.abspath(os.path.dirname(__file__))
MODULE_PATH =           pjoin(PACKAGE_PATH, 're2')

RE2_SRC_PATH =          pjoin(PACKAGE_PATH, 're2_cpp')

RE2_INSTALL_PATH = pjoin(MODULE_PATH, 'src', 're2_cpp')

def re2Clean():
    re2clean = subprocess.Popen(['make clean'], shell=True, 
                               cwd=RE2_SRC_PATH)
    re2clean.wait()


def re2Build():
    e_cmd = 'make clean; make DESTDIR=%s -j4; make DESTDIR=%s install' % (RE2_INSTALL_PATH, RE2_INSTALL_PATH)
    re2build = subprocess.Popen([e_cmd],
                                shell=True, 
                                cwd=RE2_SRC_PATH)
    re2build.wait()
    RE2_LIB_PATH = pjoin(RE2_INSTALL_PATH, 'usr', 'local', 'lib')
    rename(pjoin(RE2_LIB_PATH, 'libre2.a'), 
            pjoin(RE2_LIB_PATH, 'libre2_static.a'))

if __name__ == '__main__':
    re2Clean()
    re2Build()
