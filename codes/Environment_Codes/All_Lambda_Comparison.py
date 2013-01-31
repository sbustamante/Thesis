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
#Labels of graphs
labels = ["BOLSHOI","CLUES_16953","CLUES_2710", "CLUES_10909"]
#Box lenght
Box_L = [256., 64., 64., 64.]
#Resolutions
res = [512, 128, 128, 128]

#Colors array
Colors = ['black', 'red', 'green', 'blue']
#Linewidths
#Linewidths = [0.5,0.5,0.5,2]
Linewidths = [2.0,1.0,1.0,1.0]

#Numbers of division for lambdas
N_lambda = 60
#Values in lambda interval
L_min = -2.0
L_max = 2.0

#==================================================================================================
#			CALCULATING LAMBDA SMOOTH COMPARISON
#==================================================================================================
i_fold = 0
for fold in folds:
    #if fold != 'BOLSHOI/':
	#i_fold += 1
	#continue
      
    print '\nCurrently in ', fold
    
    #Loading original environment of each halo
    halos_envinroment = np.loadtxt("%s%s%d/Halos_Environment.dat"%(foldglobal, fold, res[i_fold]))
    #Loading smoothed environment of each halo
    halos_envinroment_s1 = np.loadtxt("%s%s%d/Halos_Environment_s1.dat"%(foldglobal, fold, res[i_fold]))
    #Difference
    Lambda_error = (halos_envinroment - halos_envinroment_s1)/halos_envinroment
    
    Nhalos = len(halos_envinroment)
    
    #Halos histogram
    Error_Histogram = np.zeros( (N_lambda, 3) )
    
    Error = np.zeros( (3,N_lambda+1) )
    Error[0] = np.linspace( L_min, L_max, N_lambda+1 )
    Error[1] = np.linspace( L_min, L_max, N_lambda+1 )
    Error[2] = np.linspace( L_min, L_max, N_lambda+1 )
    
    for i_hist in range(N_lambda):
	for l in xrange(3):
	  
	    #HALOS HISTOGRAM
	    for i_halos in xrange(Nhalos):
		if Error[l,i_hist] <= Lambda_error[i_halos,l] < Error[l,i_hist+1]:
		    Error_Histogram[i_hist,l] += 1
		        
    #Lambda 1 plot
    plt.subplot(131)
    plt.title( "$\lambda_1$ comparison" )
    plt.plot( Error[0,:-1], Error_Histogram[:,0]/np.sum(1.0*Error_Histogram[:,0]),\
    linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold], label = fold )

    #Lambda 2 plot
    plt.subplot(132)
    plt.title( "$\lambda_2$ comparison" )
    plt.plot( Error[1,:-1], Error_Histogram[:,1]/np.sum(1.0*Error_Histogram[:,1]),\
    linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold] )

    #Lambda 3 plot
    plt.subplot(133)
    plt.title( "$\lambda_3$ comparison" )
    plt.plot( Error[2,:-1], Error_Histogram[:,2]/np.sum(1.0*Error_Histogram[:,2]),\
    linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold] )

    i_fold += 1

plt.subplot(131)    
#plt.plot( [-1,-1], linestyle = '-',color = 'black', label = 'Halos Sample', linewidth = 3 )
#plt.plot( [-1,-1], linestyle = '--',color = 'black', label = 'Isolated pairs Sample', linewidth = 3 )
#plt.plot( [-1,-1], linestyle = '-.',color = 'black', label = 'LG Sample', linewidth = 3 )
plt.xlabel( "($\lambda_1$ - $\lambda_{1,smooth}$)/$\lambda_1$" )
plt.ylabel( "Fraction" )
plt.yticks(np.linspace(0,1,11),np.linspace(0,1,11))
#plt.ylim( (0,1) )
plt.ylim( (0,0.15) )
plt.xlim( (L_min,L_max) )
plt.grid()
plt.legend(loc='upper right')

plt.subplot(132)
plt.xlabel( "($\lambda_2$ - $\lambda_{2,smooth}$)/$\lambda_2$" )
plt.yticks(np.linspace(0,1,11),[''])
#plt.ylim( (0,1) )
plt.ylim( (0,0.15) )
plt.xlim( (L_min,L_max) )
plt.grid()

plt.subplot(133)
plt.xlabel( "($\lambda_3$ - $\lambda_{3,smooth}$)/$\lambda_3$" )
plt.yticks(np.linspace(0,1,11),[''])
#plt.ylim( (0,1) )
plt.ylim( (0,0.15) )
plt.xlim( (L_min,L_max) )
plt.grid()
#plt.legend(labels, loc='upper right')

plt.savefig( "All_Lambda_Comparison.pdf", format = 'pdf')
plt.show()