import numpy as np
#------------------------------------------------------------------------------------------
mola="""
22
45.00000000     Biphenyl_q045
C      0.723400000     -0.000200000     -0.000100000
C     -0.723400000      0.000300000     -0.000100000
C      1.420291301     -0.158450292      1.197697098
C     -1.420600000     -0.958600000      0.734900000
C      1.421408630      0.158050520     -1.197414807
C     -1.421000000      0.958800000     -0.735000000
C      2.815191173     -0.158520775      1.198391522
C     -2.815400000     -0.958800000      0.735000000
C      2.816208512      0.157909337     -1.196791118
C     -2.815900000      0.958600000     -0.734900000
C      3.513099823     -0.000411666      0.000935270
C     -3.513200000     -0.000200000      0.000100000
H      0.891848421     -0.282847569      2.139999916
H     -0.892300000     -1.713000000      1.313100000
H      0.893651571      0.282625417     -2.140046438
H     -0.893100000      1.713400000     -1.313400000
H      3.357950853     -0.281612266      2.130915192
H     -3.358400000     -1.705400000      1.307200000
H      3.359848823      0.281173705     -2.129049305
H     -3.359300000      1.704900000     -1.307000000
H      4.599199740     -0.000450891      0.001412812
H     -4.599200000     -0.000400000      0.000200000
"""
molb="""22
135.00000000     Biphenyl_q135
C      0.723400000     -0.000200000     -0.000100000
C     -0.723400000      0.000300000     -0.000100000
C      1.419931961     -1.198237885     -0.158109444
C     -1.420600000     -0.958600000      0.734900000
C      1.421767637      1.196873529      0.158391736
C     -1.421000000      0.958800000     -0.735000000
C      2.814831451     -1.199414372     -0.157697863
C     -2.815400000     -0.958800000      0.735000000
C      2.816567185      1.195767811      0.158732582
C     -2.815900000      0.958600000     -0.734900000
C      3.513099205     -0.002199363      0.000652427
C     -3.513200000     -0.000200000      0.000100000
H      0.891206484     -2.140358036     -0.282689338
H     -0.892300000     -1.713000000      1.313100000
H      0.894293353      2.139687506      0.282784237
H     -0.893100000      1.713400000     -1.313400000
H      3.357311333     -2.132125574     -0.280601774
H     -3.358400000     -1.705400000      1.307200000
H      3.360487012      2.127838080      0.282184819
H     -3.359300000      1.704900000     -1.307000000
H      4.599198841     -0.003052250      0.000988548
H     -4.599200000     -0.000400000      0.000200000
"""
molc="""40
0.0000000000              Morphine1
C        3.263061000     -0.182134000      0.231371000     
C        3.335445000     -1.580901000     -0.003601000     
C        2.222524000     -2.373932000     -0.347157000     
C        1.983163000      0.387963000      0.164336000     
C        0.933212000     -1.799413000     -0.404607000     
C        0.894046000     -0.451716000     -0.078158000     
O        4.356814000      0.596774000      0.480492000     
H        5.146013000      0.026384000      0.459966000     
O        1.604529000      1.735683000      0.181852000     
C       -0.321322000      0.398173000     -0.074256000     
C        0.320287000      1.693606000     -0.536056000     
C       -1.316544000     -0.072517000     -1.110507000     
C       -1.638775000     -1.543605000     -0.722619000     
C       -0.645232000      2.868877000     -0.452930000     
H        0.578933000      1.568291000     -1.608293000     
C       -2.333443000      1.054265000     -1.218566000     
C       -2.009349000      2.339183000     -0.923266000     
H       -0.801729000     -0.141481000     -2.091441000     
H       -2.774767000      3.116662000     -1.039936000     
H       -3.345325000      0.839152000     -1.586943000     
H        2.382684000     -3.431301000     -0.586380000     
H        4.328056000     -2.048797000      0.035449000     
C       -0.355948000     -2.426069000     -0.938620000     
H       -0.226505000     -2.622161000     -2.022577000     
H       -0.545885000     -3.405768000     -0.465160000     
C       -0.985020000      0.438621000      1.347012000     
C       -3.095669000     -2.654098000      0.895373000     
C       -2.256341000     -0.412254000      1.393616000     
N       -2.051735000     -1.670393000      0.687173000     
H       -2.435665000     -1.933730000     -1.391542000     
H       -1.222414000      1.474382000      1.629931000     
H       -0.254786000      0.044496000      2.072984000     
H       -2.500994000     -0.650328000      2.444151000     
H       -3.123103000      0.166111000      0.992159000     
H       -2.802215000     -3.618784000      0.443975000     
H       -4.081775000     -2.360077000      0.456456000     
H       -3.242469000     -2.819945000      1.977259000     
O       -0.772184000      3.442837000      0.851409000     
H        0.138195000      3.519948000      1.196816000     
H       -0.331941000      3.663064000     -1.165300000     
"""
mold="""40
0.0000000000              Morphine2
C       -3.263060000     -0.182132000      0.231372000     
C       -3.335445000     -1.580899000     -0.003601000     
C       -2.222524000     -2.373930000     -0.347159000     
C       -1.983162000      0.387964000      0.164335000     
C       -0.933213000     -1.799412000     -0.404609000     
C       -0.894046000     -0.451715000     -0.078159000     
O       -4.356813000      0.596777000      0.480493000     
H       -5.146013000      0.026387000      0.459968000     
O       -1.604527000      1.735684000      0.181852000     
C        0.321322000      0.398174000     -0.074256000     
C       -0.320285000      1.693607000     -0.536056000     
C        1.316545000     -0.072518000     -1.110507000     
C        1.638774000     -1.543606000     -0.722620000     
C        0.645235000      2.868877000     -0.452930000     
H       -0.578932000      1.568292000     -1.608293000     
C        2.333445000      1.054264000     -1.218565000     
C        2.009352000      2.339182000     -0.923265000     
H        0.801730000     -0.141481000     -2.091441000     
H        2.774770000      3.116660000     -1.039934000     
H        3.345327000      0.839150000     -1.586941000     
H       -2.382685000     -3.431298000     -0.586382000     
H       -4.328057000     -2.048794000      0.035449000     
C        0.355947000     -2.426068000     -0.938623000     
H        0.226504000     -2.622157000     -2.022581000     
H        0.545882000     -3.405768000     -0.465166000     
C        0.985020000      0.438621000      1.347012000     
C        3.095661000     -2.654104000      0.895376000     
C        2.256339000     -0.412257000      1.393617000     
N        2.051731000     -1.670395000      0.687173000     
H        2.435665000     -1.933731000     -1.391541000     
H        1.222417000      1.474382000      1.629930000     
H        0.254785000      0.044499000      2.072984000     
H        2.500991000     -0.650331000      2.444152000     
H        3.123103000      0.166106000      0.992161000     
H        2.802204000     -3.618789000      0.443977000     
H        4.081769000     -2.360086000      0.456461000     
H        3.242458000     -2.819952000      1.977262000     
O        0.772187000      3.442837000      0.851409000     
H       -0.138193000      3.519948000      1.196816000     
H        0.331945000      3.663064000     -1.165300000
"""
mole="""15  
-1847014.281852698      Cu15a1
Cu     2.8064550000    -1.6867130000    -0.2708790000
Cu     0.5080580000    -2.9970530000    -0.4404440000
Cu     0.6706670000    -0.8309580000     0.6368850000
Cu     0.7171180000     1.5453570000     1.2910690000
Cu    -1.3633760000    -2.2285110000     1.1863460000
Cu    -3.4403770000    -1.0836510000     0.3784920000
Cu    -1.5175250000     0.3455680000     1.1452380000
Cu    -2.7370470000     1.0175700000    -0.9019520000
Cu    -1.3409150000    -1.1171850000    -1.0061890000
Cu     1.0372150000    -0.9066200000    -1.8720100000
Cu    -0.1966420000     1.1223480000    -1.0698410000
Cu    -1.2971960000     2.7969460000     0.3568040000
Cu     1.1397330000     3.1793850000    -0.5396070000
Cu     2.2865530000     0.8722630000    -0.5971110000
Cu     2.7272780000    -0.0287460000     1.7031960000
"""
molf="""15
-1847014.281852698      Cu15a2
Cu    -2.8064550000    -1.6867130000    -0.2708790000
Cu    -0.5080580000    -2.9970530000    -0.4404440000
Cu    -0.6706670000    -0.8309580000     0.6368850000
Cu    -0.7171180000     1.5453570000     1.2910690000
Cu     1.3633760000    -2.2285110000     1.1863460000
Cu     3.4403770000    -1.0836510000     0.3784920000
Cu     1.5175250000     0.3455680000     1.1452380000
Cu     2.7370470000     1.0175700000    -0.9019520000
Cu     1.3409150000    -1.1171850000    -1.0061890000
Cu    -1.0372150000    -0.9066200000    -1.8720100000
Cu     0.1966420000     1.1223480000    -1.0698410000
Cu     1.2971960000     2.7969460000     0.3568040000
Cu    -1.1397330000     3.1793850000    -0.5396070000
Cu    -2.2865530000     0.8722630000    -0.5971110000
Cu    -2.7272780000    -0.0287460000     1.7031960000
"""
molg="""11
0.00000000               PdCu10a1
Pd     10.734321472     -6.655802903     -0.629154798
Cu     13.324476692     -9.868006398     -1.288827354
Cu     12.753084804     -9.801193444      1.099500999
Cu      9.025627350    -10.585759566     -0.663180998
Cu     11.232909043     -7.921375237      1.525356159
Cu      9.043683216     -8.380536896      0.309397313
Cu     11.022994785     -9.126131523     -0.909975568
Cu     13.001049973     -7.698398513     -0.236031717
Cu     10.372829739    -10.195215269      1.361451119
Cu     14.980361824     -8.948583701      0.333363441
Cu     11.525258546    -11.400608396     -0.477412667
"""
molh="""11
0.00000000               PdCu10a2
Pd     23.765678528     -6.655802903     -0.629154798
Cu     21.175523308     -9.868006398     -1.288827354
Cu     21.746915196     -9.801193444      1.099500999
Cu     25.474372650    -10.585759566     -0.663180998
Cu     23.267090957     -7.921375237      1.525356159
Cu     25.456316784     -8.380536896      0.309397313
Cu     23.477005215     -9.126131523     -0.909975568
Cu     21.498950027     -7.698398513     -0.236031717
Cu     24.127170261    -10.195215269      1.361451119
Cu     19.519638176     -8.948583701      0.333363441
Cu     22.974741454    -11.400608396     -0.477412667
"""
#------------------------------------------------------------------------------------------
def is_number(s):
    try:
        float(s).is_integer()
        return True
    except ValueError:
        pass
#------------------------------------------------------------------------------------------
def get_chemical_symbol(sym):
    chemical_symbol={}
    chemical_symbol[1] ="H"
    chemical_symbol[2] ="He"
    chemical_symbol[3] ="Li"
    chemical_symbol[4] ="Be"
    chemical_symbol[5] ="B"
    chemical_symbol[6] ="C"
    chemical_symbol[7] ="N"
    chemical_symbol[8] ="O"
    chemical_symbol[9] ="F"
    chemical_symbol[10]="Ne"
    chemical_symbol[11]="Na"
    chemical_symbol[12]="Mg"
    chemical_symbol[13]="Al"
    chemical_symbol[14]="Si"
    chemical_symbol[15]="P"
    chemical_symbol[16]="S"
    chemical_symbol[17]="Cl"
    chemical_symbol[18]="Ar"
    chemical_symbol[19]="K"
    chemical_symbol[20]="Ca"
    chemical_symbol[21]="Sc"
    chemical_symbol[22]="Ti"
    chemical_symbol[23]="V"
    chemical_symbol[24]="Cr"
    chemical_symbol[25]="Mn"
    chemical_symbol[26]="Fe"
    chemical_symbol[27]="Co"
    chemical_symbol[28]="Ni"
    chemical_symbol[29]="Cu"
    chemical_symbol[30]="Zn"
    chemical_symbol[31]="Ga"
    chemical_symbol[32]="Ge"
    chemical_symbol[33]="As"
    chemical_symbol[34]="Se"
    chemical_symbol[35]="Br"
    chemical_symbol[36]="Kr"
    chemical_symbol[37]="Rb"
    chemical_symbol[38]="Sr"
    chemical_symbol[39]="Y"
    chemical_symbol[40]="Zr"
    chemical_symbol[41]="Nb"
    chemical_symbol[42]="Mo"
    chemical_symbol[43]="Tc"
    chemical_symbol[44]="Ru"
    chemical_symbol[45]="Rh"
    chemical_symbol[46]="Pd"
    chemical_symbol[47]="Ag"
    chemical_symbol[48]="Cd"
    chemical_symbol[49]="In"
    chemical_symbol[50]="Sn"
    chemical_symbol[51]="Sb"
    chemical_symbol[52]="Te"
    chemical_symbol[53]="I"
    chemical_symbol[54]="Xe"
    chemical_symbol[55]="Cs"
    chemical_symbol[56]="Ba"
    chemical_symbol[57]="La"
    chemical_symbol[58]="Ce"
    chemical_symbol[59]="Pr"
    chemical_symbol[60]="Nd"
    chemical_symbol[61]="Pm"
    chemical_symbol[62]="Sm"
    chemical_symbol[63]="Eu"
    chemical_symbol[64]="Gd"
    chemical_symbol[65]="Tb"
    chemical_symbol[66]="Dy"
    chemical_symbol[67]="Ho"
    chemical_symbol[68]="Er"
    chemical_symbol[69]="Tm"
    chemical_symbol[70]="Yb"
    chemical_symbol[71]="Lu"
    chemical_symbol[72]="Hf"
    chemical_symbol[73]="Ta"
    chemical_symbol[74]="W"
    chemical_symbol[75]="Re"
    chemical_symbol[76]="Os"
    chemical_symbol[77]="Ir"
    chemical_symbol[78]="Pt"
    chemical_symbol[79]="Au"
    chemical_symbol[80]="Hg"
    chemical_symbol[81]="Tl"
    chemical_symbol[82]="Pb"
    chemical_symbol[83]="Bi"
    chemical_symbol[84]="Po"
    chemical_symbol[85]="At"
    chemical_symbol[86]="Rn"
    sym1 = chemical_symbol[int(sym)] if is_number(sym) else sym
    return sym1
#------------------------------------------------------------------------------------------
class Atom:
    def __init__(self, symbol, xcartesian, ycartesian, zcartesian):
        self.s=symbol
        self.xc=xcartesian
        self.yc=ycartesian
        self.zc=zcartesian
#------------------------------------------------------------------------------------------
class Molecule:
    def __init__(self, name, energy, matrix=[], comments=[]):
        self.atoms = []
        self.i = name
        self.e = energy
        self.n = 0
    def add_atom(self, atom):
        self.atoms.append(atom)
        natoms=len(self.atoms)
        self.n = natoms
    def clear(self):
        delattr(self, 'i')
        delattr(self, 'e')
        delattr(self, 'n')
        delattr(self, 'atoms')
#------------------------------------------------------------------------------------------
def readxyzs(filename):
    if not os.path.isfile(filename):
        print("The file",filename,"does not exist.")
        exit()
    file=open(filename,'r')
    imol=-1
    moleculeout=[]
    for line in file:
        ls=line.split()
        if len(ls)==1:
            natoms=int(ls[0])
            count=0
            imol=imol+1
            line=file.readline()
            ls=line.split()
            if len(ls)==0: name,energy='unknown', float(0.0)
            if len(ls)==1: name,energy=str(ls[0]),float(0.0)
            if len(ls)==2: name,energy=str(ls[1]),float(ls[0])
            mol=Molecule(name,energy)
        if len(ls)==4:
            s=get_chemical_symbol(ls[0])
            xc,yc,zc=float(ls[1]),float(ls[2]),float(ls[3])
            ai=Atom(s,xc,yc,zc)
            mol.add_atom(ai)
            count=count+1
            if count==natoms: moleculeout.extend([mol])
    file.close()
    return moleculeout
#------------------------------------------------------------------------------------------
def writexyzs(moleculein,filename):
    fh=open(filename,"w")
    for xmol in moleculein:
        print(xmol.n, file=fh)
        print("%12.8f     %s" %(xmol.e, xmol.i), file=fh)
        for iatom in xmol.atoms:
            print("%s %16.9f %16.9f %16.9f" %(iatom.s, iatom.xc, iatom.yc, iatom.zc), file=fh)
    fh.close()
#------------------------------------------------------------------------------------------
def chiral_invariant(moleculein):
    x=list([imol.xc for imol in moleculein.atoms])
    y=list([imol.yc for imol in moleculein.atoms])
    z=list([imol.zc for imol in moleculein.atoms])
    xavg=np.mean(x)
    yavg=np.mean(y)
    zavg=np.mean(z)
    x1 = x - xavg
    y1 = y - yavg
    z1 = z - zavg
    x2=np.power(x1, 2)
    y2=np.power(y1, 2)
    z2=np.power(z1, 2)
    x3=np.power(x1, 3)
    y3=np.power(y1, 3)
    z3=np.power(z1, 3)
    x4=np.power(x1, 4)
    y4=np.power(y1, 4)
    z4=np.power(z1, 4)
    ilist=range(moleculein.n)
    cm002=sum([z2[i] for i in ilist])
    cm020=sum([y2[i] for i in ilist])
    cm200=sum([x2[i] for i in ilist])
    a1=cm002-cm020
    a2=cm020-cm200
    a3=cm200-cm002
    cm021=sum([y2[i]*z1[i] for i in ilist])
    cm201=sum([x2[i]*z1[i] for i in ilist])
    cm210=sum([x2[i]*y1[i] for i in ilist])
    cm012=sum([y1[i]*z2[i] for i in ilist])
    cm102=sum([x1[i]*z2[i] for i in ilist])
    cm120=sum([x1[i]*y2[i] for i in ilist])
    cm003=sum([z3[i] for i in ilist])
    cm030=sum([y3[i] for i in ilist])
    cm300=sum([x3[i] for i in ilist])
    b01=cm021-cm201
    b02=cm102-cm120
    b03=cm210-cm012
    b04=cm003-cm201-2.0*cm021
    b05=cm030-cm012-2.0*cm210
    b06=cm300-cm120-2.0*cm102
    b07=cm021-cm003+2.0*cm201
    b08=cm102-cm300+2.0*cm120
    b09=cm210-cm030+2.0*cm012
    b10=cm021+cm201-3.0*cm003
    b11=cm012+cm210-3.0*cm030
    b12=cm102+cm120-3.0*cm300
    b13=cm021+cm003+3.0*cm201
    b14=cm102+cm300+3.0*cm120
    b15=cm210+cm030+3.0*cm012
    b16=cm012+cm030+3.0*cm210
    b17=cm201+cm003+3.0*cm021
    b18=cm120+cm300+3.0*cm102
    cm022=sum([y2[i]*z2[i] for i in ilist])
    cm202=sum([x2[i]*z2[i] for i in ilist])
    cm220=sum([x2[i]*y2[i] for i in ilist])
    cm400=sum([x4[i] for i in ilist])
    cm040=sum([y4[i] for i in ilist])
    cm004=sum([z4[i] for i in ilist])
    cm112=sum([x1[i]*y1[i]*z2[i] for i in ilist])
    cm121=sum([x1[i]*y2[i]*z1[i] for i in ilist])
    cm211=sum([x2[i]*y1[i]*z1[i] for i in ilist])
    cm130=sum([x1[i]*y3[i] for i in ilist])
    cm103=sum([x1[i]*z3[i] for i in ilist])
    cm013=sum([y1[i]*z3[i] for i in ilist])
    cm310=sum([x3[i]*y1[i] for i in ilist])
    cm301=sum([x3[i]*z1[i] for i in ilist])
    cm031=sum([y3[i]*z1[i] for i in ilist])
    g1=cm022-cm400
    g2=cm202-cm040
    g3=cm220-cm004
    g4=cm112+cm130+cm310
    g5=cm121+cm103+cm301
    g6=cm211+cm013+cm031
    g7=cm022-cm220+cm004-cm400
    g8=cm202-cm022+cm400-cm040
    g9=cm220-cm202+cm040-cm004
    cm011=sum([y1[i]*z1[i] for i in ilist])
    cm101=sum([x1[i]*z1[i] for i in ilist])
    cm110=sum([x1[i]*y1[i] for i in ilist])
    cm111=sum([x1[i]*y1[i]*z1[i] for i in ilist])
    f01=cm110*(cm021*(3.0*g2-2.0*g3-g1)\
       -cm201*(3.0*g1-2.0*g3-g2)+b12*g5-b11*g6+cm003*g8)
    f02=cm101*(cm210*(3.0*g1-2.0*g2-g3)\
       -cm012*(3.0*g3-2.0*g2-g1)+b10*g6-b12*g4-cm030*g7)
    f03=cm011*(cm102*(3.0*g3-2.0*g1-g2)\
       -cm120*(3.0*g2-2.0*g1-g3)+b11*g4-b10*g5+cm300*g9)
    f04=cm002*(b18*g6-b15*g5-2.0*(cm111*g8+b01*g4))
    f05=cm020*(b17*g4-b14*g6-2.0*(cm111*g7+b03*g5))
    f06=cm200*(b16*g5-b13*g4-2.0*(cm111*g9+b02*g6))
    f00=cm011*a2*a3*b02+cm101*a1*a2*b03\
       +cm110*a1*a3*b01-cm111*a1*a2*a3
    f07=cm011*cm011*(cm111*a1-cm011*b02-cm101*b05-cm110*b07)
    f08=cm101*cm101*(cm111*a3-cm101*b03-cm110*b04-cm011*b08)
    f09=cm110*cm110*(cm111*a2-cm110*b01-cm011*b06-cm101*b09)
    f10=cm011*cm101*(cm002*b01+cm020*b04+cm200*b07)
    f11=cm011*cm110*(cm020*b03+cm200*b05+cm002*b09)
    f12=cm101*cm110*(cm200*b02+cm002*b06+cm020*b08)
    cm000=float(moleculein.n)
    rgyr=np.sqrt((cm200+cm020+cm002)/(3.0*cm000))
    s1=1.0/(cm000*rgyr*rgyr*rgyr)
    s3=s1*s1*s1
    s4=s3/cm000
    ci=4.0*s3*(f01+f02+f03+f04+f05+f06)-16.0*s4*(f00-f07-f08-f09+f10+f11+f12)
    return ci
#------------------------------------------------------------------------------------------
def chiral_recognition(moleculeina, moleculeinb):
    citol=float(0.1)
    ci1=chiral_invariant(moleculeina)
    ci2=chiral_invariant(moleculeinb)
    s1=np.sign(ci1)
    s2=np.sign(ci2)
    if s1*s2 < 0.0:
        lista=np.array([np.abs(ci1),np.abs(ci2)])
        lista=np.sort(lista)
        erp=(lista[1]-lista[0])*100.0/lista[0]
        ans = 1 if (erp < citol) else 0
    else:
        ans=0
    return ans
#------------------------------------------------------------------------------------------
def qij(moleculeina, moleculeinb, tol=0.98):
    ci1=chiral_invariant(moleculeina)
    ci2=chiral_invariant(moleculeinb)
    s1=np.sign(ci1)
    s2=np.sign(ci2)
    if s1*s2 < 0.0:
        var=np.abs(ci1+ci2)
        sij=1.0/(1.0+var)
    else:
        sij=0
    return sij
#------------------------------------------------------------------------------------------
