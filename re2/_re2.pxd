# see https://github.com/cython/cython/wiki/FAQ#id35
from libcpp.string cimport string as cpp_string
#from libcpp.map cimport map as cpp_map
from libcppmap cimport map as cpp_map    # until my PR is accepted

cdef int MAGIC=7

cdef extern from "Python.h":
    IF IS_PY_THREE == 1:
        cdef bint PyBytes_Check(object)
        cdef int PyBytes_AsStringAndSize(object, char**, Py_ssize_t*)
    ELSE:
        cdef bint PyString_Check(object)
        cdef int PyString_AsStringAndSize(object, char**, Py_ssize_t*)


IF IS_PY_THREE == 1:
    cdef inline int pystring_to_cstr(object o, char** c_str_ptr, Py_ssize_t *length) except -1:
        if PyBytes_AsStringAndSize(o, c_str_ptr, length) == -1:
            return -1
        return 0
    # end def
ELSE:
    cdef inline int pystring_to_cstr(object o, char** c_str_ptr, Py_ssize_t *length) except -1:
        if PyString_AsStringAndSize(o, c_str, length) == -1:
            return -1
        return 0
    # end def
# end IF

cdef inline bytes _bytes(s):
    IF IS_PY_THREE == 1:
        if isinstance(s, str):
            # encode to the specific encoding used inside of the module
            return (<str>s).encode('utf8')
        else:
            return s
    ELSE:
        return s

cdef inline bint is_bytes(s):
    IF IS_PY_THREE == 1:
        return PyBytes_Check(s)
    ELSE:
        return PyString_Check(s)

cdef extern from "re2/stringpiece.h" namespace "re2":
    cdef cppclass StringPiece:
        StringPiece()
        StringPiece(const char*)
        StringPiece(const char*, int)
        const char* data()
        int copy(char * buf, size_t n, size_t pos)
        int length()
 
cdef extern from "re2/re2.h" namespace "re2":
    cdef enum Anchor:
        UNANCHORED "RE2::UNANCHORED"
        ANCHOR_START "RE2::ANCHOR_START"
        ANCHOR_BOTH "RE2::ANCHOR_BOTH"

    ctypedef Anchor re2_Anchor "RE2::Anchor"

    cdef enum ErrorCode:
        NoError "RE2::NoError"
        ErrorInternal "RE2::ErrorInternal"
        # Parse errors
        ErrorBadEscape "RE2::ErrorBadEscape"          # bad escape sequence
        ErrorBadCharClass "RE2::ErrorBadCharClass"       # bad character class
        ErrorBadCharRange "RE2::ErrorBadCharRange"       # bad character class range
        ErrorMissingBracket "RE2::ErrorMissingBracket"     # missing closing ]
        ErrorMissingParen   "RE2::ErrorMissingParen"       # missing closing )
        ErrorTrailingBackslash "RE2::ErrorTrailingBackslash"  # trailing \ at end of regexp
        ErrorRepeatArgument "RE2::ErrorRepeatArgument"     # repeat argument missing, e.g. "*"
        ErrorRepeatSize "RE2::ErrorRepeatSize"         # bad repetition argument
        ErrorRepeatOp "RE2::ErrorRepeatOp"           # bad repetition operator
        ErrorBadPerlOp "RE2::ErrorBadPerlOp"          # bad perl operator
        ErrorBadUTF8 "RE2::ErrorBadUTF8"            # invalid UTF-8 in regexp
        ErrorBadNamedCapture "RE2::ErrorBadNamedCapture"    # bad named capture group
        ErrorPatternTooLarge "RE2::ErrorPatternTooLarge"    # pattern too large (compile failed)

    cdef enum Encoding:
        EncodingUTF8 "RE2::Options::EncodingUTF8"
        EncodingLatin1 "RE2::Options::EncodingLatin1"

    ctypedef Encoding re2_Encoding "RE2::Options::Encoding"

    cdef cppclass Options "RE2::Options":
        Options()
        void set_posix_syntax(int b)
        void set_longest_match(int b)
        void set_log_errors(int b)
        void set_max_mem(int m)
        void set_literal(int b)
        void set_never_nl(int b)
        void set_case_sensitive(int b)
        void set_perl_classes(int b)
        void set_word_boundary(int b)
        void set_one_line(int b)
        int case_sensitive()
        void set_encoding(re2_Encoding encoding)

    cdef cppclass RE2:
        RE2(const StringPiece pattern, Options option)
        RE2(const StringPiece pattern)
        int Match(const StringPiece text, int startpos, int endpos,
                  Anchor anchor, StringPiece * match, int nmatch) nogil
        int NumberOfCapturingGroups() const
        int ok()
        const cpp_string pattern()
        cpp_string error()
        ErrorCode error_code()
        const cpp_map[cpp_string, int]& NamedCapturingGroups() const

# This header is used for ways to hack^Wbypass the cython
# issues.
cdef extern from "_re2macros.h":
    StringPiece* new_StringPiece_array(int) nogil
    void delete_StringPiece_array(StringPiece* ptr)

    # This fixes the bug Cython #548 whereby reference returns
    # cannot be addressed, due to it not being an l-value
    const cpp_map[cpp_string, int]* addressof(const cpp_map[cpp_string, int]&)
    
    cpp_string* addressofs(cpp_string&)
    
    char* as_char(const char*)

    # This fixes the bug whereby namespaces are causing
    # cython to just break for Cpp arguments.

    int pattern_Replace(cpp_string* str,
                        const RE2 pattern,
                        const StringPiece rewrite)
    int pattern_GlobalReplace(cpp_string* str,
                              const RE2 pattern,
                              const StringPiece rewrite)
