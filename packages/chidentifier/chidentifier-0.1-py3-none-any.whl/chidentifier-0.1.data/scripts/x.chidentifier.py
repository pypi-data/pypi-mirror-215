#!python -u
from chidentifier.chidentifierlib import *
import sys
import os
#------------------------------------------------------------------------------------------
if __name__ == "__main__":
     args=sys.argv[1:]
     if len(args) < 1:
         print("\n\tCHIdentifier: Chirality Identifier\n")
         print("\tUsage (1):")
         print("\t",sys.argv[0]," molecule1.xyz molecule2.xyz\n")
         print("\tUsage (2):")
         print("\t",sys.argv[0]," molecule1.xyz molecule2.xyz TOL\n")
         print("\tTOL: Similarity tolerance criterion (default = 0.95)(0.0 < TOL <= 1.0)\n")
         print("\tMenu of included examples:\n")
         print("\t%s --ex01" %(sys.argv[0]))
         print("\t%s --ex02" %(sys.argv[0]))
         print("\t%s --ex03" %(sys.argv[0]))
         print("\t%s --ex04\n" %(sys.argv[0]))
         exit()
     if len(args) == 2:
         moleculex=sys.argv[1]
         moleculey=sys.argv[2]
         toleranci=float(0.98)
     if len(args) == 3:
         moleculex=sys.argv[1]
         moleculey=sys.argv[2]
         toleranci=float(sys.argv[3])
#------------------------------------------------------------------------------------------
if sys.argv[1] == "--ex01":
    print("\n\tBuild example 1: Biphenyl")
    moleculex="biphenylq045.xyz"
    moleculey="biphenylq135.xyz"
    print("\tGenerating ... %s" %(moleculex))
    exfile=open(moleculex, "w")
    exfile.write(mola)
    exfile.close()
    print("\tGenerating ... %s" %(moleculey))
    exfile=open(moleculey, "w")
    exfile.write(molb)
    exfile.close()
    print("\tNow run: %s %s %s\n" %(sys.argv[0],moleculex,moleculey))
    exit()
if sys.argv[1] == "--ex02":
    print("\n\tBuild example 2: Morphine")
    moleculex="morphine1.xyz"
    moleculey="morphine2.xyz"
    print("\tGenerating ... %s" %(moleculex))
    exfile=open(moleculex, "w")
    exfile.write(molc)
    exfile.close()
    print("\tGenerating ... %s" %(moleculey))
    exfile=open(moleculey, "w")
    exfile.write(mold)
    exfile.close()
    print("\tNow run: %s %s %s\n" %(sys.argv[0],moleculex,moleculey))
    exit()
if sys.argv[1] == "--ex03":
    print("\n\tBuild example 3: Cu15")
    moleculex="Cu15a1.xyz"
    moleculey="Cu15a2.xyz"
    print("\tGenerating ... %s" %(moleculex))
    exfile=open(moleculex, "w")
    exfile.write(mole)
    exfile.close()
    print("\tGenerating ... %s" %(moleculey))
    exfile=open(moleculey, "w")
    exfile.write(molf)
    exfile.close()
    print("\tNow run: %s %s %s\n" %(sys.argv[0],moleculex,moleculey))
    exit()
if sys.argv[1] == "--ex04":
    print("\n\tBuild example 4: PdCu10")
    moleculex="PdCu10a1.xyz"
    moleculey="PdCu10a2.xyz"
    print("\tGenerating ... %s" %(moleculex))
    exfile=open(moleculex, "w")
    exfile.write(molg)
    exfile.close()
    print("\tGenerating ... %s" %(moleculey))
    exfile=open(moleculey, "w")
    exfile.write(molh)
    exfile.close()
    print("\tNow run: %s %s %s\n" %(sys.argv[0],moleculex,moleculey))
    exit()

print("\nCHIdentifier: Chirality Identifier\n")
mol1=readxyzs(moleculex)[0]
mol2=readxyzs(moleculey)[0]
fci=chiral_invariant(mol1)
gci=chiral_invariant(mol2)
print("CI(%s)=%f" % (moleculex,fci))
print("CI(%s)=%f" % (moleculey,gci))
sij=qij(mol1, mol2, toleranci)
if sij >= toleranci:
    print("CCC=%8.6f >= (tol=%8.6f)" %(sij,toleranci))
    print("%s and %s are chiral" %(moleculex,moleculey))
else:
    print("CCC=%8.6f < (tol=%8.6f)" %(sij,toleranci))
    print("%s and %s are not chiral" %(moleculex,moleculey))
print("CHIdentifier FINISH\n")
exit()
