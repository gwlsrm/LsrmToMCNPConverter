""" Parser for MCNP in-files"""

EN_DELTA = 0.001


class Surface:
    def __init__(self, num, geom_type, geom_params):
        self.num = num
        self.type = geom_type
        self.geom_params = geom_params

    def __repr__(self):
        s = "%i     %s " % (self.num, self.type)
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
            s += '-' + str(self.density) + ' '
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


class PhotonSource:
    def __init__(self, x, y, z, energy):
        self.x = x
        self.y = y
        self.z = z
        self.energy = energy


class PhotonPointSource(PhotonSource):
    def __init__(self, x, y, z, energy):
        PhotonSource.__init__(self, x, y, z, energy)

    def __repr__(self):
        return "SDEF  POS=%g %g %g ERG=%g PAR=2" % (self.x, self.y, self.z, self.energy)


class CylPhotonSource(PhotonSource):
    def __init__(self, x, y, z, energy, height, radius):
        PhotonSource.__init__(self, x, y, z, energy)
        self.height = height
        self.radius = radius

    def __repr__(self):
        str = "SDEF  POS=%g %g %g ERG=%g PAR=2 RAD=D2 EXT=D3 AXS=0 0 1\n" % (self.x, self.y, self.z, self.energy)
        str += f"SI2 {self.radius}\n"
        str += f"SI3 {self.height}"
        return str


class CalcParams:
    def __init__(self, cell_importance, photon_source, det_cell, energies, materials, nps):
        self.cell_importance = cell_importance
        self.photon_source = photon_source
        self.det_cell = det_cell
        self.en_range = []
        if energies[0] != 0:
            self.en_range.append(0)
        for e in energies:
            if e == 0: continue
            self.en_range.append(e - EN_DELTA)
            self.en_range.append(e + EN_DELTA)
        self.materials = materials
        self.nps = nps

    def __repr__(self):
        res = "MODE  P\n"
        res += "IMP:P " + " ".join(str(c) for c in self.cell_importance) + '\n'
        res += str(self.photon_source) + '\n'
        res += "F8:P  " + str(self.det_cell) + '\n'
        res += "E0    " + " ".join(str(e) for e in self.en_range) + '\n'
        res += "\n".join(str(m) for m in self.materials) + '\n'
        res += "NPS   %d" % (self.nps)
        return res


class McnpTask:
    def __init__(self, task_name):
        self.task_name = task_name
        self.surfaces = []
        self.cells = []
        self.datacards = {}
        self.materials = []
        self.calc_parameters = None

    def add_surface(self, surf_num, geom_type, *geom_parameters):
        self.surfaces.append(Surface(surf_num, geom_type, geom_parameters))

    def add_cell(self, cell_num, mat_num, density, equation):
        self.cells.append(Cell(cell_num, mat_num, density, equation))

    def add_material(self, mat_num, elements):
        self.materials.append(Material(mat_num, []))
        for e in elements:
            self.materials[-1].elements.append(Element(e.z, e.mf))

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

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.task_name + '\n')
            # print cells
            for c in self.cells:
                f.write(str(c) + '\n')
            f.write('\n')
            for s in self.surfaces:
                f.write(str(s) + '\n')
            f.write('\n')
            f.write(str(self.calc_parameters))
