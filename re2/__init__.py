import re2._re2

def _to_bytes(s):
  return bytes(s, 'utf-8')

def search(pattern, in_string, flags=0):
  return re2._re2.search(_to_bytes(pattern), _to_bytes(in_string), flags)

def match(pattern, in_string, flags=0):
  return re2._re2.match(_to_bytes(pattern), _to_bytes(in_string), flags)

def finditer(pattern, in_string, flags):
  return re2._re2.finditer(_to_bytes(pattern), _to_bytes(in_string), flags)

def findall(pattern, in_string, flags=0):
  return re2._re2.findfall(_to_bytes(pattern), _to_bytes(in_string), flags)

class Pattern:
  def __init__(self, p):
    self._p = p

  def search(self, in_string, pos=0, endpos=-1):
    return self._p.search(_to_bytes(in_string), pos, endpos)

def compile(pattern, flags=0, max_mem=8388608):
  return Pattern(re2._re2.compile(_to_bytes(pattern), flags, max_mem))
