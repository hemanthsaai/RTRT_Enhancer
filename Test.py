import re

# Contains C Identifiers
c_Identifiers = ['=', '+', '-', '*', '/', '>', '<', '!', '^', '&', '&&', '|', '||', '(', ')', ';']


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
# Returns the list of Variables in a given string
def _list_variable_in_line(_data):
    for _element in c_Identifiers:
        _data = _data.replace(_element, ' ')
    _list_loc = _data.split(' ')
    _list_loc = list(dict.fromkeys(_list_loc))
    while '' in _list_loc:
        _list_loc.remove('')
    return _list_loc


file = open("Test.c", 'r')
contents = file.readlines()

for line in contents:
    if _is_a_function(line):
        print(line)
    else:
        print(_list_variable_in_line(line))
