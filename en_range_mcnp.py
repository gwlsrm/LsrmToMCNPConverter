"""
    for template mcnp in-file: INP and energy range E: [e1, e2, e3, ...]
        create new file INP_i from INP with new energy
        del INP_io
        run mcnp5 n=INP_i
        del INP_ir
"""

import mcnpvarchanger
import sys
import os

def get_out_fname(fname, cnt):
    return fname + str(cnt)

def get_enrange_str(energy):
    return f"0 0.001 {energy-0.001} {energy} {energy+0.001}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("1-st param: INP file name, 2-nd energy range")
        sys.exit()
    fname = sys.argv[1]
    energies = []
    for i in range(2, len(sys.argv)):
        energies.append(float(sys.argv[i]))
    for i,e in enumerate(energies):
        fname_out = get_out_fname(fname, i)
        varname = ["ERG", "E0"]
        varvalue = [str(e), get_enrange_str(e)]
        mcnpvarchanger.change_in_file(fname, fname_out, varname, varvalue)
        if os.path.exists(fname_out + 'o'):
            os.remove(fname_out + 'o')
        os.system('mcnp5 n=' + fname_out)
        if os.path.exists(fname_out + 'r'):
            os.remove(fname_out + 'r')

