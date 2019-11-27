"""
change parameter in mcnp in-file
use change_in_file function:
fname -- name of the in-fiel
varname -- name for variable, which value needs to be changed
varvalue -- new value for varname
result file will be saved to fname_out
"""

import sys

def change_line(line, varname, varvalue):
    # simple variant: variable is head of string
    if line.startswith(varname):
        return varname + ' '*(6-len(varname)) + varvalue + '\n'

    # Complex variant: variable is in the middle of the string
    b = line.find(varname) + len(varname)
    print("1st begin line: ", line[:b])
    i = 0
    for c in line[b:]:
        if c == ' ' or c == '=':
            i += 1
            continue
        break
    b += i # begin of the value
    print("begin line: ", line[:b])
    i = 0
    for c in line[b:]:
        if c == ' ': break
        i += 1
    for c in line[b+i:]:
        if c.isalpha() and c != ' ':
            break
        i += 1
    e = b + i # end of the value
            
    print("end line: ", line[e:])
    line = line[:b] + varvalue + ' ' + line[e:]
    if line[-1] != '\n': line += '\n'
    return line

def change_in_file(fname, fname_out, varname, varvalue):
    f = open(fname_out, "w")
    for line in open(fname):
        for n,v in zip(varname, varvalue):
            if n in line:
                line = change_line(line, n, v)
        f.write(line)
    f.close()
            

if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit
    fname = sys.argv[1]
    fname_out = sys.argv[2]
    varname = []
    varvalue = []
    param_count = len(sys.argv)
    for i in range(3, param_count, 2):
        varname.append(sys.argv[i])
        varvalue.append(sys.argv[i+1])
    change_in_file(fname, fname_out, varname, varvalue)
    
    
