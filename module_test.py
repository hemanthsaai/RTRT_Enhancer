f = open("Test.c", "r")

data = f.readlines()
status = 0
for line in data:
    if status == 0:
        if '/*' in line:
            if '*/' in line:
                continue
            else:
                status = 1
        elif '//' in line:
            continue
        else:
            print(line)

    else:
        if '*/' in line:
            status = 0

f.close()
