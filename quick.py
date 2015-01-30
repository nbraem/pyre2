import re2
import re
import timeit

def bump_num(matchobj):
    int_value = int(matchobj.group(0))
    return str(int_value + 1).encode('utf-8')


print(re2.sub(b'\\d+', bump_num, b'08.2 -2 23x99y'))
print(b'9.3 -3 24x100y')

s = b'\\1\\1'
print(re2.escape(s) == s)
print(re2.sub(b'(.)', re2.escape(s), b'x'))
print(re2.sub(b'(.)', re2.escape(s), b'x') == s)

import os.path as opath
path = opath.dirname(opath.abspath(__file__))
fn = opath.join(path, "tests", "genome.dat")
with open(fn, 'rb') as fd:
    genome = fd.read()

search = b"c[cg]cg[ag]g"
# search = b"cattctg"

re2_regex = re2.compile(search)
re_regex = re.compile(search)
def testre2():
    return re2_regex.findall(genome)
def testre():
    return re_regex.findall(genome)

print(timeit.timeit("testre2()", setup="from __main__ import testre2", number=100))
print(timeit.timeit("testre()", setup="from __main__ import testre", number=100))