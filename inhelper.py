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


class Element:
    def __init__(self):
        self.z = 0
        self.mf = 0

    def __repr__(self):
        return '{' + str(self.z) + ':' + str(self.mf) + '}'

    @staticmethod
    def parse_element(parameters, material_name, num, det_type):
        element = Element()
        z = det_type + "_Z" + material_name + '[' + str(num) + ']'
        element.z = int(parameters[z])
        mf = det_type + "_Fractions" + material_name + '[' + str(num) + ']'
        element.mf = float(parameters[mf])
        return element


class Material:
    def __init__(self):
        self.rho = 0
        self.elements = []

    def __repr__(self):
        res = ','.join([str(e) for e in self.elements])
        res = "{Rho=" + str(self.rho) + " elements=" + res + "}"
        return res

    @staticmethod
    def parse_material(parameters, material_name, type_str):
        res = Material()
        res.rho = float(parameters[type_str + "_Ro" + material_name])
        if material_name != "Vacuum":
            nElements = type_str + "_n" + material_name + "Elements"
        else:
            nElements = type_str + "_n" + material_name
        nElements = int(parameters[nElements])
        for i in range(nElements):
            element = Element.parse_element(parameters, material_name, i, type_str)
            res.elements.append(element)
        return res