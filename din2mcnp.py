"""
    Converts lsrm-detector (e.g. from din-files) to MCNP in-files
"""

import din_parser
import sin_parser
from mcnpinparser import *

SOURCE_DIST = 10
ENERGY = 1
AIR_MAT = [Element(7, 0.755), Element(8, 0.2315), Element(18, 0.0129)]
AIR_RHO = 0.001

def write_det_layers_to_file(f, det):
    rho_cryst = det.materials["Crystal"].rho
    rho_cr_clad = det.materials["CrystalSideCladding"].rho
    rho_vacuum = det.materials["Vacuum"].rho
    rho_cr_mount = det.materials["CrystalMounting"].rho
    rho_det_cap = det.materials["DetectorCap"].rho
    f.write(f"1     1 -{rho_cryst} 3 -6 -12 ( 5 : 11 )\n")  # crystal
    f.write(f"2     1 -{rho_cryst} 2 -7 -13 ( 12 : 6 : ( -3 11 ))\n")  # deadlayer 1
    f.write(f"3     1 -{rho_cryst} -11 -5 2 ( 10 : 4 )\n")  # deadlayer 2
    f.write(f"4     2 -{rho_cr_clad} 13 -14 -7  2\n")  # crystal cladding
    f.write(f"5     3 -{rho_vacuum} -4 -10  2\n")  # hole
    f.write(f"6     3 -{rho_vacuum} 1 -8 -15 ( 14 : 7 )\n")  # vacuum chamber
    f.write(f"7     4 -{rho_cr_mount} 1 -2 -14\n")  # Detector mounting
    f.write(f"8     5 -{rho_det_cap} 18 -16 -9 ( -1 : 15 : 8 )\n")  # Detector cap

def write_det_surf_to_file(f, det):
    thick = det.dimensions.detector_cap_back_thickness
    f.write("1     PZ %g\n" % (thick))
    thick += det.dimensions.detector_mounting_thickness
    f.write("2     PZ %g\n" % (thick))
    f.write("3     PZ %g\n" % (thick + det.dimensions.crystal_back_dl))
    f.write("4     PZ %g\n" % (thick + det.dimensions.crystal_hole_height))
    f.write("5     PZ %g\n" % (thick + det.dimensions.crystal_hole_height + det.dimensions.crystal_hole_bottom_dl))
    thick += det.dimensions.crystal_height
    f.write("6     PZ %g\n" % (thick - det.dimensions.crystal_front_dl))
    f.write("7     PZ %g\n" % (thick))
    thick += det.dimensions.cap_to_crystal_distance
    f.write("8     PZ %g\n" % (thick))
    thick += det.dimensions.detector_cap_front_thickness
    f.write("9     PZ %g\n" % (thick))
    radius = det.dimensions.crystal_hole_diameter / 2.0
    f.write("10    CZ %g\n" % (radius))
    f.write("11    CZ %g\n" % (radius + det.dimensions.crystal_hole_side_dl))
    radius = det.dimensions.crystal_diameter / 2.0
    f.write("12    CZ %g\n" % (radius - det.dimensions.crystal_side_dl))
    f.write("13    CZ %g\n" % (radius))
    f.write("14    CZ %g\n" % (radius + det.dimensions.crystal_side_cladding_thickness))
    radius = det.dimensions.detector_cap_diameter / 2.0
    f.write("15    CZ %g\n" % (radius - det.dimensions.detector_cap_side_thickness))
    f.write("16    CZ %g\n" % (radius))
    return thick

def form_mcnp_file(filename, det):
    with open(filename, 'w') as f:
        f.write("COAXIAL\n")

        # layers
        # detector
        write_det_layers_to_file(f, det)

        # source
        f.write("9     6 -0.001 9 -16 -17\n")                                # air between detector and source
        #universe
        f.write("10    0      -18 : 16 : 17\n")                              # universe
        f.write("\n")

        # surfaces
        # detector
        thick = write_det_surf_to_file(f, det)

        #sources
        f.write("17    PZ %g\n" % (thick + SOURCE_DIST + 0.05))
        f.write("18    PZ 0\n")
        f.write("\n")

        # calculation parameters
        f.write("MODE  P\n")
        f.write("IMP:P 1 1 1 1 1 1 1 1 1 0\n")
        f.write("SDEF  POS=0 0 %g ERG=%g PAR=2\n" % (thick + SOURCE_DIST, ENERGY))
        f.write("F8:P  1\n")
        f.write("E0    0 %g %g\n" % (ENERGY - 0.001, ENERGY + 0.001))

        # materials
        # detector
        f.write("M1    32000 1\n")  # crystal
        f.write("M2    13000 1\n")  # crystal cladding
        f.write("M3    7000 1\n")   # vacuum
        f.write("M4    13000 1\n")  # crystal mounting
        f.write("M5    13000 1\n")  # detector cap

        # source
        f.write("M6    7000 1\n")  # air

        # history number (counts)
        f.write("NPS   100000\n")

def mcnp_add_det(mcnp, det):
    # add planes
    thick = det.dimensions.detector_cap_back_thickness
    mcnp.add_surface(1, "PZ", thick)
    thick += det.dimensions.detector_mounting_thickness
    mcnp.add_surface(2, "PZ", thick)
    mcnp.add_surface(3, "PZ", thick + det.dimensions.crystal_back_dl)
    mcnp.add_surface(4, "PZ", thick + det.dimensions.crystal_hole_height)
    mcnp.add_surface(5, "PZ", thick + det.dimensions.crystal_hole_height + det.dimensions.crystal_hole_bottom_dl)
    thick += det.dimensions.crystal_height
    mcnp.add_surface(6, "PZ", thick - det.dimensions.crystal_front_dl)
    mcnp.add_surface(7, "PZ", thick)
    thick += det.dimensions.cap_to_crystal_distance
    mcnp.add_surface(8, "PZ", thick)
    thick += det.dimensions.detector_cap_front_thickness
    mcnp.add_surface(9, "PZ", thick)
    # add cylinders
    radius = det.dimensions.crystal_hole_diameter / 2.0
    mcnp.add_surface(10, "CZ", radius)
    mcnp.add_surface(11, "CZ", radius + det.dimensions.crystal_hole_side_dl)
    radius = det.dimensions.crystal_diameter / 2.0
    mcnp.add_surface(12, "CZ", radius - det.dimensions.crystal_side_dl)
    mcnp.add_surface(13, "CZ", radius)
    mcnp.add_surface(14, "CZ", radius + det.dimensions.crystal_side_cladding_thickness)
    radius = det.dimensions.detector_cap_diameter / 2.0
    mcnp.add_surface(15, "CZ", radius - det.dimensions.detector_cap_side_thickness)
    mcnp.add_surface(16, "CZ", radius)
    mcnp.add_surface(17, "PZ", 0)
    det.set_top_surf_num(9)
    det.set_cyl_surf_num(16)
    det.set_bottom_surf_num(17)
    # add cells
    rho_cryst = det.materials["Crystal"].rho
    rho_cr_clad = det.materials["CrystalSideCladding"].rho
    rho_vacuum = det.materials["Vacuum"].rho
    rho_cr_mount = det.materials["CrystalMounting"].rho
    rho_det_cap = det.materials["DetectorCap"].rho
    mcnp.add_cell(1, 1, rho_cryst, "3 -6 -12 ( 5 : 11 )")
    mcnp.add_cell(2, 1, rho_cryst, "2 -7 -13 ( 12 : 6 : ( -3 11 ))")  # deadlayer 1
    mcnp.add_cell(3, 1, rho_cryst, "-11 -5 2 ( 10 : 4 )")  # deadlayer 2
    mcnp.add_cell(4, 2, rho_cr_clad, "13 -14 -7  2")  # crystal cladding
    mcnp.add_cell(5, 3, rho_vacuum, "-4 -10  2")  # hole
    mcnp.add_cell(6, 3, rho_vacuum, "1 -8 -15 ( 14 : 7 )")  # vacuum chamber
    mcnp.add_cell(7, 4, rho_cr_mount, "1 -2 -14")  # Detector mounting
    mcnp.add_cell(8, 5, rho_det_cap, "17 -16 -9 ( -1 : 15 : 8 )")  # Detector cap
    # add materials
    mcnp.add_material(1, det.materials["Crystal"].elements)
    mcnp.add_material(2, det.materials["CrystalSideCladding"].elements)
    mcnp.add_material(3, det.materials["Vacuum"].elements)
    mcnp.add_material(4, det.materials["CrystalMounting"].elements)
    mcnp.add_material(5, det.materials["DetectorCap"].elements)


def mcnp_add_source(mcnp, source, det):
    # surfaces
    sn = len(mcnp.surfaces)+1
    mcnp.add_surface(sn, "PZ", det.get_height() + source.dimensions.distance + 0.05)
    # cells
    cn = len(mcnp.cells)+1
    mn = len(mcnp.materials)+1
    # air
    mcnp.add_cell(cn, mn, AIR_RHO, "%d -%d -%d" % (det.get_top_surf_num(), det.get_cyl_surf_num(), sn))
    mcnp.materials.append(Material(mn, AIR_MAT))
    # universe
    mcnp.add_cell(cn+1, 0, 0, "-%d : %d : %d" % (det.get_bottom_surf_num(), det.get_cyl_surf_num(), sn))


if __name__ == "__main__":
    detector = din_parser.PPDDetector.parse_from_file("mcnp_examples/Gem15P4-70_51-TP32799B_UVT_tape4.din")
    source = sin_parser.PointSource.parse_from_file("mcnp_examples/Point-10cm.sin")
    print(detector)
    form_mcnp_file("mcnp_examples/PPD_in", detector)
    mcnp = McnpTask("COAXIAL")
    mcnp_add_det(mcnp, detector)
    mcnp_add_source(mcnp, source, detector)
    cell_imp = [1] * (len(mcnp.cells)-1)
    cell_imp.append(0)
    mcnp.calc_parameters = CalcParams(cell_imp,
                                      PhotonSource(0, 0, detector.get_height() + source.dimensions.distance, 1),
                                      1, [1], mcnp.materials, 100000)

    mcnp.save_to_file("mcnp_examples/PPD_test")
