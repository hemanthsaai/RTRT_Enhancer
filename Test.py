import re

# Contains C Identifiers
c_Identifiers = ['=', '+', '-', '*', '/', '>', '<', '!', '^', '&', '&&', '|', '||', '(', ')', ';']
c_data_types = ['int', 'unsigned int', 'signed int', 'float',
                'long', 'double', 'uint32', 'uint16', 'uint8',
                'sint32', 'sint16', 'sint8', 'float32', 'boolean']


# Input:   FileName including its Directory
# Output:  String holding a full file without comments
# Reads the file and removes comments completely
def _remove_comments(_file_r, _file_w):
    _regex_block_comment_single_line = "/\*.*[\S]*\*/"
    _regex_block_comment_multi_line = "/\*.*[\S\s]*\*/"
    _regex_single_line = "//.*"
    _regex_remove_new_line = '\n\n\n*'
    _file_descriptor_r = open(_file_r, 'r')
    _file_descriptor_w = open(_file_w, "w")
    _contents = _file_descriptor_r.read()
    _re_object = re.compile(_regex_block_comment_single_line)
    _contents = _re_object.sub('', _contents)
    _re_object = re.compile(_regex_block_comment_multi_line)
    _contents = _re_object.sub('', _contents)
    _re_object = re.compile(_regex_single_line)
    _contents = _re_object.sub('', _contents)
    _re_object = re.compile(_regex_remove_new_line)
    _contents = _re_object.sub('', _contents)
    _file_descriptor_w.write(_contents)
    _file_descriptor_r.close()
    _file_descriptor_w.close()
    return _contents


# Input:   String
# Output:  List
# Returns  True if the parameter is a function call
def _is_a_function(_data):
    _regex = r"\w\w*\(.*\);"
    _check = re.search(_regex, _data)
    if _check:
        return True
    else:
        return False


# Input:   String
# Output:  List
# Returns  True if the parameter is an assignment
# TODO Multi line Assignment
#      statements to be considered
def _is_an_assignment(_data):
    _regex = r"\w.*=.*;"
    _check = re.search(_regex, _data)
    if _check:
        return True
    else:
        return False


# Input:   String
# Output:  TRUE/FALSE
# Returns  True if the parameter is a condition
# TODO Multi line Conditions has to be checked
def _is_a_condition(_data):
    _regex = r"if.*\(.*\)"
    _check = re.search(_regex, _data)
    if _check:
        return True
    else:
        return False


# Input:   String
# Output:  TRUE/FALSE
# Returns  True if the parameter is a loop
# TODO Add code - while, do-while, for
def _is_a_loop(_data):
    return False


# Input:   String
# Output:  TRUE/FALSE
# Returns  True if the parameter is a loop
# TODO Add code - #if, #elif,Endif
def _is_a_compiler_directive(_data):
    return False


# Input:   String
# Output:  List
# Returns the list of Variables in a given string
# TODO Multi line functions has to be checked
def _list_variables_in_line(_data):
    for _element in c_Identifiers:
        _data = _data.replace(_element, ' ')
    _list_loc = _data.split(' ')
    _list_loc = list(dict.fromkeys(_list_loc))
    while '' in _list_loc:
        _list_loc.remove('')
    return _list_loc


# Input:   C line with assignment
# Output:  List[0] with LHS variable  List[1] with RHS variable
# TODO If line is (int vaar = 10;)  This function will not differentiate data types.
def _lhs_rhs_split(_line):
    _split_data = [0, 0]
    _split_data[0] = _line.split('=')[0].replace(' ', '')
    _split_data[1] = _line.split('=')[1].replace(' ', '').replace(';', '')[:-1]
    return _split_data


# TODO This function always puts init value 255,
#       Take this from a a2l file
def _test_case_line_RHS(_variable):
    _line_list = ['VAR,\t', _variable, ',\tinit = ', str(255), ',\tev = init']
    _line_complete = ""
    for item in _line_list:
        _line_complete += item
    print(_line_complete)


def _functionality_test_1(_file):
    _file_r = open(_file, 'r')
    _data = _file_r.readlines()
    for _line in _data:
        if _is_a_function(_line):
            print(_line[:-1])
        elif _is_a_condition(_line):
            print(_line[:-1])
        elif _is_a_loop(_line):
            print(_line[:-1])
        elif _is_an_assignment(_line):
            print(_line[:-1])


def _functionality_test_2(_file):
    _file_r = open(_file, 'r')
    _data = _file_r.readlines()
    for _line in _data:
        if _is_an_assignment(_line):
            _split_data = _lhs_rhs_split(_line)
            # print(_split_data)
            _test_case_line_RHS(_split_data[0])


Data = _remove_comments("Test.c", "data.tmp")
# _functionality_test_1("data.tmp")
_functionality_test_2("data.tmp")
