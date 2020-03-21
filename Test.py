data_ = "variable1=variable1*variable2/data_12_val+!(variable_3)-variable4<<variable5>>variable6^variable7>>(variable&&variable9);"
opers = ['=', '+', '-', '*', '/', '>', '<', '!', '^', '&', '&&', '|', '||', '(', ')', ';']
list_ = []


# Input:   String
# Output:  List
# Function returns the list of Variables in a given string
def list_variable_in_line(data):
    for i in opers:
        data = data.replace(i, ' ')
    list_loc = data.split(' ')
    list_loc = list(dict.fromkeys(list_loc))
    list_loc.remove('')
    return list_loc


data2 = 'a = b + c'
list_ = list_variable_in_line(data2)
print(list_)
