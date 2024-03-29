import re


# Input:   Entire A2l File as a String
# Output:  List with all available detail of A2l variable
def _Capture_a2l_variable(_file_contents, _variable):
    _regex = r"\/\w*\s\w*\s(" + _variable + r")\s\"(.*)\"\n\s*(\w*)\s(\w*)\s(\d\s\d*\s)(.*)"
    _extracted = re.search(_regex, _file_contents)
    if _extracted:
        return _extracted.groups()
    else:
        return 0
