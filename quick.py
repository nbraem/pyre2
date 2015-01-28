import re2 as re

def bump_num(matchobj):
    int_value = int(matchobj.group(0))
    return str(int_value + 1).encode('utf-8')


print(re.sub(b'\\d+', bump_num, b'08.2 -2 23x99y'))
print(b'9.3 -3 24x100y')

s = b'\\1\\1'
print(re.escape(s) == s)
print(re.sub(b'(.)', re.escape(s), b'x'))
print(re.sub(b'(.)', re.escape(s), b'x') == s)