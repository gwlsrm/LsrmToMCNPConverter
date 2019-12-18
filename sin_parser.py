"""
    Parser for .sin - files (lsrm source input files)
"""

from inhelper import *

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


class CylinderDimensions:
    def __init__(self):
        self.distance = 0
        self.beaker_diameter = 0
        self.beaker_height = 0
        self.beaker_side_wall_thickness = 0
        self.beaker_end_wall_thickness = 0
        self.source_height = 0

    def __repr__(self):
        return ("dimensions:\n" +
                "distance=" + str(self.distance) + '\n' +
                "beaker_diameter=" + str(self.beaker_diameter) + '\n' +
                "beaker_height=" + str(self.beaker_height) + '\n' +
                "beaker_side_wall_thickness=" + str(self.beaker_side_wall_thickness) + '\n' +
                "beaker_end_wall_thickness=" + str(self.beaker_end_wall_thickness) + '\n' +
                "source_height=" + str(self.source_height) + '\n'
                )

    @staticmethod
    def parse_from_str(parameters):
        res = CylinderDimensions()
        res.distance = get_float_from_cm_str(parameters["SC_BeakerToDetectorFrontDistance"])
        res.beaker_diameter = get_float_from_cm_str(parameters["SC_BeakerDiameter"])
        res.beaker_height = get_float_from_cm_str(parameters["SC_BeakerHeight"])
        res.beaker_side_wall_thickness = get_float_from_cm_str(parameters["SC_BeakerSideWallThickness"])
        res.beaker_end_wall_thickness = get_float_from_cm_str(parameters["SC_BeakerEndWallThickness"])
        res.source_height = get_float_from_cm_str(parameters["SC_SourceHeight"])
        return res


class MarinelliDimensions:
    def __init__(self):
        self.distance = 0
        self.beaker_diameter = 0
        self.beaker_height = 0
        self.beaker_side_wall_thickness = 0
        self.beaker_end_wall_thickness = 0
        self.beaker_hole_diameter = 0
        self.beaker_hole_height = 0
        self.beaker_hole_side_wall_thickness = 0
        self.beaker_hole_end_wall_thickness = 0
        self.source_height = 0

    def __repr__(self):
        return ("dimensions:\n" +
                "distance=" + str(self.distance) + '\n' +
                "beaker_diameter=" + str(self.beaker_diameter) + '\n' +
                "beaker_height=" + str(self.beaker_height) + '\n' +
                "beaker_side_wall_thickness=" + str(self.beaker_side_wall_thickness) + '\n' +
                "beaker_end_wall_thickness=" + str(self.beaker_end_wall_thickness) + '\n' +
                "beaker_hole_diameter=" + str(self.beaker_hole_diameter) + '\n' +
                "beaker_hole_height=" + str(self.beaker_hole_height) + '\n' +
                "beaker_hole_side_wall_thickness=" + str(self.beaker_hole_side_wall_thickness) + '\n' +
                "beaker_hole_end_wall_thickness=" + str(self.beaker_hole_end_wall_thickness) + '\n' +
                "source_height=" + str(self.source_height) + '\n'
                )

    @staticmethod
    def parse_from_str(parameters):
        res = MarinelliDimensions()
        res.distance = get_float_from_cm_str(parameters["SM_BeakerToDetectorFrontDistance"])
        res.beaker_diameter = get_float_from_cm_str(parameters["SM_BeakerDiameter"])
        res.beaker_height = get_float_from_cm_str(parameters["SM_BeakerHeight"])
        res.beaker_side_wall_thickness = get_float_from_cm_str(parameters["SM_BeakerSideThickness"])
        res.beaker_end_wall_thickness = get_float_from_cm_str(parameters["SM_BeakerEndWallThickness"])
        res.beaker_hole_diameter = get_float_from_cm_str(parameters["SM_BeakerHoleDiameter"])
        res.beaker_hole_height = get_float_from_cm_str(parameters["SM_BeakerHoleHeight"])
        res.beaker_hole_side_wall_thickness = get_float_from_cm_str(parameters["SM_BeakerHoleSideThickness"])
        res.beaker_hole_end_wall_thickness = get_float_from_cm_str(parameters["SM_BeakerHoleEndWallThickness"])
        res.source_height = get_float_from_cm_str(parameters["SM_SourceHeight"])
        return res


class PointSource:
    def __init__(self):
        self.dimensions = PointDimensions()
        self.source_type = "Point"

    def __repr__(self):
        return "PointSource\n" + str(self.dimensions)

    @staticmethod
    def parse_from_parameters(parameters):
        if "SourceType" not in parameters or parameters["SourceType"] != "POINT":
            return None
        res = PointSource()
        res.dimensions = PointDimensions.parse_from_str(parameters)
        return res


class CylSource:
    def __init__(self):
        self.dimensions = CylinderDimensions()
        self.materials = {}
        self.source_type = "Cylinder"

    def __repr__(self):
        res = '\n'.join(k + str(v) for k, v in self.materials.items())
        res = "CylinderSource\n" + str(self.dimensions) + res
        return res

    def get_radius(self):
        return self.dimensions.beaker_diameter / 2

    def get_source_radius(self):
        return self.dimensions.beaker_diameter / 2 - self.dimensions.beaker_side_wall_thickness

    def get_source_height(self):
        return self.dimensions.source_height

    def get_source_center_from_beaker_bottom(self):
        return self.dimensions.beaker_end_wall_thickness + self.get_source_height() / 2

    @staticmethod
    def parse_from_parameters(parameters):
        if "SourceType" not in parameters or parameters["SourceType"] != "CYLINDER":
            return None
        res = CylSource()
        res.dimensions = CylinderDimensions.parse_from_str(parameters)
        source_type_str = "SC"
        res.materials["Wall"] = Material.parse_material(parameters, "Wall", source_type_str)
        res.materials["Source"] = Material.parse_material(parameters, "Source", source_type_str)
        res.materials["EmptySpace"] = Material.parse_material(parameters, "EmptySpace", source_type_str)
        return res


class MarinelliSource:
    def __init__(self):
        self.dimensions = MarinelliDimensions()
        self.materials = {}
        self.source_type = "Marinelli"

    def __repr__(self):
        res = '\n'.join(k + str(v) for k, v in self.materials.items())
        res = "MarinelliSource\n" + str(self.dimensions) + res
        return res

    @staticmethod
    def parse_from_parameters(parameters):
        if "SourceType" not in parameters or parameters["SourceType"] != "MARINELLI":
            return None
        res = MarinelliSource()
        res.dimensions = MarinelliDimensions.parse_from_str(parameters)
        source_type_str = "SM"
        res.materials["Wall"] = Material.parse_material(parameters, "Wall", source_type_str)
        res.materials["Source"] = Material.parse_material(parameters, "Source", source_type_str)
        res.materials["EmptySpace"] = Material.parse_material(parameters, "EmptySpace", source_type_str)
        return res


def parseSourceFromIn(filename):
    parameters = parseInDoc(filename)
    if "SourceType" not in parameters:
        return None
    if parameters["SourceType"] == "POINT":
        return PointSource.parse_from_parameters(parameters)
    if parameters["SourceType"] == "CYLINDER":
        return CylSource.parse_from_parameters(parameters)
    if parameters["SourceType"] == "MARINELLI":
        return MarinelliSource.parse_from_parameters(parameters)


if __name__ == "__main__":
    source = parseSourceFromIn("mcnp_examples/Point-10cm.sin")
    print(source)
    source = parseSourceFromIn("mcnp_examples/Petri-80ml.sin")
    print(source)
    print()
    source = parseSourceFromIn("mcnp_examples/Marinelli-1l-ppd.sin")
    print(source)