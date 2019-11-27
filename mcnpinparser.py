""" Parser for MCNP in-files"""


class Surface:
    def __init__(self, num, geom_type, geom_params):
        self.num = num
        self.type = geom_type
        self.geom_params = geom_params

    def __repr__(self):
        s = "%i     %s" % (self.num, self.type)
        s += " ".join([str(g) for g in self.geom_params])
        return s

    @staticmethod
    def parse_from_line(surf_str):
        words = surf_str.split()
        surf = Surface(int(words[0]), words[1], [])
        # surf coordinates and sizes
        for c in words[2:]:
            if c[0] == '$': break
            surf.geom_params.append(float(c))
        return surf


class Cell:
    def __init__(self, num, mat_num, density, equation):
        self.num = num
        self.mat_num = mat_num
        self.density = density
        self.equation = equation

    def __repr__(self):
        s = "%i     %i " % (self.num, self.mat_num)
        if self.mat_num:
            s += ' ' + str(self.density) + ' '
        return s + self.equation

    @staticmethod
    def parse_from_line(cell_str):
        words = cell_str.split()

        cell = Cell(int(words[0]), int(words[1]), 0.0, "")
        if cell.mat_num != 0:
            cell.density = float(words[2])
            idx = 3
        else:
            cell.density = 0.0
            idx = 2
        # cell equation
        cell.equation = ' '.join(words[idx:])
        return cell


class Element:
    def __init__(self, z, frac):
        self.z = z
        self.frac = frac

    def __repr__(self):
        return f"{self.z}000 {self.frac}"

class Material:
    def __init__(self, num, elements):
        self.num = num
        self.elements = elements

    def __repr__(self):
        s = f"M{self.num}    "
        s += " ".join([str(e) for e in self.elements])
        return s


class McnpTask:
    def __init__(self, task_name):
        self.task_name = task_name
        self.surfaces = []
        self.cells = []
        self.datacards = {}

    @staticmethod
    def parse_from_in_file(filename):
        with open(filename) as f:
            # read header
            mcnp = McnpTask(f.readline().strip())
            # read cells
            while True:
                s = f.readline().strip()
                if s != '' and s[0] in "1234567890":
                    break
            while True:
                if s == '': break
                if s[0] == '$': continue
                mcnp.cells.append(Cell.parse_from_line(s))
                s = f.readline().strip()

            # read surfaces
            while True:
                s = f.readline().strip()
                if s and s[0] in "1234567890":
                    break
            while True:
                if s == '': break
                if s[0] == '$': continue
                mcnp.surfaces.append(Surface.parse_from_line(s))
                s = f.readline().strip()

            # read data cards
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
                    mcnp.datacards[key] = " ".join(words[1:])
                else:
                    mcnp.datacards[key] += " " + s.strip()
                s = f.readline().rstrip()
        return mcnp
