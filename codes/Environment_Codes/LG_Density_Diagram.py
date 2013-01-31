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
Markers = ['','','','']


#==================================================================================================
#			CALCULATING ENVIROMENT DENSITY DIAGRAM
#==================================================================================================
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
    halos_envinroment = np.loadtxt("%s%s%d/Halos_Environment_s1.dat"%(foldglobal, fold, res[i_fold]))
    
    #Load Volume fraction respect to lambda_th for this simulation
    volumen_environment = np.loadtxt( "%s%s%d/Volume_s1.dat"%(foldglobal,fold,res[i_fold]) )[:,1:-1]
    
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
	#Density in each region
	plt.semilogy( lambda_thr, (number_isop_env[:,l]/volumen_environment[:,l])\
	/(np.sum(number_isop_env[0,:])/np.sum(volumen_environment[0,:])), 'o-', color = Colors[l], label = "%s"%env_labels[l] )

    plt.title('Density of LG pairs respect to environment total volume')
    plt.ylabel('Density [%1.3e Number of LG Pairs/Box Volume]'%(np.sum(number_isop_env[0,:])/np.sum(volumen_environment[0,:])))
    plt.xlabel('$\Lambda_{th}$')
    plt.text( 0.9, 60, labels[i_fold] )
    #plt.legend( bbox_to_anchor=(0., 1.1, 1., 0.0), borderaxespad=0, loc='upper left', ncol=4, mode="expand", handlelength=2, labelspacing=0)
    plt.legend( loc='upper left' )
    plt.hlines( 1, 0,1, linewidth = 2, linestyle = '--', color='black' )
    plt.grid()
    plt.ylim( (1e-2,100) )
    
    plt.savefig('LG_Diagram_Density(%s_%d).pdf'%(labels[i_fold], res[i_fold]), format = 'pdf')
	    
    i_fold += 1