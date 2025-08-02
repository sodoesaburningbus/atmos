### This module contains functions relating to Monin-Obukhov Similarity theory.
### The relationships used herein are sourced from the textbook
### "An Introduction to Boundary Layer Meteorology" by Stull (2009)
###
### As a reminder, M-O similarity theory is most appropriate for an unstable surface layer with windy conditons (U* != 0)
###
### Christopher Phillips

### Import modules
import numpy as np

### Constants
k = 0.40 # von Karman constant
g = 9.81 # Gravitaitonal acceleration [m/s2]

### Function to compute the Monin-Obuukhov length
### Inputs:
###  temp, float array, either temporal or spatial distribution of any temperature (but preferably virtual potential)
###  w, float array, same shape as temp, either temporal or spatial distribution of vertical wind
###  ustar, float, the friction velocity
###
### Outputs:
###  L, float, the Obukhov length
def compute_L(temp, w, ustar):

    L = -(ustar**3)/(k*g*compute_flux(temp, w)/np.nanmean(temp))

    return L

### Function to compute fluxes
### Inputs:
###  A, float array, either temporal or spatial distribution of the variable for flux computation
###  w, float array, same shape as A, either temporal or spatial distribution of wind
###
### Outputs:
###  Aw, float array matching input shape of A, the values of the A flux.
def compute_flux(A, w):

    # Check if inputs are same shape
    if (A.shape != w.shape):
        raise Exception('Both inputs must be same shape!')


    Abar = np.nanmean(A)
    wbar = np.nanmean(w)

    Aprime = A-Abar
    wprime = w-wbar

    Aw = np.nanmean(Aprime*wprime)

    return Aw

### Function to compute U*
### Inputs:
###  u, float array, either temporal or spatial distribution of zonal wind
###  v, float array, either temporal or spatial distribution of meridional wind
###  w, float array, either temporal or spatial distribution of vertical wind
###
### Outputs:
###  ustar, float, the friction velocity
def compute_ustar(u,v,w):

    # Compute momentum fluxes
    uw = compute_flux(u,w)
    vw = compute_flux(v,w)

    # Compute friction velocity
    ustar = (uw**2+vw**2)**0.25

    return ustar

### Function to compute the temperature scale (Tstar)
### Inputs:
###  temp, float array, any temperature (T, Tv, Theta, etc.)
###  w, float array, either temporal or spatial distribution of vertical wind
###  ustar, float, friction velocity
###
### Outputs:
###  tstar, float, temperature scale
def compute_tstar(temp, w, ustar):

    uT = compute_flux(temp,w)
    tstar = -uT/ustar

    return tstar

### Function to compute temperature gradient at a height in the surface layer
### Inputs:
###  z, float, the height at which to compute the gradient [m]
###  L, float, the Obhukov length
###  tstar, float, temperature scale. Whether dry bulb, virtual, etc. determines which temperature gradient is computed
###  ustar, float, friction velocity
###
### Outputs:
###  dTdz, float, the temperature (matching tstar) gradient at height z [K/m]
def compute_dTdz(z, L, tstar, ustar):

    if (L <= 0): # The buoyant case
        dTdz = tstar/(k*z)*0.74*((1.0-9.0*z/L)**(-0.5))

    else: # The dynamically unstable case
        dTdz = tstar/(k*z)*0.74+4.7*z/L

    return dTdz

### Function to compute the temperature at a new level using another level.
### Functions for any dry bulb, virtual, etc, provided that Tstar is of the same type.
### Uses 4th order Runge-Kutta and numerical integrates the temperature gradient
### beginning at the initial height and moving towards the final height.
### Inputs:
###  z1, float, the initial height [m]
###  temp1, float, the temperature at z1 [K]
###  L, float, the Obhukov length
###  tstar, float, temperature scale. Whether dry bulb, virtual, etc. determines which temperature gradient is computed
###  ustar, float, friction velocity
###  z2, float, the final height [m]
###  step_size, optional, defaults to 0.1 m, the integration step [m].
###  tolerance, optional, defaults to 0.05 m, allowable deviation from z2 when stopping integration 
###
### Outputs:
###  temp2, float, the temperature at z2 [K]
def compute_temp(z1, temp1, L, tstar, ustar, z2, step_size=0.1, tolerance=0.05):

    # Initialization
    z = z1
    temp2 = temp1

    # Integration
    while (abs(z2-z) < tolerance):

        k1 = compute_dTdz(z, L, tstar, ustar)
        k2 = compute_dTdz(z+step_size*0.5, L, tstar, ustar) # note in this instance, k2==k3 in traditional RK4 notation
        k4 = compute_dTdz(z+step_size, L, tstar, ustar)

        temp2 = temp2+(step_size/6.0)*(k1+4.0*k2+k4)

    return temp2