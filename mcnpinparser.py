""" Parser for MCNP in-files"""

#class dataline:

class surface:
    def __init__(self, surf_str):
        #print("surf str: ", surf_str)
        words = surf_str.split()
        # surface number
        self.num = int(words[0])
        # surface type
        self.type = words[1]
        # surf coordinates and sizes
        self.geom = []
        for c in words[2:]:
            if c[0] == '$': break
            self.geom.append(float(c))

    def __repr__(self):
        s = "%i     %s" % (self.num, self.type)
        for g in self.geom:
            s += " " + str(g)
        return s

class cell:
    def __init__(self, cell_str):
        #print("cell str: ", cell_str)
        words = cell_str.split()
        # cell number
        self.num = int(words[0])
        # cell material num
        self.mat_num = int(words[1])
        if self.mat_num != 0:
            self.density = float(words[2])
            idx = 3
        else:
            self.density = 0.0
            idx = 2
        # cell equation
        self.cell_equation = ' '.join(words)

    def __repr__(self):
        s = "%i     %i " % (self.num, self.mat_num)
        if self.mat_num != 0:
            s += ' ' + str(self.density) + ' '
        return s + self.cell_equation

class infile:
    def __init__(self, filename):
        with open(filename) as f:
            # read header
            self.header = f.readline().strip()
            # read cells
            self.cells = []
            while True:
                s = f.readline().strip()
                if s != '' and s[0] in "1234567890":
                    break
            while True:
                if s == '': break
                if s[0] == '$': continue
                self.cells.append(cell(s))
                s = f.readline().strip()
                
            # read surfaces
            self.surfaces = []
            while True:
                s = f.readline().strip()
                if s != '' and s[0] in "1234567890":
                    break
            while True:
                if s == '': break
                if s[0] == '$': continue
                self.surfaces.append(surface(s))
                s = f.readline().strip()
                
            # read data cards
            self.datacards = {}
            while True:
                s = f.readline().rstrip()
                if s != '':
                    break
            while True:
                if s == '': break
                if s[0] == '$': continue
                if s[0] != ' ':
                    words = s.split()
                    key = words[0]
                    self.datacards[key] =" ".join(words[1:])
                else:
                    self.datacards[key] += " " + s.strip()
                s = f.readline().rstrip()
            
