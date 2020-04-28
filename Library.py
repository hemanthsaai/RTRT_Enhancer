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


# Input:   Variable
# Output:  TRUE/FALSE
# Returns  True if the string is a MACRO or a CONSTANT
def _is_a_macroOrConstant(_split_line):
    _split_line = _split_line.replace(' ', '')
    if _split_line.isnumeric() or _split_line.isupper():
        return True
    else:
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


# Input:   C line with assignment
# Output:  List[0] with LHS variable  List[1] with RHS variable
# TODO If line is (int var = 10;)  This function will not differentiate data types.
def _lhs_rhs_split_regex(_line):
    # _regex = r"\(?\s?\w*?\s?\)?\s*?(\w*\W*?\w*)\s*?=\s*?\(?\s?\w*?\s?\*?\s?\)?\s*?(\w*\W*?\w*)\s*;"
    _regex = r"\(?\s?\w*?\s?\)?\s*?(\w*\W*?\w*)\s*?=(\s*?\(?\s?\w*?\s?\*?\s?\)\s*?)?(\w*\W*?\w*)\s*;"
    _check = re.search(_regex, _line)
    if _check:
        return _check.groups()
    else:
        return 0


# TODO This function always puts init value as a2l_MAX VALUE,
#       Take both Limits from A2l_limits
# Input     :   RHS variable and a2l_limits_of_variables
# Output    :   returns [PTU_LINE_OF_VARIABLE,
#               which is expected value for LHS
def _test_case_line_RHS(_variable, a2l_limits_of_variables):
    _rhs_init_val = a2l_limits_of_variables[_variable]
    _line_list = ['VAR\t', _variable, ',\tinit (RTRT_Iter) in {', _rhs_init_val[0], ',', _rhs_init_val[1],
                  '},\t\tev = init']
    _line_complete = ""
    for item in _line_list:
        _line_complete += item
    return [_line_complete, _rhs_init_val]


# Input     :   "LHS variable", "a2l_limits_of_variables" and "initial value for RHS in same line"
# Output    :   LHS Test case Line for Ptu
def _test_case_line_LHS(_variable, a2l_limits_of_variables, _rhs_init_val):
    _line_list = ['VAR\t', _variable, ',\tinit = 0', ',\t\tev (RTRT_Iter) with {', _rhs_init_val[0], ',',
                  _rhs_init_val[1], '}']
    _line_complete = ""
    for item in _line_list:
        _line_complete += item
    return _line_complete


# Input     :   "LHS variable", and "expected value for RHS in same line"
# Output    :   LHS Test case Line for Ptu for a MACRO
def _test_case_line_LHS_MACRO_CONSTANT(_variable, _rhs_ev_val):
    _line_list = ['VAR\t', _variable, ',\tinit = 0', ',\t\tev = ', _rhs_ev_val]
    _line_complete = ""
    for item in _line_list:
        _line_complete += item
    return _line_complete


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
# TODO  : If a variable has no limits in A2l This function set limits as [0, 255]
#         In such cases the Max and Min limits of a variable has to be used
def _Create_A2l_limits_of_variables(_a2l_file, _all_variables_in_file):
    a2l_limits_of_variables = {}
    _a2l_file_descriptor = open(_a2l_file, 'r')
    _A2l_file_contents = _a2l_file_descriptor.read()
    for _single_variable in _all_variables_in_file:
        data = _Capture_a2l_variable(_A2l_file_contents, _single_variable)
        if data:
            if len(data) > 4:
                data = data[5].split(' ')
            else:
                data = ['0', '255']
        else:
            data = ['0', '255']
        a2l_limits_of_variables[_single_variable] = data

    _a2l_file_descriptor.close()
    return a2l_limits_of_variables


def _Test_case_for_line(_split_line):
    if not (_is_a_macroOrConstant(_split_line[2])):
        _TestCaseLine_Rhs_init_val = _test_case_line_RHS(_split_line[2], A2l_limits_of_variables)
        print(_TestCaseLine_Rhs_init_val[0])
        _Test_caseLine_LHS = _test_case_line_LHS(_split_line[0], A2l_limits_of_variables, _TestCaseLine_Rhs_init_val[1])
        print(_Test_caseLine_LHS + '\n')
    else:
        _Test_caseLine_LHS = _test_case_line_LHS_MACRO_CONSTANT(_split_line[0], _split_line[2])
        print(_Test_caseLine_LHS + '\n')


Data = _remove_comments("Test.c", "data.tmp")
_All_variables_in_file = _get_all_variables("data.tmp")
# print(_All_variables_in_file)
A2l_limits_of_variables = _Create_A2l_limits_of_variables("A2l_sample.txt", _All_variables_in_file)


# print(A2l_limits_of_variables)


def Create_Test_case_Sample():
    print('VAR\tRTRT_Iter,\tinit in {0, 1},\tev = init')
    file = open("data.tmp", 'r')
    contents = file.readlines()
    for line in contents:
        if _is_an_assignment(line):
            split_line = _lhs_rhs_split_regex(line)
            if split_line:
                try:
                    _Test_case_for_line(split_line)
                except:
                    print("Error in line:", split_line)

    file.close()


Create_Test_case_Sample()
