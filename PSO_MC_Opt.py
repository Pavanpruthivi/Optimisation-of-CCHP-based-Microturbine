from numpy import *
from random import random as rand
import math

rho_steam = 1.295 # density of air
vis = 22.97e-6 # viscosity of air
P = 6 #No of poles 3 phase synchronous ac generator
f = 50 # frequency in India
Nm = 120*f/P

wm = 2*math.pi*Nm/60 # angular velocity of motor
Bg = 0.98 # The magnetic flux value is taken from paper
V = 220 # common voltage seen in household applicatoions
rho_Cu = 1.72e-8
a = 7 #No of parallel coil branches
Nstrand = 231 # No of parallel strands in litz wire

Pload = 5e3 # Load Power

iter_max = 50
pop_size = 50
dimensions = 3
c1 = 1.5
c2 = 2
w = 0.75
err_crit = 0.001

class Particle:
    pass

def constraint(position, minx, maxx):
    if position < minx:
        position = minx
    elif position > maxx:
        position = maxx

    return position

def f6(param):
    para = param
    Ro = param[0]/2
    Rsh = Ro/6
    Iload = Pload/V # Load current
    
    Re = (2*math.pi*Nm*rho_steam*(Ro**2)/vis) #Reynolds number
    cf = 3.87/(Re**0.5) #Co -efficient of Drag

    Pmech = (0.5*cf*rho_steam)*((2*math.pi*Nm)**3)*(Ro**5 - Rsh**5) # Mechanical loss
    
    Ns = V*(1/(wm*Bg*(math.pi*(param[0]**2*(1- param[1]**2)/4)/P))) #Number of turns
    Astrand = (math.pi*param[2]**2)/4 # Area of wire strand
    Lturn = math.pi*param[0] # Length of each turn
    Rs = (rho_Cu*Lturn*Ns)/(a*Nstrand*Astrand) #Resistance of Stator
    Vcu = Ns*Lturn*Astrand

    Pcu= Rs*(Iload**2)
    Pcu_eddy=((Nstrand*Bg*2*math.pi*f*param[2])**2*Vcu)/(32*rho_Cu) # eddy current loss
    f6 = Pmech + Pcu + Pcu_eddy

    errorf6 = f6
    return f6, errorf6;
    # return f6;


# initialize the particles
particles = []
for i in range(pop_size):
    p = Particle()
    p.params = array([random.uniform(0.1, 0.4) ,random.uniform(0.2,0.9),random.uniform(0.0001,0.0003)])
    print(p.params)
    p.fitness = 0.0
    p.v = 0.0
    p.best = 0
    particles.append(p)

# print(particles)
# let the first particle be the global best
gbest = particles[0]
err = 999999999
while i < iter_max:
    for p in particles:
        fitness, err = f6(p.params)
        print(fitness)
        if fitness < p.fitness:
            p.fitness = fitness
            # print(p.fitness)
            p.best = p.params
            # print(p.best)

        if fitness < gbest.fitness:
            gbest = p

        p.v = w * p.v + c1 * rand() * (p.best - p.params) + c2 * rand() * (gbest.params - p.params)

        p.params = p.params + p.v

        for k in range(dimensions):
            if k == 0:
                minx = 0.1
                maxx = 0.4
            if k == 1: 
                minx = 0.2
                maxx = 0.9
            if k == 2:
                minx = 0.0001
                maxx = 0.0003
            p.params[k] = constraint(p.params[k], minx, maxx)

    i += 1

    if err < err_crit:
        break
    # progress bar. '.' = 10%
    # if i % (iter_max/10) == 0:
    #   print ('.')

print('\nParticle Swarm Optimisation\n')
print('PARAMETERS\n', '-' * 9)
print('Population size : ', pop_size)
print('Dimensions      : ', dimensions)
print('Error Criterion : ', err_crit)
print('c1              : ', c1)
print('c2              : ', c2)
print('function        :  f6')

print('RESULTS\n', '-' * 7)
print('gbest fitness   : ', gbest.fitness)
print('gbest params    : ', gbest.params)
print('iterations      : ', i + 1)
