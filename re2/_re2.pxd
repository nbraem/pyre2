# TODO: bring up to current cython spec for const and c++ strings
# see https://github.com/cython/cython/wiki/FAQ#id35
#cdef extern from *:
#    ctypedef char* const_char_ptr "const char*"

#cdef extern from "<string>" namespace "std":
#    cdef cppclass string:
#        string(char *)
#        string(char *, size_t n)
#        const_char_ptr c_str()
#        int length()
#        void push_back(char c)



#    ctypedef string cpp_string "std::string"
#    ctypedef string const_string "const std::string"

from libcpp.string cimport string as cpp_string

#cdef extern from "<map>" namespace "std":
#    cdef cppclass stringintmapiterator "std::map<std::string, int>::const_iterator":
#        cpp_string first
#        int second
#        stringintmapiterator operator++()
#        bint operator==(stringintmapiterator)
#        stringintmapiterator& operator*(stringintmapiterator)
#        bint operator!=(stringintmapiterator)

#    cdef cppclass const_stringintmap "const std::map<std::string, int>":
#        stringintmapiterator begin()
#        stringintmapiterator end()
#        int operator[](cpp_string)

from libcpp.map cimport map as cpp_map
#cdef  cpp_map[string, int].const_iterator it = ...

cdef int MAGIC=7

cdef extern from "Python.h":
    IF IS_PY_THREE == 1:
        cdef bint PyBytes_Check(object)
        cdef int PyBytes_AsStringAndSize(object, char**, Py_ssize_t*)
        #cdef object PyBytes_FromString(const char*)
        #cdef object PyBytes_FromStringAndSize(const char*, Py_ssize_t)
        #cdef char* PyBytes_AsString(object)

        cdef char* PyUnicode_AsUTF8AndSize(object, Py_ssize_t*)
        #cdef object PyUnicode_FromString(const char*)
        #cdef object PyUnicode_FromStringAndSize(const char*, Py_ssize_t)
        #cdef char* PyUnicode_AsUTF8(object)
    ELSE:
        #cdef object PyString_FromString(char *)
        #cdef object PyString_FromStringAndSize(char *, Py_ssize_t len)
        cdef int PyString_AsStringAndSize(object, char**, Py_ssize_t*)
        #cdef char* PyString_AsString(object)


IF IS_PY_THREE == 1:
    cdef inline int pystring_to_cstr(object o, char** c_str_ptr, Py_ssize_t *length) except -1:
        cdef int obj_type
        cdef size_t b_length
        if PyBytes_Check(o):
            obj_type = 0
            if PyBytes_AsStringAndSize(o, c_str_ptr, length) == -1:
                return -1
        else:
            obj_type = 1
            c_str_ptr[0] = PyUnicode_AsUTF8AndSize(o, length)
            if c_str_ptr[0] == NULL:
                return -1
        return obj_type
    # end def
ELSE:
    cdef inline int pystring_to_cstr(object o, char** c_str_ptr, Py_ssize_t *length) except -1:
        if PyString_AsStringAndSize(o, c_str, length) == -1:
            return -1
        return 0
    # end def
# end IF


cdef extern from "re2/stringpiece.h" namespace "re2":
    cdef cppclass StringPiece:
        StringPiece()
        StringPiece(const char*)
        StringPiece(const char*, int)
        const char* data()
        int copy(char * buf, size_t n, size_t pos)
        int length()

    #ctypedef StringPiece const_StringPiece "const StringPiece"
 
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

    #ctypedef Options const_Options "const RE2::Options"

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
        #const_stringintmap& NamedCapturingGroups()
        const cpp_map[cpp_string, int]& NamedCapturingGroups() const

    #ctypedef RE2 const_RE2 "const RE2"

# This header is used for ways to hack^Wbypass the cython
# issues.
cdef extern from "_re2macros.h":
    StringPiece* new_StringPiece_array(int) nogil
    void delete_StringPiece_array(StringPiece* ptr)

    # This fixes the bug Cython #548 whereby reference returns
    # cannot be addressed, due to it not being an l-value
    #const_stringintmap * addressof(const_stringintmap&)
    const cpp_map[cpp_string, int]* addressof(const cpp_map[cpp_string, int]&)
    
    #cpp_string * addressofs(cpp_string&)
    cpp_string* addressofs(cpp_string&)
    
    char* as_char(const char*)

    # This fixes the bug whereby namespaces are causing
    # cython to just break for Cpp arguments.

    #int pattern_Replace(cpp_string *str,
    #                    const_RE2 pattern,
    #                    const StringPiece rewrite)
    #int pattern_GlobalReplace(cpp_string *str,
    #                          const_RE2 pattern,
    #                          const StringPiece rewrite)

    int pattern_Replace(cpp_string* str,
                        const RE2 pattern,
                        const StringPiece rewrite)
    int pattern_GlobalReplace(cpp_string* str,
                              const RE2 pattern,
                              const StringPiece rewrite)
