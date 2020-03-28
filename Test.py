import re

from A2l_Extractor import _Capture_a2l_variable

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
# Output:  list of Variables in a given string
# TODO Multi line functions has to be checked
def _list_variables_in_line(_data):
    for _element in c_Identifiers:
        _data = _data.replace(_element, ' ')
    _list_loc = _data.split(' ')
    _list_loc = list(dict.fromkeys(_list_loc))
    while '' in _list_loc:
        _list_loc.remove('')
        _list_loc.remove('\n')
    return _list_loc


# Input:   C line with assignment
# Output:  List[0] with LHS variable  List[1] with RHS variable
# TODO If line is (int var = 10;)  This function will not differentiate data types.
def _lhs_rhs_split(_line):
    _split_data = [0, 0]
    _split_data[0] = _line.split('=')[0].replace(' ', '')
    _split_data[1] = _line.split('=')[1].replace(' ', '').replace(';', '')[:-1]
    return _split_data


# TODO This function always puts init value 255,
#       Take Limits from A2l_limits
# Input     :   A variable
# Output    :   Testcase Line for Ptu
def _test_case_line_RHS(_variable):
    _line_list = ['VAR,\t', _variable, ',\tinit = ', str(255), ',\tev = init']
    _line_complete = ""
    for item in _line_list:
        _line_complete += item
    print(_line_complete)


def _get_all_variables(_file):
    _var_in_line = []
    _all_variables_in_file = []
    _file_r = open(_file, 'r')
    _data = _file_r.readlines()
    for _line in _data:
        if _is_an_assignment(_line):
            _var_in_line = _list_variables_in_line(_line)
            for _variable in _var_in_line:
                _all_variables_in_file.append(_variable)
    _all_variables_in_file = list(dict.fromkeys(_all_variables_in_file))
    return _all_variables_in_file


# Input:   A2l File Name as String
# Output:  Dictionary Variable name and limits of Variables
#          [VARIABLE_NAME, [MIN_LIMIT  ,  MAX_LIMIT]]
def _Create_A2l_limits_of_variables(_a2l_file, _all_variables_in_file):
    a2l_limits_of_variables = {}
    _a2l_file_descriptor = open(_a2l_file, 'r')
    _A2l_file_contents = _a2l_file_descriptor.read()
    for _single_variable in _all_variables_in_file:
        data = _Capture_a2l_variable(_A2l_file_contents, _single_variable)
        data = data[5].split(' ')
        a2l_limits_of_variables[_single_variable] = data

    _a2l_file_descriptor.close()
    return a2l_limits_of_variables


Data = _remove_comments("Test.c", "data.tmp")
_All_variables_in_file = _get_all_variables("data.tmp")
print(_All_variables_in_file)
A2l_limits_of_variables = _Create_A2l_limits_of_variables("A2l_sample.txt", _All_variables_in_file)
print(A2l_limits_of_variables)
