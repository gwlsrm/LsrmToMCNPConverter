"""
    Converts lsrm-detector (e.g. from din-files) to MCNP in-files
"""

import din_parser

def form_mcnp_file(filename, det):
    with open(filename, 'w') as f:
        f.write("COAXIAL\n")
        rho_cryst = det.materials["Crystal"].rho
        f.write(f"1     1 -{rho_cryst} 3 -6 -12 ( 5 : 11 )")
        f.write(f"2     1 -{rho_cryst} 2 -7 -13 ( 12 : 6 : ( -3 11 ))")
        f.write(f"3     1 -{rho_cryst} -11 -5 2 ( 10 : 4 )")
        rho_cr_clad = det.materials["CrystalSideCladding"].rho
        f.write(f"4     1 -{rho_cr_clad} 13 -14 -7  2")
        rho_cr_mount = det.materials["CrystalMounting"].rho
        rho_det_cap = det.materials["DetectorCap"].rho


if __name__ == "__main__":
    detector = din_parser.PPDDetector.parse_from_file("Gem15P4-70_51-TP32799B_UVT_tape4.din")
    print(detector)
    form_mcnp_file("test.in", detector)