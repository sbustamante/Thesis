#==================================================================================================
#			HEADERS
#==================================================================================================
from __future__ import division
from struct import *
import numpy as np
import sys
import matplotlib
import os
import matplotlib.pyplot as plt
from pylab import *

#==================================================================================================
#			FUNCTIONS
#==================================================================================================
def mass_center( m1, r1, m2, r2 ):
    Rm = ( m1*r1 + m2*r2 )/( m1 + m2 )
    return Rm

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Global Fold
foldglobal = '../Data/'
#Simulation
folds = [ "CLUES/16953/", "CLUES/2710/", "CLUES/10909/", "BOLSHOI/" ]
Box_L = [64., 64., 64., 256.]

#==================================================================================================
#			CALCULATING ENVIROMENT DENSITY DIAGRAM
#==================================================================================================
i_fold = 0
for fold in folds:
    #if fold != 'BOLSHOI/':
	#i_fold += 1
	#continue
      
    print '\nCurrently in ', fold
    
    #Loading Halos Data
    halos = np.transpose( np.loadtxt( '%s%sHalos_catalog.dat'%(foldglobal,fold) ) )
    Nhalos = len(halos[0])		#Number of halos
    
    #Pairs datas
    pairs = np.transpose( np.loadtxt( '%s%sPairs_catalog.dat'%(foldglobal,fold) ) )
    Npair = len(pairs[0])		#Number of isolated pairs
    
    #Angular momentum
    L = np.zeros( (Npair, 6) )
    
    #Calculating total angular momenta of each pair halo
    for i in xrange( Npair ):
	#Data of first halo
	i1 = pairs[1][i] - 1
	m1 = pairs[2][i]
	r1 = halos[1:4,i1]
	v1 = halos[4:7,i1]
	#Data of second halo
	i2 = pairs[4][i] - 1
	m2 = pairs[5][i]
	r2 = halos[1:4,i2]
	v2 = halos[4:7,i2]
	#Mass center coordinate
	Rm = mass_center( m1, r1, m2, r2 )
	Vm = mass_center( m1, v1, m2, v2 )
	#Relative coordinates and velocities
	r1p = r1 - Rm
	r2p = r2 - Rm
	v1p = v1 - Vm
	v2p = v2 - Vm
	#Angular momentum of total pair
	L[i,0:3] = np.cross( r1p, m1*v1p ) + np.cross( r2p, m2*v2p )
	#Normalized angular momentum of total pair
	L[i,3:6] = np.cross( r1p, v1p ) + np.cross( r2p, v2p )
	
    #Saving files
    np.savetxt( '%s%sAngular_Momentum.dat'%(foldglobal,fold), L )