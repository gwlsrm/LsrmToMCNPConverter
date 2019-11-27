import mcnpinparser

infile = mcnpinparser.infile("Am01")
print("test")
print("header: ",  infile.header)
print("cells (%i):" % (len(infile.cells)))
for c in infile.cells:
    print("\t", c)
print("surfaces (%i):" % (len(infile.surfaces)))
for s in infile.surfaces:
    print("\t", s)
print("datalines (%i):" % (len(infile.datacards)))
for k, d in infile.datacards.items():
    print("\t", k, "  ", d)
