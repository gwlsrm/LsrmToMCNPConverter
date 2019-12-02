"""
    Parser for .sin - files (lsrm source input files)
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


class PointDimensions:
    def __init__(self):
        self.distance = 0
        self.rho = 0

    def __repr__(self):
        return ("dimensions:\n" +
                "pdistanse=" + str(self.distance) + '\n' +
                "prho=" + str(self.rho) + '\n'
                )

    @staticmethod
    def parse_from_str(parameters):
        res = PointDimensions()
        res.distance = get_float_from_cm_str(parameters["pdistance"])
        res.rho = get_float_from_cm_str(parameters["prho"])
        return res


class PointSource:
    def __init__(self):
        self.dimensions = PointDimensions()

    def __repr__(self):
        return "PointSource\n" + str(self.dimensions)

    @staticmethod
    def parse_from_file(filename):
        parameters = parseInDoc(filename)
        if "SourceType" not in parameters or parameters["SourceType"] != "POINT":
            return None
        res = PointSource()
        res.dimensions = PointDimensions.parse_from_str(parameters)
        return res

if __name__ == "__main__":
    source = PointSource.parse_from_file("mcnp_examples/Point-10cm.sin")
    print(source)