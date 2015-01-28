import os.path
from os.path import join as pjoin
import subprocess

PACKAGE_PATH =          os.path.abspath(os.path.dirname(__file__))
MODULE_PATH =           pjoin(PACKAGE_PATH, 're2')

RE2_SRC_PATH =          pjoin(PACKAGE_PATH, 're2_cpp')

RE2_INSTALL_PATH = pjoin(MODULE_PATH, 'src', 're2_cpp')

def re2Clean():
    # Clean up any previous primer3 builds
    re2clean = subprocess.Popen(['make clean'], shell=True, 
                               cwd=RE2_SRC_PATH)
    re2clean.wait()


def re2Build():
    # Build primer3
    e_cmd = 'make clean; make DESTDIR=%s -j4; make DESTDIR=%s install' % (RE2_INSTALL_PATH, RE2_INSTALL_PATH)
    p3build = subprocess.Popen([e_cmd],
                                shell=True, 
                                cwd=RE2_SRC_PATH)
    re2build.wait()

if __name__ == '__main__':
    re2Clean()
    re2Build()
