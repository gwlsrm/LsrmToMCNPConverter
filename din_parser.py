"""
    Parser for .din - files (lsrm detector input files)
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

class HPGeDimensions:
    def __init__(self):
        self.crystal_diameter = 0
        self.crystal_height = 0
        self.crystal_hole_diameter = 0
        self.crystal_hole_height = 0
        self.crystal_front_dl = 0
        self.crystal_side_dl = 0
        self.crystal_back_dl = 0
        self.crystal_hole_bottom_dl = 0
        self.crystal_hole_side_dl = 0
        self.crystal_side_cladding_thickness = 0
        self.cap_to_crystal_distance = 0
        self.detector_cap_diameter = 0
        self.detector_cap_front_thickness = 0
        self.detector_cap_side_thickness = 0
        self.detector_cap_back_thickness = 0
        self.detector_mounting_thickness = 0

    def __repr__(self):
        return ("dimesions:\n" +
                "CrystalDiameter=" + str(self.crystal_diameter) + '\n' +
                "CrystalHeight=" + str(self.crystal_height) + '\n' +
                "CrystalHoleDiameter=" + str(self.crystal_hole_diameter) + '\n' +
                "CrystalHoleHeight=" + str(self.crystal_hole_height) + '\n' +
                "CrystalFrontDeadLayer=" + str(self.crystal_front_dl) + '\n' +
                "CrystalSideDeadLayer=" + str(self.crystal_side_dl) + '\n' +
                "CrystalBackDeadLayer=" + str(self.crystal_back_dl) + '\n'

                "CrystalHoleBottomDeadLayer=" + str(self.crystal_hole_bottom_dl) + '\n' +
                "CrystalHoleSideDeadLayer=" + str(self.crystal_hole_side_dl) + '\n' +
                "CrystalSideCladdingThickness=" + str(self.crystal_side_cladding_thickness) + '\n' +
                "CapToCrystalDistance=" + str(self.cap_to_crystal_distance) + '\n' +
                "DetectorCapDiameter=" + str(self.detector_cap_diameter) + '\n' +
                "DetectorCapFrontThickness=" + str(self.detector_cap_front_thickness) + '\n' +
                "DetectorCapSideThickness=" + str(self.detector_cap_side_thickness) + '\n' +
                "DetectorCapBackThickness=" + str(self.detector_cap_back_thickness) + '\n' +
                "DetectorMountingThickness=" + str(self.detector_mounting_thickness) + '\n'
                )

    @staticmethod
    def parse_dimensions(parameters):
        res = HPGeDimensions()
        res.crystal_diameter = get_float_from_cm_str(parameters["DC_CrystalDiameter"])
        res.crystal_height = get_float_from_cm_str(parameters["DC_CrystalHeight"])
        res.crystal_hole_diameter = get_float_from_cm_str(parameters["DC_CrystalHoleDiameter"])
        res.crystal_hole_height = get_float_from_cm_str(parameters["DC_CrystalHoleHeight"])
        res.crystal_front_dl = get_float_from_cm_str(parameters["DC_CrystalFrontDeadLayer"])
        res.crystal_side_dl = get_float_from_cm_str(parameters["DC_CrystalSideDeadLayer"])
        res.crystal_back_dl = get_float_from_cm_str(parameters["DC_CrystalBackDeadLayer"])
        res.crystal_hole_bottom_dl = get_float_from_cm_str(parameters["DC_CrystalHoleBottomDeadLayer"])
        res.crystal_hole_side_dl = get_float_from_cm_str(parameters["DC_CrystalHoleSideDeadLayer"])
        res.crystal_side_cladding_thickness = get_float_from_cm_str(
            parameters["DC_CrystalSideCladdingThickness"])
        res.cap_to_crystal_distance = get_float_from_cm_str(parameters["DC_CapToCrystalDistance"])
        res.detector_cap_diameter = get_float_from_cm_str(parameters["DC_DetectorCapDiameter"])
        res.detector_cap_front_thickness = get_float_from_cm_str(parameters["DC_DetectorCapFrontThickness"])
        res.detector_cap_side_thickness = get_float_from_cm_str(parameters["DC_DetectorCapSideThickness"])
        res.detector_cap_back_thickness = get_float_from_cm_str(parameters["DC_DetectorCapBackThickness"])
        res.detector_mounting_thickness = get_float_from_cm_str(parameters["DC_DetectorMountingThickness"])
        return res

class Element:
    def __init__(self):
        self.z = 0
        self.mf = 0

    def __repr__(self):
        return '{' + str(self.z) + ':' + str(self.mf) + '}'

    @staticmethod
    def parse_element(parameters, material_name, num):
        element = Element()
        z = "DC_Z" + material_name + '[' + str(num) + ']'
        element.z = int(parameters[z])
        mf = "DC_Fractions" + material_name + '[' + str(num) + ']'
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
    def parse_material(parameters, material_name):
        res = Material()
        res.rho = float(parameters["DC_Ro" + material_name])
        if material_name != "Vacuum":
            nElements = "DC_n" + material_name + "Elements"
        else:
            nElements = "DC_n" + material_name
        nElements = int(parameters[nElements])
        for i in range(nElements):
            element = Element.parse_element(parameters, material_name, i)
            res.elements.append(element)
        return res


class PPDDetector:
    def __init__(self):
        # dimensions
        self.dimensions = HPGeDimensions()
        # materials
        self.materials = {}

    def __repr__(self):
        res = '\n'.join(k + str(v) for k,v in self.materials.items())
        res = "HPGeDetector" + str(self.dimensions) + res
        return res

    @staticmethod
    def parse_from_file(filename):
        parameters = parseInDoc(filename)
        if "DetectorType" not in parameters or parameters["DetectorType"] != "COAXIAL":
            return None
        res = PPDDetector()
        res.dimensions = HPGeDimensions.parse_dimensions(parameters)
        res.materials["Crystal"] = Material.parse_material(parameters, "Crystal")
        res.materials["CrystalSideCladding"] = Material.parse_material(parameters, "CrystalSideCladding")
        res.materials["CrystalMounting"] = Material.parse_material(parameters, "CrystalMounting")
        res.materials["DetectorCap"] = Material.parse_material(parameters, "DetectorCap")
        res.materials["Vacuum"] = Material.parse_material(parameters, "Vacuum")
        return res

    def get_height(self):
        return self.dimensions.detector_cap_back_thickness + self.dimensions.detector_mounting_thickness + \
               self.dimensions.crystal_height + self.dimensions.cap_to_crystal_distance + \
               self.dimensions.detector_cap_front_thickness

    def get_radius(self):
        return self.dimensions.detector_cap_diameter / 2

    def set_top_surf_num(self, top_surf_num):
        self.top_surf_num = top_surf_num

    def set_cyl_surf_num(self, cyl_surf_num):
        self.cyl_surf_num = cyl_surf_num

    def set_bottom_surf_num(self, bottom_surf_num):
        self.bottom_surf_num = bottom_surf_num

    def get_top_surf_num(self):
        return self.top_surf_num

    def get_cyl_surf_num(self):
        return self.cyl_surf_num

    def get_bottom_surf_num(self):
        return self.bottom_surf_num

if __name__ == "__main__":
    detector = PPDDetector.parse_from_file("Gem15P4-70_51-TP32799B_UVT_tape4.din")
    print(detector)
