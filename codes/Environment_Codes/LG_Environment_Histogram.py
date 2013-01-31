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
#Scheme of environment classification
scheme = 'Vweb/'
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
Linewidths = [1,1,1,2]
#Markers
Markers = ['','','','']
#Gaussian smoothing
smooth = '_s1'

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
    isop = np.transpose( np.loadtxt( '%s%s%s%d/LG_catalog%s.dat'%(foldglobal, fold, scheme, res[i_fold], smooth) ) )
    Nisop = len(isop[0])		#Number of isolated pairs

    #Loading environment of each halo
    halos_envinroment = np.loadtxt("%s%s%s%d/Halos_Environment%s.dat"%(foldglobal, fold, scheme, res[i_fold], smooth))
    
    #Load Volume fraction respect to lambda_th for this simulation
    volumen_environment = np.loadtxt( "%s%s%s%d/Volume%s.dat"%(foldglobal,fold, scheme, res[i_fold], smooth) )[:,1:-1]
    
    #Histogram of Halos in each environment
    number_isop_env = np.ones((len(lambda_thr), 4))
    for i_lamb in xrange( len(lambda_thr) ):
	for i_iso in xrange(Nisop):
	    for l in xrange(4):
		if enviroment( halos_envinroment[isop[1,i_iso]-1], lambda_thr[i_lamb] ) == l:
		    number_isop_env[i_lamb, l] += 1
		    
    #Plotting Environment
    plt.figure(figsize=(16,8.5))
    for l in xrange(4):
	#Number in each region
	plt.plot( lambda_thr, (number_isop_env[:,l])\
	/(1.0*np.sum(number_isop_env[0,:])), 'o-', color = Colors[l], label = "LGs fraction in%s"%env_labels[l] )
	#Volume fraction in each region
	plt.plot( lambda_thr, volumen_environment[:,l]/(1.0*np.sum(volumen_environment[0,:])),\
	's--', color = Colors[l], label = "Volume in %s"%env_labels[l] )


    #plt.title('Histogram of LG pair numbers respect to environment total volume')
    plt.ylabel('Fraction of LG pairs [%1.3e Number of LG Pairs]'%(np.sum(number_isop_env[0,:])))
    plt.xlabel('$\Lambda_{th}$')
    plt.text( 0.9, 0.9, labels[i_fold] )
    plt.legend( bbox_to_anchor=(0., 1.1, 1., 0.0), borderaxespad=0, loc='upper left', ncol=4, mode="expand", handlelength=2, labelspacing=0)
    #plt.legend( loc='upper left' )
    plt.hlines( 1, 0,1, linewidth = 2, linestyle = '--', color='black' )
    plt.grid()
    plt.ylim( (0,1) )
    
    plt.twinx()
    plt.ylabel('Volume fraction in each environment', rotation = 270)    
    plt.grid()    
    
    plt.savefig('LG_Number_Histogram(%s_%d)%s.pdf'%(labels[i_fold], res[i_fold], smooth), format = 'pdf')
	    
    i_fold += 1