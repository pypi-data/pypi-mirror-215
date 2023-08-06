#!/usr/bin/env python3 -u
import sys
import os
import numpy as np
from usramp.usramplib import *
#------------------------------------------------------------------------------------------
if __name__ == "__main__":
     args=sys.argv[1:]
     if len(args) < 1:
         print("\n\tUSRAMP: Ultrafast shape-recognition algorithm with eight descriptors\n")
         print("\tUsage (1):")
         print("\t",sys.argv[0]," molecule_list_in.xyz \n")
         print("\tUsage (2):")
         print("\t",sys.argv[0]," molecule_list_in.xyz TOL\n")
         print("\tTOL: Similarity tolerance criterion (default = 0.95)(0.0 < TOL <= 1.0)\n")
         print("\tMenu of included examples:\n")
         print("\t%s --ex01" %(sys.argv[0]))
         print("\t%s --ex02" %(sys.argv[0]))
         print("\t%s --ex03" %(sys.argv[0]))
         print("\t%s --ex04\n" %(sys.argv[0]))
         exit()
     if len(args) == 1:
         moleculex=sys.argv[1]
         tolerance=float(0.95)
     if len(args) == 2:
         moleculex=sys.argv[1]
         tolerance=float(sys.argv[2])
#------------------------------------------------------------------------------------------
if sys.argv[1] == "--ex01":
    print("\n\tBuild example 1: RuCu12.xyz")
    exfile = open("RuCu12.xyz", "w")
    exfile.write(mola)
    exfile.close()
    print("\tNow run: %s RuCu12.xyz\n" %(sys.argv[0]))
    exit()
if sys.argv[1] == "--ex02":
    print("\n\tBuild example 2: ethanol_dihedral.xyz")
    exfile = open("ethanol_dihedral.xyz", "w")
    exfile.write(molb)
    exfile.close()
    print("\tNow run: %s ethanol_dihedral.xyz\n" %(sys.argv[0]))
    exit()
if sys.argv[1] == "--ex03":
    print("\n\tBuild example 3: coenzymeA_randomrot.xyz")
    exfile = open("coenzymeA_randomrot.xyz", "w")
    exfile.write(molc)
    exfile.close()
    print("\tNow run: %s coenzymeA_randomrot.xyz\n" %(sys.argv[0]))
    exit()
if sys.argv[1] == "--ex04":
    print("\n\tBuild example 4: Ag12.xyz")
    exfile = open("Ag12.xyz", "w")
    exfile.write(mold)
    exfile.close()
    print("\tNow run: %s Ag12.xyz\n" %(sys.argv[0]))
    exit()

print("\nUSRAMP: Ultrafast shape-recognition algorithm with eight descriptors\n")
mol00=readxyzs(moleculex)
n00=len(mol00)
print("Before the discrimination we have %d molecules\n" %(n00))
mol01=kick_similar_molecules(mol00, tolerance)
n01=len(mol01)
print("After the discrimination (tol = %1.2f) we have %d molecules" %(tolerance, n01))
if n00==n01: print("ALL MOLECULES ARE DI-SIMILAR, NONE HAS BEEN DISCRIMINATED")
writexyzs(mol01,'molecule_list_out.xyz')
print("Created: molecule_list_out.xyz\n")
print("USRAMP FINISH\n")
exit()
