#!/usr/bin/python3
"""
    Converts lsrm-detector (e.g. from din-files) to MCNP in-files
"""

import sys
import din_parser
import sin_parser
from mcnpinparser import *

SOURCE_DIST = 10
ENERGY = 1
AIR_MAT = [Element(7, 0.7554), Element(8, 0.2316), Element(18, 0.0129)]
AIR_RHO = 0.001

def din_mat_to_mcnp(mat_num, material):
    elements = []
    for e in material.elements:
        elements.append(Element(e.z, e.mf))
    return Material(mat_num, elements)

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

def mcnp_add_hpge_det(mcnp, det):
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
    mcnp.add_material(din_mat_to_mcnp(1, det.materials["Crystal"]))
    mcnp.add_material(din_mat_to_mcnp(2, det.materials["CrystalSideCladding"]))
    mcnp.add_material(din_mat_to_mcnp(3, det.materials["Vacuum"]))
    mcnp.add_material(din_mat_to_mcnp(4, det.materials["CrystalMounting"]))
    mcnp.add_material(din_mat_to_mcnp(5, det.materials["DetectorCap"]))

def mcnp_add_scint_det(mcnp, det):
    # add planes
    thick = det.dimensions.det_mount
    mcnp.add_surface(1, "PZ", thick)
    thick += det.dimensions.crystal_height
    mcnp.add_surface(2, "PZ", thick)
    thick += det.dimensions.crystal_front_reflector
    mcnp.add_surface(3, "PZ", thick)
    thick += det.dimensions.crystal_front_cladding
    mcnp.add_surface(4, "PZ", thick)
    thick += det.dimensions.det_front_pack
    mcnp.add_surface(5, "PZ", thick)
    thick += det.dimensions.det_front_cap
    mcnp.add_surface(6, "PZ", thick)
    # add cylinders
    radius = det.dimensions.crystal_diameter / 2.0
    mcnp.add_surface(7, "CZ", radius)
    radius += det.dimensions.crystal_side_reflector
    mcnp.add_surface(8, "CZ", radius)
    radius += det.dimensions.crystal_side_cladding
    mcnp.add_surface(9, "CZ", radius)
    radius += det.dimensions.det_side_pack
    mcnp.add_surface(10, "CZ", radius)
    radius += det.dimensions.det_side_cap
    mcnp.add_surface(11, "CZ", radius)
    mcnp.add_surface(12, "PZ", 0)
    det.set_top_surf_num(6)
    det.set_cyl_surf_num(11)
    det.set_bottom_surf_num(12)
    # add cells
    rho_cryst = det.materials["Crystal"].rho
    rho_cr_clad = det.materials["CrystalCladding"].rho
    rho_reflector = det.materials["CrystalReflector"].rho
    rho_det_pack = det.materials["DetectorPackaging"].rho
    rho_det_cap = det.materials["DetectorCap"].rho
    mcnp.add_cell(1, 1, rho_cryst, "1 -2 -7")   # Crystal (Sensitive volume (always the first))
    mcnp.add_cell(2, 1, rho_reflector, "1 -3 -8 ( 2 : 7 )")  # Reflector
    mcnp.add_cell(3, 1, rho_cr_clad, "1 -4 -9 ( 3 : 8 )")  # Crystal cladding
    mcnp.add_cell(4, 2, rho_det_pack, "1 -5 -10 ( 4 : 9 )")  # Packaging
    mcnp.add_cell(5, 3, rho_det_cap, "12 -6 -11 ( -1 : 5 : 10 )")  # Cap
    # add materials
    mcnp.add_material(din_mat_to_mcnp(1, det.materials["Crystal"]))
    mcnp.add_material(din_mat_to_mcnp(2, det.materials["CrystalCladding"]))
    mcnp.add_material(din_mat_to_mcnp(3, det.materials["CrystalReflector"]))
    mcnp.add_material(din_mat_to_mcnp(4, det.materials["DetectorPackaging"]))
    mcnp.add_material(din_mat_to_mcnp(5, det.materials["DetectorCap"]))


def mcnp_add_coaxwell_det(mcnp, det):
    # add planes
    thick = det.dimensions.detector_cap_back_thickness
    mcnp.add_surface(1, "PZ", thick)
    thick += det.dimensions.detector_mounting_thickness
    mcnp.add_surface(2, "PZ", thick)
    mcnp.add_surface(3, "PZ", thick + det.dimensions.crystal_back_dl)
    thick += det.dimensions.crystal_height
    mcnp.add_surface(4, "PZ", thick - det.dimensions.crystal_hole_height - det.dimensions.crystal_hole_bottom_dl)
    mcnp.add_surface(5, "PZ", thick - det.dimensions.crystal_hole_height)
    cap_thick = thick + det.dimensions.cap_to_crystal_distance + det.dimensions.detector_cap_front_thickness
    mcnp.add_surface(6, "PZ", cap_thick - det.dimensions.detector_cap_hole_height - det.dimensions.detector_cap_hole_bottom_thickness)
    mcnp.add_surface(7, "PZ", cap_thick - det.dimensions.detector_cap_hole_height)
    mcnp.add_surface(8, "PZ", thick - det.dimensions.crystal_front_dl)
    mcnp.add_surface(9, "PZ", thick)
    mcnp.add_surface(10, "PZ", cap_thick - det.dimensions.detector_cap_front_thickness)
    mcnp.add_surface(11, "PZ", cap_thick)
    # add cylinders
    radius = det.dimensions.detector_cap_hole_diameter / 2.0
    mcnp.add_surface(12, "CZ", radius)
    mcnp.add_surface(13, "CZ", radius + det.dimensions.detector_cap_hole_side_thickness)
    radius = det.dimensions.crystal_hole_diameter / 2.0
    mcnp.add_surface(14, "CZ", radius)
    mcnp.add_surface(15, "CZ", radius + det.dimensions.crystal_hole_side_dl)
    radius = det.dimensions.crystal_diameter / 2.0
    mcnp.add_surface(16, "CZ", radius - det.dimensions.crystal_side_dl)
    mcnp.add_surface(17, "CZ", radius)
    mcnp.add_surface(18, "CZ", radius + det.dimensions.crystal_side_cladding_thickness)
    radius = det.dimensions.detector_cap_diameter / 2.0
    mcnp.add_surface(19, "CZ", radius - det.dimensions.detector_cap_side_thickness)
    mcnp.add_surface(20, "CZ", radius)
    mcnp.add_surface(21, "PZ", 0)
    det.set_top_surf_num(11)
    det.set_cyl_surf_num(20)
    det.set_hole_top_surf_num(7)
    det.set_hole_cyl_surf_num(12)
    det.set_bottom_surf_num(21)
    # add cells
    rho_cryst = det.materials["Crystal"].rho
    rho_cr_clad = det.materials["CrystalSideCladding"].rho
    rho_vacuum = det.materials["Vacuum"].rho
    rho_cr_mount = det.materials["CrystalMounting"].rho
    rho_det_cap = det.materials["DetectorCap"].rho
    mcnp.add_cell(1, 1, rho_cryst, "-16 3 -8 (15 : -4)")
    mcnp.add_cell(2, 1, rho_cryst, "2 -17 -9 (-3 : 16 : (8 15))")  # deadlayer 1
    mcnp.add_cell(3, 1, rho_cryst, "-15 4 -9 (-5 : 14)")  # deadlayer 2
    mcnp.add_cell(4, 2, rho_cr_clad, "2 -9 -18 17")  # crystal cladding
    mcnp.add_cell(5, 3, rho_vacuum, "5 -14 -9 (-6 : 13)")  # hole
    mcnp.add_cell(6, 3, rho_vacuum, "-19 1 -10 (18 : (9 13))")  # vacuum chamber
    mcnp.add_cell(7, 4, rho_cr_mount, "1 -2 -18")  # Detector mounting
    mcnp.add_cell(8, 5, rho_det_cap, "21 -11 -20 (-1 : 19 : (10 13))")  # Detector cap
    mcnp.add_cell(9, 5, rho_det_cap, "6 -13 -11 (-7 : 12)")  # Detector cap hole wall
    # add materials
    mcnp.add_material(din_mat_to_mcnp(1, det.materials["Crystal"]))
    mcnp.add_material(din_mat_to_mcnp(2, det.materials["CrystalSideCladding"]))
    mcnp.add_material(din_mat_to_mcnp(3, det.materials["Vacuum"]))
    mcnp.add_material(din_mat_to_mcnp(4, det.materials["CrystalMounting"]))
    mcnp.add_material(din_mat_to_mcnp(5, det.materials["DetectorCap"]))


def mcnp_add_point_source(mcnp, source, det):
    sn = len(mcnp.surfaces) + 1
    cn = len(mcnp.cells) + 1
    mn = len(mcnp.materials) + 1
    if (det.det_type != "CoaxWell"):
        # surfaces
        mcnp.add_surface(sn, "PZ", det.get_height() + source.dimensions.distance + 0.05)
        # cells
        # air
        mcnp.add_cell(cn, mn, AIR_RHO, "%d -%d -%d" % (det.get_top_surf_num(), det.get_cyl_surf_num(), sn))
        mcnp.add_material(Material(mn, AIR_MAT))
        # universe
        mcnp.add_cell(cn+1, 0, 0, "-%d : %d : %d" % (det.get_bottom_surf_num(), det.get_cyl_surf_num(), sn))
    else:
        # cells
        # air
        mcnp.add_cell(cn, mn, AIR_RHO, "%d -%d -%d" % (det.get_hole_top_surf_num(), det.get_hole_cyl_surf_num(), det.get_top_surf_num()))
        mcnp.add_material(Material(mn, AIR_MAT))
        # universe
        mcnp.add_cell(cn + 1, 0, 0, "-%d : %d : %d" % (det.get_bottom_surf_num(), det.get_top_surf_num(), det.get_cyl_surf_num()))


def mcnp_add_cyl_source(mcnp, source, det):
    # surfaces
    sn = len(mcnp.surfaces)
    height = det.get_height() + source.dimensions.distance
    mcnp.add_surface(sn+1, "PZ", height)
    height += source.dimensions.beaker_end_wall_thickness
    mcnp.add_surface(sn+2, "PZ", height)
    height += source.dimensions.source_height
    mcnp.add_surface(sn+3, "PZ", height)
    height = det.get_height() + source.dimensions.distance + source.dimensions.beaker_height
    mcnp.add_surface(sn+4, "PZ", height - source.dimensions.beaker_side_wall_thickness)
    mcnp.add_surface(sn+5, "PZ", height)
    radius = source.dimensions.beaker_diameter / 2
    mcnp.add_surface(sn+6, "CZ", radius - source.dimensions.beaker_side_wall_thickness)
    mcnp.add_surface(sn+7, "CZ", radius)
    # cells
    cn = len(mcnp.cells)
    mn = len(mcnp.materials)
    rho_wall = source.materials["Wall"].rho
    rho_source = source.materials["Source"].rho
    rho_empty = source.materials["EmptySpace"].rho
    mcnp.add_cell(cn+1, mn+1, rho_source, f"{sn+2} -{sn+6} -{sn+3}") # source
    mcnp.add_cell(cn+2, mn+2, rho_empty, f"{sn+3} -{sn+6} -{sn+4}")  # empty space
    mcnp.add_cell(cn+3, mn+3, rho_wall, f"{sn+1} -{sn+7} -{sn+5} ({sn+4} : {sn+6} : -{sn+2})")  # beaker
    mcnp.add_material(din_mat_to_mcnp(mn+1, source.materials["Source"]))
    mcnp.add_material(din_mat_to_mcnp(mn+2, source.materials["EmptySpace"]))
    mcnp.add_material(din_mat_to_mcnp(mn+3, source.materials["Wall"]))
    # air && universe
    if (radius <= det.get_radius()):
        # air
        mcnp.add_cell(cn+4, mn+4, AIR_RHO,
              f"{det.get_top_surf_num()} -{det.get_cyl_surf_num()} -{sn+5} ({sn+7} : -{sn+1})")
        # universe
        mcnp.add_cell(cn+5, 0, 0,
              f"-{det.get_bottom_surf_num()} : {det.get_cyl_surf_num()} : {sn+5}")
    else:
        # air
        mcnp.add_cell(cn+4, mn+4, AIR_RHO,
              f"{det.get_bottom_surf_num()} -{sn+7} -{sn+1} ({det.get_top_surf_num()} : {det.get_cyl_surf_num()})")
        # universe
        mcnp.add_cell(cn+5, 0, 0,
              f"-{det.get_bottom_surf_num()} : {sn+7} : {sn+5}")
    # air
    mcnp.add_material(Material(mn+4, AIR_MAT))

def mcnp_add_calc_params(mcnp, detector, source):
    energy = 1
    MPS = 10000000
    cell_imp = [1] * (len(mcnp.cells) - 1)
    cell_imp.append(0)
    det_front = detector.get_height()
    if detector.det_type == "CoaxWell":
        det_front -= detector.dimensions.detector_cap_hole_height
    if source.source_type == "Point":
        photon_source = PhotonPointSource(0, 0, det_front + source.dimensions.distance, energy)
    elif source.source_type == "Cylinder":
        photon_source = CylPhotonSource(0, 0, det_front + source.dimensions.distance
                                        + source.get_source_center_from_beaker_bottom(), energy,
                                        source.get_source_radius(), source.get_source_height() / 2)
    else:
        photon_source = None
    mcnp.calc_parameters = CalcParams(cell_imp, photon_source, 1, [1], mcnp.materials, MPS)

def create_mcnp_from_lsrm(mcnp_task, det, source):
    mcnp = McnpTask(mcnp_task)
    if det.det_type == "Coaxial":
        mcnp_add_hpge_det(mcnp, det)
    elif det.det_type == "Scintillator":
        mcnp_add_scint_det(mcnp, det)
    elif det.det_type == "CoaxWell":
        mcnp_add_coaxwell_det(mcnp, det)
    if source.source_type == "Point":
        mcnp_add_point_source(mcnp, source, det)
    elif source.source_type == "Cylinder":
        mcnp_add_cyl_source(mcnp, source, det)
    else:
        pass
    mcnp_add_calc_params(mcnp, det, source)
    return mcnp

def Example():
    # coaxial detector + point
    hpge_detector = din_parser.parseDetFromIn("mcnp_examples/Gem15P4-70_51-TP32799B_UVT_tape4.din")
    point_source = sin_parser.parseSourceFromIn("mcnp_examples/Point-25cm.sin")
    mcnp = create_mcnp_from_lsrm("COA_POI", hpge_detector, point_source)
    mcnp.save_to_file("mcnp_examples/PP")
    # scintillator + point
    scint_detector = din_parser.parseDetFromIn("mcnp_examples/NaI40x40.din")
    mcnp = create_mcnp_from_lsrm("SCINT_POI", scint_detector, point_source)
    mcnp.save_to_file("mcnp_examples/SP")
    # coaxial + cylinder
    cyl_source = sin_parser.parseSourceFromIn("mcnp_examples/Petri-80ml_1.sin")
    mcnp = create_mcnp_from_lsrm("COA_CYL", hpge_detector, cyl_source)
    mcnp.save_to_file("mcnp_examples/PC")
    # coaxial well detector + point
    well_detector = din_parser.parseDetFromIn("mcnp_examples/Well.din")
    point_source = sin_parser.parseSourceFromIn("mcnp_examples/Point-1cm.sin")
    mcnp = create_mcnp_from_lsrm("WELL_POI", well_detector, point_source)
    mcnp.save_to_file("mcnp_examples/WP")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        Example()
        sys.exit()
    din_filename = sys.argv[1]
    sin_filename = sys.argv[2]
    hpge_detector = din_parser.parseDetFromIn(din_filename)
    point_source = sin_parser.parseSourceFromIn(sin_filename)
    mcnp = create_mcnp_from_lsrm("LSRM", hpge_detector, point_source)
    mcnp.save_to_file("INP")

