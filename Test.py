import re

# Contains C Identifiers
c_Identifiers = ['=', '+', '-', '*', '/', '>', '<', '!', '^', '&', '&&', '|', '||', '(', ')', ';']


# Input:   FileName including its Directory
# Output:  String holding a full file without comments
# Reads the file and removes comments completely
def _remove_comments(_file):
    _regex_block_comment_single_line = "/\*.*[\S]*\*/"
    _regex_block_comment_multi_line = "/\*.*[\S\s]*\*/"
    _regex_single_line = "//.*"
    _file_descriptor = open(_file, 'r')
    _contents = _file_descriptor.read()
    _re_object = re.compile(_regex_block_comment_single_line)
    _contents = _re_object.sub('', _contents)
    _re_object = re.compile(_regex_block_comment_multi_line)
    _contents = _re_object.sub('', _contents)
    _re_object = re.compile(_regex_single_line)
    _contents = _re_object.sub('', _contents)
    _file_descriptor.close()

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


def _functionality_test_1():
    file = open("Test.c", 'r')
    contents = file.readlines()

    for line in contents:
        if _is_a_function(line):
            print(line[:-1])
        elif _is_a_condition(line):
            print(line[:-1])
        elif _is_a_loop(line):
            print(line[:-1])
        elif _is_an_assignment(line):
            print(line[:-1])

    file.close()


def _functionality_test_2():
    data = _remove_comments("Test.c")
    print(data)


_functionality_test_2()
