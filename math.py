# This module contains mathematical functions and constants
# that are useful to Atmospheric Scientists
# Written by Christopher Phillips
# Source materials are:
# Grant Petty's "A First Course in Atmospheric Thermodynamics" 1st Ed.
# Dennis Hartmann's "Global Physical Climatology" 1994 Ed.
#
# Requires:
#    Python 3.4+
#    Numpy
#
# History:
#    January 24, 2020 - First Write
#       Functiont to interpolate variables to a given layer
#       Function to average variables over a layer
#
# Copyright:
# This module may be freely distributed and used provided this header
# remains attached.
# ~Christopher Phillips

#Import required modules
import numpy

############################################################################
#++++++++++++++++++++++++++++++ FUNCTIONS +++++++++++++++++++++++++++++++++#
############################################################################

#This function interpolates variables between two layers
#It assumes that variables vary linearly with log-pressure
#Inputs:
# pbot, ptop, pmid, type = float or 2D array of floats, bottom, top,
# and desired pressure levels respectively.
# varbot, vartop, type = float or 2D array of floats, bottom and
#top layer of variable to interpolate.
#
#Outputs:
# varmid, float or 2D array of floats, the interpolated variable.
#
def layer_interp(pbot, ptop, pmid, varbot, vartop):
    #Compute interpolation weight
    alpha = numpy.log(pmid/pbot)/numpy.log(ptop/pbot)

    #Interpolate and return
    return alpha*vartop+(1-alpha)*varbot

#This function calculate the pressure-wighted layer average of a variable
#Inputs:
# pres, 1D array of floats, vertical pressure levels to average over
# var, 1D array of floats, the vertical profile of the variable to average
#
#Outputs:
# meanvar, float, the layer-averaged variable
def layer_average(pres, var):
