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

#==================================================================================================
#			FUNDAMENTAL CONSTANTS
#==================================================================================================
GC = 6.6742e-11
MPC2M = 3.085678e22
KM2M = 1e3
MSUN2KG = 1.98e30

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Global Fold
foldglobal = '../Data/'
#Simulation
folds = [ "CLUES/16953/", "CLUES/2710/", "CLUES/10909/", "BOLSHOI/" ]
#Lambdas_Threshold
lambda_thr = np.linspace(0,1,21)
#Labels of graphs
labels = ["CLUES_16953","CLUES_2710", "CLUES_10909", "BOLSHOI"]
#Box lenght
Box_L = [64., 64., 64., 256.]
#Resolutions
res = [128, 128, 128, 512]
#Index of each LG halos
LG_index = [ [888,1106], [642,830], [674,894], False ]

#Colors array
Colors = ['red', 'green', 'blue', 'black']
#Enviroment Labels
env_labels = ['voids', 'sheets', 'filaments', 'knots']
#Linewidths
Linewidths = [1,1,1,2]
#Markers
Markers = ['o','s','>','']

#Number of Energy Histogram
N_energy = 10

#==================================================================================================
#			CALCULATING ENVIROMENT DENSITY DIAGRAM
#==================================================================================================
plt.figure(figsize=(16,8.5))
i_fold = 0
for fold in folds:
    print '\nCurrently in ', fold
    
    #Loading Halos Data
    halos = np.transpose( np.loadtxt( '%s%sHalos_catalog.dat'%(foldglobal,fold) ) )
    Nhalos = len(halos[0])		#Number of halos
    
    #Isolated Pairs datas
    isop = np.transpose( np.loadtxt( '%s%sLG_catalog.dat'%(foldglobal,fold) ) )
    Nisop = len(isop[0])		#Number of isolated pairs

    #Loading environment of each halo
    halos_envinroment = np.loadtxt("%s%s%d/Halos_Environment.dat"%(foldglobal, fold, res[i_fold]))
        
    #Energy array
    Energy_pair = np.zeros(Nisop)
    
    for i_iso in xrange(Nisop):
	i1 = isop[1,i_iso]-1
	i2 = isop[4,i_iso]-1
	#Halo 1
	r1 = halos[ 1:4, i1 ]
	v1 = halos[ 4:7, i1 ]
	m1 = halos[ 8, i1 ]
	#Halo 2
	r2 = halos[ 1:4, i2 ]
	v2 = halos[ 4:7, i2 ]
	m2 = halos[ 8, i2 ]
	#Energy
	Energy_pair[i_iso] = KM2M**2*MSUN2KG*(0.5*m1*norm(v1**2) + 0.5*m2*norm(v2**2)) - GC*m1*m2*MSUN2KG**2/( norm(r1-r2)*MPC2M )
	print KM2M**2*MSUN2KG*(0.5*m1*norm(v1**2) + 0.5*m2*norm(v2**2)), GC*m1*m2*MSUN2KG**2/( norm(r1-r2)*MPC2M )
	
    
    #Histogram of Halos in each environment
    Energy_Histogram = np.zeros( N_energy )
    #Energy Range
    Energy_Range = np.linspace( np.min(Energy_pair), np.max(Energy_pair), N_energy + 1 )
    
    #Histogram Construction
    for i_en in xrange( N_energy ):
	for i_iso in xrange(Nisop):
	    if Energy_Range[i_en] <= Energy_pair[i_iso] < Energy_Range[i_en+1]:
		Energy_Histogram[i_en] += 1
	    	    
    #Plotting Energy Histogram
    plt.title('Energy histogram of LG pairs')
    plt.plot( Energy_Range[:-1], Energy_Histogram/np.sum(Energy_Histogram), color = Colors[i_fold],\
    linewidth = Linewidths[i_fold], label = labels[i_fold] )
    plt.ylabel('Fraction of LG pairs with Energy given')
    plt.xlabel('Energy [kg km$^2$/s$^2$')
    i_fold += 1
    
plt.savefig('LG_Energy_Histogram.pdf', format = 'pdf')
	    