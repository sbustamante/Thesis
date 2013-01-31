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
folds = [ "BOLSHOI/","CLUES/16953/", "CLUES/2710/", "CLUES/10909/"]
#Lambdas_Threshold
lambda_thr = np.linspace(0,1,21)
#Classification Scheme of environment
Scheme = 'Tweb/'
#Labels of graphs
labels = ["BOLSHOI","CLUES_16953","CLUES_2710", "CLUES_10909"]
#Box lenght
Box_L = [256., 64., 64., 64.]
#Resolutions
res = [256, 64, 64, 64]
#Index of each LG halos
LG_index = [ False, [888,1106], [642,830], [674,894] ]

#Colors array
Colors = ['black', 'red', 'green', 'blue']
#Linewidths
#Linewidths = [0.5,0.5,0.5,2]
Linewidths = [2.0,1.0,1.0,1.0]
#Markers
Markers = ['','','','']

#Numbers of division for lambdas
N_lambda = 60
#Values in lambda interval
L_min = -2
L_max = 2

#Number of partitions in bolshoi simulation
N = 4

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
    ncol = len(halos)
    Nhalos = len(halos[0])		#Number of halos
    

    #Loading environment of each halo
    halos_envinroment = np.loadtxt("%s%s%s%d/Halos_Environment_s1.dat"%(foldglobal, fold, Scheme, res[i_fold]))
    
    #Halos histogram
    Halos_Histogram = np.zeros( (N_lambda, 3) )
    
    Lambdas = np.zeros( (3,N_lambda+1) )
    Lambdas[0] = np.linspace( L_min, L_max, N_lambda+1 )
    Lambdas[1] = np.linspace( L_min, L_max, N_lambda+1 )
    Lambdas[2] = np.linspace( L_min, L_max, N_lambda+1 )
    
    for i_hist in range(N_lambda):
	for l in xrange(3):
	  
	    #HALOS HISTOGRAM
	    for i_halos in xrange(Nhalos):
		if Lambdas[l,i_hist] <= halos_envinroment[i_halos,l] < Lambdas[l,i_hist+1]:
		    Halos_Histogram[i_hist,l] += 1
		    
    #Cosmic Variance Effect
    if fold == 'BOLSHOI/':
	#Sort in x coordinate
	argx = list( np.argsort( halos[1] ) )
	for i in xrange(0, ncol):
	    halos[i] = halos[i][argx]

	#Sort in y coordinate
	Nx = Nhalos/N
	for j in xrange(0,N):
	    argy = list( np.argsort( halos[2][j*Nx:(j+1)*Nx-1] ) )
	    for i in xrange(0, ncol):
		halos[i][j*Nx:(j+1)*Nx-1] = halos[i][j*Nx:(j+1)*Nx-1][argy]
	    
	#Sort in y coordinate
	Ny = Nhalos/(N**2)
	for j in xrange(0,N):
	      for k in xrange(0,N):
		  argz = list( np.argsort( halos[3][j*Nx:(j+1)*Nx-1][k*Ny:(k+1)*Ny-1] ) )
		  for i in xrange(0, ncol):
		      halos[i][j*Nx:(j+1)*Nx-1][k*Ny:(k+1)*Ny-1] = halos[i][j*Nx:(j+1)*Nx-1][k*Ny:(k+1)*Ny-1][argz]
	Nz = Nhalos/(N**3)
	
	for i_box in xrange(0,N**3):
	    #Halos histogram
	    Bolshoi_Histogram = np.zeros( (N_lambda, 3) )
	
	    Lambdas = np.zeros( (3,N_lambda+1) )
	    Lambdas[0] = np.linspace( L_min, L_max, N_lambda+1 )
	    Lambdas[1] = np.linspace( L_min, L_max, N_lambda+1 )
	    Lambdas[2] = np.linspace( L_min, L_max, N_lambda+1 )
	    
	    for i_hist in range(N_lambda):
		for l in xrange(3):
		    #HALOS HISTOGRAM
		    for i_halos in np.arange( Nhalos/(1.0*N**3)*i_box, Nhalos/(1.0*N**3)*(i_box+1) - 1, 1 ):
			if Lambdas[l,i_hist] <= halos_envinroment[halos[ 0, i_halos ] - 1 ,l] < Lambdas[l,i_hist+1]:
			    Bolshoi_Histogram[i_hist,l] += 1
		    
			
	    #Lambda 1 plot
	    plt.subplot(131)
	    plt.title( "$\lambda_1$ distribution" )
	    plt.plot( Lambdas[0,:-1], Bolshoi_Histogram[:,0]/np.sum(Bolshoi_Histogram[:,0]),\
	    linestyle = '-', color = 'purple', linewidth = 0.5 )
	    
	    #Lambda 2 plot
	    plt.subplot(132)
	    plt.title( "$\lambda_2$ distribution" )
	    plt.plot( Lambdas[1,:-1], Bolshoi_Histogram[:,1]/np.sum(Bolshoi_Histogram[:,1]),\
	    linestyle = '-', color = 'purple', linewidth = 0.5 )

	    #Lambda 3 plot
	    plt.subplot(133)
	    plt.title( "$\lambda_3$ distribution" )
	    plt.plot( Lambdas[2,:-1], Bolshoi_Histogram[:,2]/np.sum(Bolshoi_Histogram[:,2]),\
	    linestyle = '-', color = 'purple', linewidth = 0.5 )
	    
    #Lambda 1 plot
    plt.subplot(131)
    plt.title( "$\lambda_1$ distribution" )
    plt.plot( Lambdas[0,:-1], Halos_Histogram[:,0]/np.sum(Halos_Histogram[:,0]),\
    linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold], label = fold )

    #Lambda 2 plot
    plt.subplot(132)
    plt.title( "$\lambda_2$ distribution" )
    plt.plot( Lambdas[1,:-1], Halos_Histogram[:,1]/np.sum(Halos_Histogram[:,1]),\
    linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold] )

    #Lambda 3 plot
    plt.subplot(133)
    plt.title( "$\lambda_3$ distribution" )
    plt.plot( Lambdas[2,:-1], Halos_Histogram[:,2]/np.sum(Halos_Histogram[:,2]),\
    linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold] )

    i_fold += 1

plt.subplot(131)    
#plt.plot( [-1,-1], linestyle = '-',color = 'black', label = 'Halos Sample', linewidth = 3 )
#plt.plot( [-1,-1], linestyle = '--',color = 'black', label = 'Isolated pairs Sample', linewidth = 3 )
#plt.plot( [-1,-1], linestyle = '-.',color = 'black', label = 'LG Sample', linewidth = 3 )
plt.xlabel( "$\lambda_1$" )
plt.ylabel( "Fraction" )
plt.yticks(np.linspace(0,1,11),np.linspace(0,1,11))
#plt.ylim( (0,1) )
plt.ylim( (0,0.6) )
#plt.xlim( (L_min,L_max) )
plt.xlim( (-0.5,2.0) )
plt.grid()
plt.legend(loc='upper right')

plt.subplot(132)
plt.xlabel( "$\lambda_2$" )
plt.yticks(np.linspace(0,1,11),[''])
#plt.ylim( (0,1) )
plt.ylim( (0,0.6) )
#plt.xlim( (L_min,L_max) )
plt.xlim( (-1.0,1.0) )
plt.grid()

plt.subplot(133)
plt.xlabel( "$\lambda_3$" )
plt.yticks(np.linspace(0,1,11),[''])
#plt.ylim( (0,1) )
plt.ylim( (0,0.6) )
#plt.xlim( (L_min,L_max) )
plt.xlim( (-2.0,0.5) )
plt.grid()
#plt.legend(labels, loc='upper right')

plt.savefig( "All_Lambda_Histogram.pdf", format = 'pdf')
plt.show()