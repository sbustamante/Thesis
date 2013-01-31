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
#Labels of each Simulation
#label="CLUES 2710"
#Lambda files
lambda_thr = [0.0, 1.0]

#Resolution
n_x = 64
Box_lenght = 64.
#Extent in imshow graphic
extent = [0, Box_lenght, 0, Box_lenght]
#Colors
#New Scheme
#jet3 = plt.cm.get_cmap('gray', 10)
#Old Scheme
jet3 = plt.cm.get_cmap('gray', 4)

#==================================================================================================
#			CALCULATING ENVIROMENT
#==================================================================================================
#==========================================================================================
#			HALOS AND ENVIRONMENT DATA
#==========================================================================================
#Environment data
datos = np.loadtxt( "%s%s%d/enviroment_Lamb_0.00_std.dat"%(foldglobal,fold,n_x) )
enviroment1 = datos.reshape([n_x,n_x,n_x])

#==========================================================================================
#			PLOTTING
#==========================================================================================
#Initializing the figure entorn
fig = plt.figure()
ax = fig.add_subplot(111)

#cax = ax.matshow( -np.transpose(enviroment1[10,:,::-1]), extent=extent, vmin=-9, vmax=0, cmap = jet3 )
cax = ax.matshow( -np.transpose(enviroment1[10,:,::-1]), extent=extent, vmin=-3, vmax=0, cmap = jet3 )
plt.xlim( (0,Box_lenght) )
plt.ylim( (0,Box_lenght) )
plt.ylabel('z [$h^{-1}$Mpc]')
plt.xlabel('y [$h^{-1}$Mpc]')

#Old scheme
#plt.title( "Standard scheme with $\lambda_{th}$ = 0" )
plt.title( "Standardized scheme with $\lambda_{th}$ = 0" )
cbar = fig.colorbar(cax, ticks=[0, -1, -2, -3])
cbar.ax.set_yticklabels(['Void','Sheet','Filament','Knot'])

#New scheme
#plt.title( "New scheme results" )
#cbar = fig.colorbar(cax, ticks=[0, -1, -2, -3, -4, -5, -6, -7, -8, -9] )
#cbar.ax.set_yticklabels(['0','1','2','3','4','5','6','7','8','9',])

plt.show()
