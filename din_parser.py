"""
    Parser for .din - files (lsrm detector input files)
"""

from inhelper import *


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


class ScintDimensions:
    def __init__(self):
        self.crystal_diameter = 0
        self.crystal_height = 0
        self.crystal_front_reflector = 0
        self.crystal_side_reflector = 0
        self.crystal_front_cladding = 0
        self.crystal_side_cladding = 0
        self.det_front_pack = 0
        self.det_side_pack = 0
        self.det_front_cap = 0
        self.det_side_cap = 0
        self.det_mount = 0

    def __repr__(self):
        return ("dimesions:\n" +
                "CrystalDiameter=" + str(self.crystal_diameter) + '\n' +
                "CrystalHeight=" + str(self.crystal_height) + '\n' +
                "CrystalFrontReflector=" + str(self.crystal_front_reflector) + '\n' +
                "CrystalSideReflector=" + str(self.crystal_side_reflector) + '\n' +
                "CrystalFrontCladding=" + str(self.crystal_front_cladding) + '\n' +
                "CrystalSideCladding=" + str(self.crystal_side_cladding) + '\n' +
                "DetectorFrontPackaging=" + str(self.det_front_pack) + '\n' +
                "DetectorSidePackaging=" + str(self.det_side_pack) + '\n' +
                "DetectorFrontCap=" + str(self.det_front_cap) + '\n' +
                "DetectorSideCap=" + str(self.det_side_cap) + '\n' +
                "DetectorMounting=" + str(self.det_mount) + '\n'
                )

    @staticmethod
    def parse_dimensions(parameters):
        res = ScintDimensions()
        res.crystal_diameter = get_float_from_cm_str(parameters["DS_CrystalDiameter"])
        res.crystal_height = get_float_from_cm_str(parameters["DS_CrystalHeight"])
        res.crystal_front_reflector = get_float_from_cm_str(parameters["DS_CrystalFrontReflectorThickness"])
        res.crystal_side_reflector = get_float_from_cm_str(parameters["DS_CrystalSideReflectorThickness"])
        res.crystal_front_cladding = get_float_from_cm_str(parameters["DS_CrystalFrontCladdingThickness"])
        res.crystal_side_cladding = get_float_from_cm_str(parameters["DS_CrystalSideCladdingThickness"])
        res.det_front_pack = get_float_from_cm_str(parameters["DS_DetectorFrontPackagingThickness"])
        res.det_side_pack = get_float_from_cm_str(parameters["DS_DetectorSidePackagingThickness"])
        res.det_front_cap = get_float_from_cm_str(parameters["DS_DetectorFrontCapThickness"])
        res.det_side_cap = get_float_from_cm_str(parameters["DS_DetectorSideCapThickness"])
        res.det_mount = get_float_from_cm_str(parameters["DS_DetectorMountingThickness"])
        return res


class CoaxWellDimensions:
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
        self.detector_cap_hole_diameter = 0
        self.detector_cap_hole_height = 0
        self.detector_cap_hole_bottom_thickness = 0
        self.detector_cap_hole_side_thickness = 0
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
        res.crystal_diameter = get_float_from_cm_str(parameters["DCW_CrystalDiameter"])
        res.crystal_height = get_float_from_cm_str(parameters["DCW_CrystalHeight"])
        res.crystal_hole_diameter = get_float_from_cm_str(parameters["DCW_CrystalHoleDiameter"])
        res.crystal_hole_height = get_float_from_cm_str(parameters["DCW_CrystalHoleHeight"])
        res.crystal_front_dl = get_float_from_cm_str(parameters["DCW_CrystalFrontDeadLayer"])
        res.crystal_side_dl = get_float_from_cm_str(parameters["DCW_CrystalSideDeadLayer"])
        res.crystal_back_dl = get_float_from_cm_str(parameters["DCW_CrystalBackDeadLayer"])
        res.crystal_hole_bottom_dl = get_float_from_cm_str(parameters["DCW_CrystalHoleBottomDeadLayer"])
        res.crystal_hole_side_dl = get_float_from_cm_str(parameters["DCW_CrystalHoleSideDeadLayer"])
        res.crystal_side_cladding_thickness = get_float_from_cm_str(
            parameters["DCW_CrystalSideCladdingThickness"])
        res.cap_to_crystal_distance = get_float_from_cm_str(parameters["DCW_CapToCrystalDistance"])
        res.detector_cap_diameter = get_float_from_cm_str(parameters["DCW_DetectorCapDiameter"])
        res.detector_cap_front_thickness = get_float_from_cm_str(parameters["DCW_DetectorCapFrontThickness"])
        res.detector_cap_side_thickness = get_float_from_cm_str(parameters["DCW_DetectorCapSideThickness"])
        res.detector_cap_back_thickness = get_float_from_cm_str(parameters["DCW_DetectorCapBackThickness"])
        res.detector_cap_hole_diameter = get_float_from_cm_str(parameters["DCW_DetectorCapHoleDiameter"])
        res.detector_cap_hole_height = get_float_from_cm_str(parameters["DCW_DetectorCapHoleHeight"])
        res.detector_cap_hole_bottom_thickness = get_float_from_cm_str(parameters["DCW_DetectorCapHoleBottomThickness"])
        res.detector_cap_hole_side_thickness = get_float_from_cm_str(parameters["DCW_DetectorCapHoleSideThickness"])
        res.detector_mounting_thickness = get_float_from_cm_str(parameters["DCW_DetectorMountingThickness"])
        return res


class HPGeDetector:
    def __init__(self):
        # dimensions
        self.dimensions = HPGeDimensions()
        # materials
        self.materials = {}
        # type
        self.det_type = "Coaxial"

    def __repr__(self):
        res = '\n'.join(k + str(v) for k,v in self.materials.items())
        res = "HPGeDetector" + str(self.dimensions) + res
        return res

    @staticmethod
    def parse_from_parameters(parameters):
        if "DetectorType" not in parameters or parameters["DetectorType"] != "COAXIAL":
            return None
        res = HPGeDetector()
        res.dimensions = HPGeDimensions.parse_dimensions(parameters)
        det_type_str = "DC"
        res.materials["Crystal"] = Material.parse_material(parameters, "Crystal", det_type_str)
        res.materials["CrystalSideCladding"] = Material.parse_material(parameters, "CrystalSideCladding", det_type_str)
        res.materials["CrystalMounting"] = Material.parse_material(parameters, "CrystalMounting", det_type_str)
        res.materials["DetectorCap"] = Material.parse_material(parameters, "DetectorCap", det_type_str)
        res.materials["Vacuum"] = Material.parse_material(parameters, "Vacuum", det_type_str)
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


class ScintDetector:
    def __init__(self):
        # dimensions
        self.dimensions = ScintDimensions()
        # materials
        self.materials = {}
        # type
        self.det_type = "Scintillator"

    def __repr__(self):
        res = '\n'.join(k + str(v) for k,v in self.materials.items())
        res = "ScintDetector" + str(self.dimensions) + res
        return res

    @staticmethod
    def parse_from_parameters(parameters):
        if "DetectorType" not in parameters or parameters["DetectorType"] != "SCINTILLATOR":
            return None
        res = ScintDetector()
        res.dimensions = ScintDimensions.parse_dimensions(parameters)
        det_type_str = "DS"
        res.materials["Crystal"] = Material.parse_material(parameters, "Crystal", det_type_str)
        res.materials["CrystalCladding"] = Material.parse_material(parameters, "CrystalCladding", det_type_str)
        res.materials["CrystalReflector"] = Material.parse_material(parameters, "CrystalReflector", det_type_str)
        res.materials["DetectorPackaging"] = Material.parse_material(parameters, "DetectorPackaging", det_type_str)
        res.materials["DetectorCap"] = Material.parse_material(parameters, "DetectorCap", det_type_str)
        return res

    def get_height(self):
        return self.dimensions.det_mount + self.dimensions.crystal_height + \
               self.dimensions.crystal_front_reflector + self.dimensions.crystal_front_cladding + \
               self.dimensions.det_front_pack + self.dimensions.det_front_cap

    def get_radius(self):
        return self.dimensions.crystal_diameter / 2 + self.dimensions.crystal_side_reflector + \
               self.dimensions.crystal_side_cladding + self.dimensions.det_side_pack + \
               self.dimensions.det_side_cap

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


class CoaxWellDetector:
    def __init__(self):
        # dimensions
        self.dimensions = CoaxWellDimensions()
        # materials
        self.materials = {}
        # type
        self.det_type = "CoaxWell"

    def __repr__(self):
        res = '\n'.join(k + str(v) for k,v in self.materials.items())
        res = "CoaxWellDetector" + str(self.dimensions) + res
        return res

    @staticmethod
    def parse_from_parameters(parameters):
        if "DetectorType" not in parameters or parameters["DetectorType"] != "COAX_WELL":
            return None
        res = CoaxWellDetector()
        res.dimensions = CoaxWellDimensions.parse_dimensions(parameters)
        det_type_str = "DCW"
        res.materials["Crystal"] = Material.parse_material(parameters, "Crystal", det_type_str)
        res.materials["CrystalSideCladding"] = Material.parse_material(parameters, "CrystalSideCladding", det_type_str)
        res.materials["CrystalMounting"] = Material.parse_material(parameters, "CrystalMounting", det_type_str)
        res.materials["DetectorCap"] = Material.parse_material(parameters, "DetectorCap", det_type_str)
        res.materials["Vacuum"] = Material.parse_material(parameters, "Vacuum", det_type_str)
        return res

    def get_height(self):
        return self.dimensions.detector_cap_back_thickness + self.dimensions.detector_mounting_thickness + \
               self.dimensions.crystal_height + self.dimensions.cap_to_crystal_distance + \
               self.dimensions.detector_cap_front_thickness

    def get_radius(self):
        return self.dimensions.detector_cap_diameter / 2

    def set_top_surf_num(self, top_surf_num):
        self.top_surf_num = top_surf_num

    def get_top_surf_num(self):
        return self.top_surf_num

    def set_cyl_surf_num(self, cyl_surf_num):
        self.cyl_surf_num = cyl_surf_num

    def get_cyl_surf_num(self):
        return self.cyl_surf_num

    def set_bottom_surf_num(self, bottom_surf_num):
        self.bottom_surf_num = bottom_surf_num

    def get_bottom_surf_num(self):
        return self.bottom_surf_num

    def set_hole_top_surf_num(self, hole_top_surf_num):
        self.hole_top_surf_num = hole_top_surf_num

    def get_hole_top_surf_num(self):
        return self.hole_top_surf_num

    def set_hole_cyl_surf_num(self, hole_cyl_surf_num):
        self.hole_cyl_surf_num = hole_cyl_surf_num

    def get_hole_cyl_surf_num(self):
        return self.hole_cyl_surf_num


def parseDetFromIn(filename):
    parameters = parseInDoc(filename)
    if "DetectorType" not in parameters:
        return None
    if parameters["DetectorType"] == "COAXIAL":
        return HPGeDetector.parse_from_parameters(parameters)
    if parameters["DetectorType"] == "SCINTILLATOR":
        return ScintDetector.parse_from_parameters(parameters)
    if parameters["DetectorType"] == "COAX_WELL":
        return CoaxWellDetector.parse_from_parameters(parameters)

if __name__ == "__main__":
    detector = parseDetFromIn("mcnp_examples/Gem15P4-70_51-TP32799B_UVT_tape4.din")
    print(detector)
    print()
    detector = parseDetFromIn("mcnp_examples/NaI40x40.din")
    print(detector)
