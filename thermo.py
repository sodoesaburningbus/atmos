# This module contains thermodynamic functions and constants
# that are useful to Atmospheric Scientists
# Written by Christopher Phillips
# Source materials are:
# Grant Petty's "A First Course in Atmospheric Thermodynamics" 1st Ed.
# Dennis Hartmann's "Global Physical Climatology" 1994 Ed.
#
# Requires:
#	Python 3.4+
#	Numpy
#
# History:
#	July 25th, 2016 - First Write
#	July 27th, 2016 - Added Virtual Temperature Function, Poisson's Equation,
#		Potential Temperature
#	July 28th, 2016 - Added Bolton's Formula for Saturation Vapor Pressure
#	August 10th, 2016 - Added RH calculator
#	August 15th, 2016 - Completed moist adiabat function
#	August 16th, 2016 - Added mixing ratio to vapor pressure conversion
#
#
# Future Plans:
#	More as I decide what I use most often
#
#
# Copyright:
# This module may be freely distributed and used provided this header
# remains attached.
# ~Christopher Phillips

#Import required modules
import numpy

############################################################################
#++++++++++++++++++++++++++++++ CONSTANTS ++++++++++++++++++++++++++++++++++
############################################################################

#From Petty
G = 9.80665 #Gravitational Acceleration (m/s^2)
P0 = 101325.0 #Standard Sea Pressure (Pa)
RD = 287.047 #Gas Constant for Dry Air (J/kg/K)
RV = 461.5 #Gas Constant for Water Vapor (J/kg/K)
CP = 1005.0 #Heat Capacity of Dry Air with Constant Pressure (J/kg/K)
CV = 718.0 #Heat Capacity of Dry Air with Constant Volume (J/kg/K)


#From Hartmann
CVP = 1952.0 #Heat Capacity of Water Vapor with Constant Pressure (J/kg/K)
CVV = 1463.0 #Heat Capacity of Water Vapor with Constant Volume (J/kg/K)
LV0 = 2.5e6 #Latent Heat of Vaporization at 0'C (J/kg)
LV100 = 2.25e6 #Latent Heat of Vaporization at 100'C (J/kg)
LF = 3.34e5 #Latent Heat of Fusion at 0'C (J/kg)



############################################################################
#++++++++++++++++++++++++++++++ FUNCTIONS ++++++++++++++++++++++++++++++++++
############################################################################

#This function calculates dewpoint given vapor pressure
#by reversing Bolton's Formula
#Inputs:
#e, type=float, vapor pressure in Pa
#Outputs:
#Dewpoint temperature in Kelvin
def dewpoint(e):
	try:
		return -243.5*numpy.log(e/611.2)/(numpy.log(e/611.2)-17.67)+273.15
	except Exception as err:
		print(err)
		return -1
	

#This function converts vapor pressure to mixing ratio
#Equation 7.22 in Petty
#Inputs:
#pres, type=float, pressure in Pa
#vpres, type=float, vapor pressure in Pa
#Outputs:
#Mixing ratio in kg/kg
#Returns -1 on failure
def etow(pres, vpres):
	try:
		return (RD/RV*vpres)/(pres-vpres)
	except Exception as err:
		print(err)
		return -1

#Hypsometric Equation from Petty
#Given two pressure levels and the mean layer virtual temperature,
#this function calculates the thickness of the layer.
#Inputs:
#p1, type=float, pressure in Pa of bottom layer
#p2, type=float, pressure in Pa of top of layer
#Tbar, type=float, mean layer virtual temperature in Kelvin
#Outputs:
#Layer thickness, type=float, in meters
#-1 on failure
def hydrostatic(p1,p2,Tbar):
	try:
		if (p1 < p2):
			raise ValueError()
		return RD*Tbar/G*numpy.log(p1/p2)

	except ValueError:
		print("ERROR: Pressure at top of layer must be less than pressure at bottom!")
		return -1

	except Exception as err:
		print(err)
		return -1

#Moist Adiabatic Lapse Rate from Peety
#Numerically integrates EQ 7.37 in Petty
#using the 4th order Rutta-Kunga method
#Lifts a saturated parcel adiabatically to a
#specified pressure
#Inputs:
#p1, type=float, initial pressure in Pa
#p2, type=float, final pressure in Pa
#t1, type=float, initial temperature in Kelvin
#Outputs:
#A dictionary containing a list of pressures and the corresponding temperatures
#Pressure list may be accessed with key: 'pres'
#Temperature list may be accessed with key: 'temp'
#Returns -1 on failure
def moist_adiabat(p1,p2,t1):
	def dtdp(p,t): #Equation 7.37 from Petty
		return ((1.0+(LV0*etow(p, sat_vaporpres(t))/RD/t))/
			(1.0+((LV0**2)*etow(p, sat_vaporpres(t))/RV/CP/t**2))
			*t/p*RD/CP)

	try:
		#Testing if first pressure is lower in atmosphere than second pressure		
		if (p1 < p2):
			raise Exception('p1 must be a larger pressure than p2.')

		#Defining stepsize
		dp = -1.0 #Stepsize in Pa
		#Calculating pressure levels to use in integration and placing in list
		pres = list(numpy.arange(p1,p2+dp,dp))
		#Placing initial temeprature in a list
		temp = [t1]
		#Performing integration
		for p in pres:
			k1 = dp*dtdp(p,temp[-1])
			k2 = dp*dtdp(p+0.5*dp, temp[-1]+0.5*k1)
			k3 = dp*dtdp(p+0.5*dp, temp[-1]+0.5*k2)
			k4 = dp*dtdp(p+dp, temp[-1]+k3)
			temp.append(temp[-1]+1.0/6.0*k1+1.0/3.0*k2+1.0/3.0*k3+1.0/6.0*k4)
			
		return {'pres':pres, 'temp':temp}

	except Exception as err:
		print(err)		
		return -1

#Poisson's Equation from Petty
#Given an initial temperature, initial pressure, and final pressure,
#this function returns the final temperature of a parcel
#that underwent a dry adiabatic ascent.
#Inputs:
#p1, type=float, initial pressure in Pa
#p2, type=float, final pressure in Pa
#temp, type=float, initial temperature in Kelvin
#OUTPUTS:
#Final Temp, type=float
#-1 on failure
def poisson(p1,p2,temp):
	try:
		return temp*(p2/p1)**(RD/CP)
	except Exception as err:
		print(err)		
		return -1

#Potential Temperature from Petty
#Given a temperature and a pressure, this function
#returns the potential temperature of the parcel
#Inputs:
#pres, type=float, pressure in Pa
#temp, type=float, temperatue in Kelvin
#-1 on failure
def pot_temp(pres, temp):
	try:
		return poisson(pres, 100000.0, temp)
	except Exception as err:
		print(err)
		return -1

#RH calculator from Petty
#Given dewpoint and temperature, calculates RH
#Inputs:
#dtemp, type=float, dewpoint in Kelvin
#temp, type=float, temp in Kelvin
#Outputs:
#Relative humidity as a decimal
#-1 on failure
def rh(dtemp, temp):
	try:
		return sat_vaporpres(dtemp)/sat_vaporpres(temp)
	except Exception as err:
		print(err)
		return -1

#Saturation Vapor Pressure from Petty
#Calculated with Bolton's Formula
#which is accurate to 0.1% between -30'C and 35'C
#Inputs:
#temp, type=float, environmental temperature in Kelvin
#Outputs:
#Saturation vapor pressure in Pa
#-1 on failure
def sat_vaporpres(temp):
	try:
		temp -= 273.15 #Convert Kelvin -> Celcius
		return 611.2*numpy.exp(17.67*temp/(temp+243.5))
	except Exception as err:
		print(err)
		return -1

#Virtual Temperature Equation from Petty
#Given temperature and mixing ratio, computes virtual temperature
#Inputs:
#temp, type=float, temperature in Kelvin
#mix_ratio, type=float, mixing ratio in kg/kg
#Outputs:
#Virtual Temperature, type=float, in Kelvin
def virt_temp(temp, mix_ratio):
	try:
		return (1.0+(RV/RD-1.0)*(mix_ratio/(1.0+mix_ratio)))*temp
	except Exception as err:
		print(err)
		return -1

#This function converts mixing ratio to vapor pressure
#Equation 7.22 in Petty
#Inputs:
#pres, type=float, pressure in Pa
#mixr, type=float, mixing ratio in kg/kg
#Outputs:
#vapor pressure in Pa
#Returns -1 on failure
def wtoe(pres, mixr):
	try:
		return mixr*pres/(RD/RV+mixr)
	except Exception as err:
		print(err)
		return -1


