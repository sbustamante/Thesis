#==================================================================================================
#			HEADERS
#==================================================================================================
from struct import *
import numpy as np
import sys
import matplotlib
import os

import matplotlib.pyplot as plt
from pylab import *

import halo_cuts as HC

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Global Fold
foldglobal = '../Data/'
#Data filename
fold="CLUES/2710/Vweb/"
#fold="BOLSHOI/Vweb/"
#Reslution
n_x = 64

#==========================================================================================
#			HALOS AND ENVIRONMENT DATA
#==========================================================================================
#Environment data
datos = np.loadtxt( "%s%s%d/enviroment_Lamb_0.00_new.dat"%(foldglobal,fold,n_x) )

New_datos = np.zeros( len(datos) )

for i in xrange( len(datos) ):
    #Voids
    if datos[i] == 0 or datos[i] == 1 or datos[i] == 3:
	New_datos[i] = 0
    #Sheets
    if datos[i] == 6 or datos[i] == 3 or datos[i] == 4:
	New_datos[i] = 1
    #Filaments
    if datos[i] == 5 or datos[i] == 5 or datos[i] == 7 or datos[i] == 8:
	New_datos[i] = 2
    #Knots
    if datos[i] == 9:
	New_datos[i] = 3
	
np.savetxt( "%s%s%d/enviroment_Lamb_0.00_std.dat"%(foldglobal,fold,n_x), New_datos )
