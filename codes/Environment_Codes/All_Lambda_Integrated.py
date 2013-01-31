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
#Lambdas_Threshold
lambda_thr = np.linspace(0,1,21)
#Classification Scheme of environment
Scheme = 'Vweb/'
#Labels of graphs
labels = ["CLUES_16953","CLUES_2710", "CLUES_10909", "BOLSHOI"]
#Box lenght
Box_L = [64., 64., 64., 256.]
#Resolutions
res = [64, 64, 64, 256]
#Index of each LG halos
LG_index = [ [888,1106], [642,830], [674,894], False ]

#Colors array
Colors = ['red', 'green', 'blue', 'black']
#Enviroment Labels
env_labels = ['voids', 'sheets', 'filaments', 'knots']
#Linewidths
#Linewidths = [0.5,0.5,0.5,2]
Linewidths = [1.0,1.0,1.0,2]
#Markers
Markers = ['','','','']

#Numbers of division for lambdas
N_lambda = 40
#Values in lambda interval
L_min = -2
L_max = 2

#==================================================================================================
#			CALCULATING ENVIROMENT DENSITY DIAGRAM
#==================================================================================================
i_fold = 0
for fold in folds:
    if fold != 'BOLSHOI/':
	i_fold += 1
	continue
      
    print '\nCurrently in ', fold
    
    #Loading Halos Data
    halos = np.transpose( np.loadtxt( '%s%sHalos_catalog.dat'%(foldglobal,fold) ) )
    Nhalos = len(halos[0])		#Number of halos
    
    #Isolated Pairs datas
    isop = np.transpose( np.loadtxt( '%s%sIsoPairs_catalog.dat'%(foldglobal,fold) ) )
    Nisop = len(isop[0])		#Number of isolated pairs
    
    #LG datas
    #lgsamp = np.transpose( np.loadtxt( '%s%s%s%d/LG_catalog.dat'%(foldglobal, fold, Scheme, res[i_fold]) ) )
    #Nlg = len(lgsamp[0])		#Number of isolated pairs

    #Loading environment of each halo
    halos_envinroment = np.loadtxt("%s%s%s%d/Halos_Environment_s1.dat"%(foldglobal, fold, Scheme, res[i_fold]))
    
    #Halos histogram
    Halos_Histogram = np.zeros( (N_lambda, 3) )
    #IsoPairs histogram
    Isop_Histogram = np.zeros( (N_lambda, 3) )
    #LG histogram
    LG_Histogram = np.zeros( (N_lambda, 3) )
    
    Lambdas = np.zeros( (3,N_lambda+1) )
    #Lambdas[0] = np.linspace( min(halos_envinroment[:,0]), max(halos_envinroment[:,0]),  N_lambda+1 )
    #Lambdas[1] = np.linspace( min(halos_envinroment[:,1]), max(halos_envinroment[:,1]),  N_lambda+1 )
    #Lambdas[2] = np.linspace( min(halos_envinroment[:,2]), max(halos_envinroment[:,2]),  N_lambda+1 )
    
    Lambdas[0] = np.linspace( L_min, L_max, N_lambda+1 )
    Lambdas[1] = np.linspace( L_min, L_max, N_lambda+1 )
    Lambdas[2] = np.linspace( L_min, L_max, N_lambda+1 )
    
    for i_hist in range(N_lambda):
	for l in xrange(3):
	  
	    #HALOS HISTOGRAM
	    for i_halos in xrange(Nhalos):
		#Differenciated distribution
		#if Lambdas[l,i_hist] <= halos_envinroment[i_halos,l] < Lambdas[l,i_hist+1]:
		    #Halos_Histogram[i_hist,l] += 1
		#Integrated distribution
		if Lambdas[l,i_hist] <= halos_envinroment[i_halos,l]:
		    Halos_Histogram[i_hist,l] += 1
		
	    #ISOLATED PAIRS HISTOGRAM
	    #for i_isop in xrange(Nisop):
		#i1 = isop[1, i_isop] - 1
		#if Lambdas[l,i_hist] <= halos_envinroment[i1,l] < Lambdas[l,i_hist+1]:
		    #Isop_Histogram[i_hist,l] += 1
		    
	    #LG HISTOGRAM
	    #for i_lg in xrange(Nlg):
		#i1 = lgsamp[1, i_lg] - 1
		#if Lambdas[l,i_hist] <= halos_envinroment[i1,l] < Lambdas[l,i_hist+1]:
		    #LG_Histogram[i_hist,l] += 1
		    
    #Lambda 1 plot
    plt.subplot(131)
    plt.title( "$\lambda_1$ distribution" )
    #Differenciated
    #plt.plot( Lambdas[0,:-1], Halos_Histogram[:,0]/np.sum(Halos_Histogram[:,0]),\
    #linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold] )
    #Integrated
    plt.plot( Lambdas[0,:-1], Halos_Histogram[:,0]/Halos_Histogram[0,0],\
    linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold] )
    
    #plt.plot( Lambdas[0,:-1], Isop_Histogram[:,0]/np.sum(Isop_Histogram[:,0]),\
    #linestyle = '--', color = Colors[i_fold], linewidth = Linewidths[i_fold] )
    #plt.plot( Lambdas[0,:-1], LG_Histogram[:,0]/np.sum(LG_Histogram[:,0]),\
    #linestyle = '-.', color = Colors[i_fold], linewidth = Linewidths[i_fold] )


    #Lambda 2 plot
    plt.subplot(132)
    plt.title( "$\lambda_2$ distribution" )
    #Differenciated
    #plt.plot( Lambdas[1,:-1], Halos_Histogram[:,1]/np.sum(Halos_Histogram[:,1]),\
    #linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold] )
    #Integrated
    plt.plot( Lambdas[1,:-1], Halos_Histogram[:,1]/Halos_Histogram[0,1],\
    linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold] )
    
    #plt.plot( Lambdas[1,:-1], Isop_Histogram[:,1]/np.sum(Isop_Histogram[:,1]),\
    #linestyle = '--', color = Colors[i_fold], linewidth = Linewidths[i_fold] )
    #plt.plot( Lambdas[1,:-1], LG_Histogram[:,1]/np.sum(LG_Histogram[:,1]),\
    #linestyle = '-.', color = Colors[i_fold], linewidth = Linewidths[i_fold] )


    #Lambda 3 plot
    plt.subplot(133)
    plt.title( "$\lambda_3$ distribution" )
    #Differenciated
    #plt.plot( Lambdas[2,:-1], Halos_Histogram[:,2]/np.sum(Halos_Histogram[:,2]),\
    #linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold] )
    #Integrated
    plt.plot( Lambdas[2,:-1], Halos_Histogram[:,2]/Halos_Histogram[0,2],\
    linestyle = '-', color = Colors[i_fold], linewidth = Linewidths[i_fold] )
    
    #plt.plot( Lambdas[2,:-1], Isop_Histogram[:,2]/np.sum(Isop_Histogram[:,2]),\
    #linestyle = '--', color = Colors[i_fold], linewidth = Linewidths[i_fold] )
    #plt.plot( Lambdas[2,:-1], LG_Histogram[:,2]/np.sum(LG_Histogram[:,2]),\
    #linestyle = '-.', color = Colors[i_fold], linewidth = Linewidths[i_fold] )
    #plt.plot( [-1,-1], linestyle = '-', color = Colors[i_fold], label = labels[i_fold] )
    
    i_fold += 1
    

plt.subplot(131)    
plt.plot( [-1,-1], linestyle = '-',color = 'black', label = 'Halos Sample', linewidth = 3 )
plt.plot( [-1,-1], linestyle = '--',color = 'black', label = 'Isolated pairs Sample', linewidth = 3 )
plt.plot( [-1,-1], linestyle = '-.',color = 'black', label = 'LG Sample', linewidth = 3 )
plt.xlabel( "$\lambda_1$" )
plt.ylabel( "Fraction" )
plt.yticks(np.linspace(0,1,11),np.linspace(0,1,11))
#plt.ylim( (0,1) )
plt.ylim( (0,0.15) )
#plt.xlim( (L_min,L_max) )
plt.xlim( (-0.5,2.0) )
plt.grid()
#plt.legend(loc='upper right')

plt.subplot(132)
plt.xlabel( "$\lambda_2$" )
plt.yticks(np.linspace(0,1,11),[''])
#plt.ylim( (0,1) )
plt.ylim( (0,0.15) )
#plt.xlim( (L_min,L_max) )
plt.xlim( (-1.0,1.0) )
plt.grid()

plt.subplot(133)
plt.xlabel( "$\lambda_3$" )
plt.yticks(np.linspace(0,1,11),[''])
#plt.ylim( (0,1) )
plt.ylim( (0,0.15) )
#plt.xlim( (L_min,L_max) )
plt.xlim( (-2.0,0.5) )
plt.grid()
plt.legend(labels, loc='upper right')

plt.savefig( "All_Lambda_Histogram", format = 'pdf')
plt.show()