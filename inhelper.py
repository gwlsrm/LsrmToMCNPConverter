"""
    Helper functions for reading lsrm in-files (din and sin)
"""

def parseInDoc(filename):
    parameters = {}
    with open(filename, 'r') as f:
        for l in f:
            if '=' not in l: continue
            n, v = ((w.strip() for w in l.split('=')))
            parameters[n] = v
    return parameters

def get_float_from_cm_str(cm_str):
    words = cm_str.split()
    return float(words[0])