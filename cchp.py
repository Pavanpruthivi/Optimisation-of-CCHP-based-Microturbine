import random
import math
import pandas as pd

ka = 0.025 # thermal conductivity of air
kg = 0.038 # thermal conductiviy of flue gas
ma = 0.1 # mass flow rate of air
mf = 0.01 #mass flow rate of fuel
mg = mf + ma # total mass of gas
Cpa = 1.006 # specific capacity of air
Cpg = 1.068 # specific heat capacity of gas
eff_cc = 0.89 
LHFv = 35.8e3#calorific value of fuel
com_gt = 3.5 # compression ratio of natural gas
eff_cc = 0.89 # effectiveness of combustion
eff_e = 0.45 #Power generation efficiency
eff_c = 0.9 #Transmission efficiency
eff_mc = 0.83778 # efficiency of microturbine
COPe = 3.5 #Co efficient of performance of Absorption chiler
Ex_ng = 51702 # Exergy of Natural gas
w1 = 0.5  #weight of pesr ratio
w2 = 0.5 #weight of exergy efficiency

def Max(E,T1,com,eff_ac):

    T2 = T1*(1+ com_gt**(1 - (1/ka))-1)/eff_ac #temperature after compression
    T3 = (ma*Cpa*T2 + eff_cc*mf*LHFv)/(mg*Cpg) # temperature after combustion
    T4 = T3*(1 - (1-com_gt**(-1+(1/kg))/eff_mc)) #exhaust gas temperature
    Wac = ma*Cpa*(T2 - T1) # work done by air compressor
    Wgt = mg*Cpg*(T3 - T4) #work done by micro_turbine
    Qc = mg*Cpg*7 # cooling energy supplied
    Ex_cooling = -(7-math.log(7)*T1)*(Cpg*mg) # exergy gained in cooling process

    eff_cchp = (Wgt - Wac + Qc)/(mf*LHFv)
    PEC_cchp = E/eff_cchp
    PEC_sp = E/(eff_e*eff_c) + Qc/(COPe*eff_e*eff_c)
    return w1*(1- (PEC_cchp/PEC_sp)) + w2*(E + Ex_cooling)/(Ex_ng*mf) - 1
"""
def fitness(E,T1,com,eff_ac):
    ans= Max(E,T1,com,eff_ac)
    
    if ans==0:
        return 9999
    else:
        return abs(1/ans)
    
#generating random solutions

solutions= []

for s in range(100): #initial popultion
    solutions.append((random.uniform(0,30),random.uniform(298,308),random.uniform(0,2),
                      random.uniform(0,0.9)))
    

for i in range(100): #Generating newer genarations
    rankedsolutions =[]
    for s in solutions:
        rankedsolutions.append((fitness(s[0],s[1],s[2],s[3]),s))
    rankedsolutions.sort()
    rankedsolutions.reverse()
        
    print(f"===Gen {i} best solutions ===")
    print(rankedsolutions[0])
    
    
    if rankedsolutions[0][0] >999:
        break
    
    bestsolutions = rankedsolutions[:50]
    
    elements1 = list()
    elements2 = list()
    elements3 = list()
    elements4 = list()
    
    for s in bestsolutions: # cross over
        elements1.append(s[1][0])
        elements2.append(s[1][1])
        elements3.append(s[1][2])
        elements4.append(s[1][3])
        
    newGen =[]

    for _ in range(1000): #mutation
        e1 = random.choice(elements1) * random.uniform(0.99,1.01) #variation of 1%
        if e1 > 30:
            e1 =30
        e2 = random.choice(elements2) * random.uniform(0.99,1.01)
        if e2 > 308:
            e2 = 308
        e3 = random.choice(elements3) * random.uniform(0.99,1.01)
        if e3>2:
            e3 = 2
        e4 = random.choice(elements4) * random.uniform(0.99,1.01)
        if e4>0.9:
            e4 = 0.9
    
        newGen.append((e1,e2,e3,e4))
    
    solutions= newGen
"""