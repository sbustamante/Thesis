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

def enviroment( lambdas, threshold ):
    '''
    FUNCTION: Return the local enviroment in a given r coordinate
    ARGUMENTS: r - Local coordinate
	       n - Number of lambda
    RETURN:   Enviroment
	      0 - Void
	      1 - Filament
	      2 - Knot
    '''
    env = 0
    for i in xrange(3):
	if lambdas[i] >= threshold:
	    env += 1
    return env


#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Global Fold
foldglobal = '../Data/'
#Simulation
folds = [ "CLUES/16953/", "CLUES/2710/", "CLUES/10909/", "BOLSHOI/" ]
#Classification Scheme of environment
scheme = 'Vweb/'
#Labels of graphs
labels = ["CLUES_16953","CLUES_2710", "CLUES_10909", "BOLSHOI"]
#Box lenght
Box_L = [64., 64., 64., 256.]
#Resolutions
res = [64, 64, 64, 256]
#Index of each LG halos
LG_index = [ [888,1106], [642,830], [674,894], False ]

#Numbers of division for lambdas
N_angle = 50
#Values in angle interval
A_min = 0
A_max = 1
#Range
Angles = np.linspace( A_min, A_max, N_angle+1 )

#Colors array
Colors = ['red', 'green', 'blue', 'black']
Linewidths = [0.5,0.5,0.5,2]
#Linewidths = [2.0,2.0,2.0,2]

#Gaussian smoothing
smooth = '_s1'

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
    
    #Isolated Pairs datas
    isop = np.transpose( np.loadtxt( '%s%sIsoPairs_catalog.dat'%(foldglobal,fold) ) )
    Nisop = len(isop[0])		#Number of isolated pairs
    
    #Isolated Pairs datas
    #isop = np.transpose( np.loadtxt( '%s%s%s%d/LG_catalog%s.dat'%(foldglobal, fold, scheme, res[i_fold], smooth) ) )
    #Nisop = len(isop[0])		#Number of isolated pairs
    
    #Loading environment of each halo
    halos_eigenvector = np.loadtxt("%s%s%s%d/Halos_Eigenvector_s1.dat"%(foldglobal, fold, scheme, res[i_fold]))
    
    #Loading momentum of each pair
    pair_momentum = np.loadtxt("%s%s/Angular_Momentum.dat"%(foldglobal, fold))
    
    #Construction of mean environment eigenvector and histogram of angles
    pair_eigenvector = np.zeros( (Nisop, 9) )
    angle_histogram = np.zeros( (N_angle, 3) )
    for i in xrange( Nisop ):
	i1 = isop[1][i] - 1
	i2 = isop[4][i] - 1
	#Angle between each eigendirection and the angular momentum
	angle = np.zeros( 3 )
	for j in xrange(3):
	    #Mean eigenvector
	    norma = norm((halos_eigenvector[i1,3*j:3*j+3] + halos_eigenvector[i2,3*j:3*j+3]))
	    pair_eigenvector[i,3*j:3*j+3] = (halos_eigenvector[i1,3*j:3*j+3] + halos_eigenvector[i2,3*j:3*j+3])/norma
	    #Angles
	    angle[j] = np.dot( pair_eigenvector[i,3*j:3*j+3], pair_momentum[i,0:3] )/norm(pair_momentum[i,0:3])
	    #Histogram
	    for k in xrange(N_angle):
		#if Angles[k] <= abs(angle[j]) < Angles[k+1]:
		    #angle_histogram[k,j] += 1
		if Angles[k] <= abs(angle[j]):
		    angle_histogram[k,j] += 1
    
    #Plotting properties---------------------------------------
    #Angle with first eigenvector
    plt.subplot(131)
    plt.plot( Angles[:-1], angle_histogram[:,0]/(1.0*angle_histogram[0,0]), linewidth = Linewidths[i_fold], color = Colors[i_fold] )
    
    #Angle with second eigenvector
    plt.subplot(132)
    plt.plot( Angles[:-1], angle_histogram[:,1]/(1.0*angle_histogram[0,1]), linewidth = Linewidths[i_fold], color = Colors[i_fold] )
    
    #Angle with second eigenvector
    plt.subplot(133)
    plt.plot( Angles[:-1], angle_histogram[:,2]/(1.0*angle_histogram[0,2]), linewidth = Linewidths[i_fold], color = Colors[i_fold] )
    
    i_fold += 1
    
    
#Formating figures
plt.subplot(131)
plt.grid()
plt.xlabel( "$\cos(\\theta_1) = \sigma_1 \cdot \hat{L}_{pair}$" )
plt.ylabel( "Accumulated Fraction > $\cos(\\theta)$" )
plt.title( "Pair orientation: first," )

plt.subplot(132)
plt.grid()
plt.xlabel( "$\cos(\\theta_2) = \sigma_2 \cdot \hat{L}_{pair}$" )
plt.yticks( np.linspace(0,1,6), [" "," "," "," "," "," "] )
plt.title( "second and " )

plt.subplot(133)
plt.grid()
plt.xlabel( "$\cos(\\theta_3) = \sigma_3 \cdot \hat{L}_{pair}$" )
plt.yticks( np.linspace(0,1,6), [" "," "," "," "," "," "] )
plt.title( "third eigendirection." )
plt.legend( labels )