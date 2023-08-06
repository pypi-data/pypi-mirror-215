import gmsh
import sys

# generate the mesh
gmsh.initialize()
gdim =2

# 
membrane = gmsh.model.occ.addDisk(0, 0, 0, 1, 1)

gmsh.model.occ.synchronize()
gmsh.model.addPhysicalGroup(gdim, [membrane], 1)
gmsh.option.setNumber("Mesh.CharacteristicLengthMin",0.05)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax",0.05)
gmsh.model.mesh.generate(gdim)

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()
