import math

#Optimised parameters
Do = 0.1 # Outer diameter
lm = 0.2 # Ratio of Inner diameter to outer diameter
Dstrand = 0.1e-3 # Diameter of wire strand

rho_steam = 1.295 # density of air
vis = 22.97e-6 # viscosity of air
Ro = Do/2
Rsh = Ro/6
P = 6 #No of poles 3 phase synchronous ac generator
f = 50 # frequency in India
Nm = 120*f/P

wm = 2*math.pi*Nm/60 # angular velocity of motor
V = 220 # common voltage seen in household applicatoions
rho_Cu = 1.72e-8
a = 7 #No of parallel coil branches
Nstrand = 231 # No of parallel strands in litz wire
Lturn = math.pi*Do # Length of each turn
Bg = 0.98 # The magnetic flux value is taken from paper
Ns = V*(1/(wm*Bg*(math.pi*(Do**2*(1- lm**2)/4)/P))) #Number of turns

Astrand = (math.pi*Dstrand**2)/4 # Area of wire strand

Rs = (rho_Cu*Lturn*Ns)/(a*Nstrand*Astrand) # Resistance of stator
Iload = 5000/220 # Load current

Re = (2*math.pi*Nm*rho_steam*(Ro**2)/vis) #Reynolds number

cf = 3.87/(Re**0.5) #Co -efficient of Drag
Vcu = Ns*Lturn*Astrand # Volume of copper used

# Losses

Pmech = (0.5*cf*rho_steam)*((2*math.pi*Nm)**3)*(Ro**5 - Rsh**5) # Mechanical loss

Pcu = Rs*(Iload**2) # Current loss

Pcu_eddy = ((Nstrand*Bg*2*math.pi*f*Dstrand)**2*Vcu)/(32*rho_Cu) # eddy current loss

Pload = 5e3
eff_mc = Pload/(Pload + Pmech+ Pcu+ Pcu_eddy)

Ploss= [Pmech, Pcu, Pcu_eddy]

import pandas as pd
  
# DataFrame of each student and the votes they get
Losses = pd.DataFrame({'Name': ['Pmech', 'Pcu', 'Pcu_eddy'],
                          'Values': [Pmech, Pcu, Pcu_eddy]})
  
# Plotting the pie chart for above dataframe
Losses.groupby(['Name']).sum().plot(
    kind='pie', y='Values', autopct='%1.0f%%')