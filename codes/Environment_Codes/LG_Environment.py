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
folds = [ "CLUES/16953/", "CLUES/2710/", "CLUES/10909/" ]
#Lambdas_Threshold
lambda_thr = np.linspace(0,1,21)
#Classification Scheme of environment
Scheme = 'Vweb/'
#Labels of graphs
labels = ["CLUES_16953","CLUES_2710", "CLUES_10909", "BOLSHOI"]
#Box lenght
Box_L = [64., 64., 64., 256.]
#Resolutions
res = [128, 128, 128, 256]
#Index of each LG halos
LG_index = [ [889,1107], [643,831], [675,895], False ]

#Colors array
Colors = ['red', 'green', 'blue', 'black']
#Enviroment Labels
env_labels = ['voids', 'sheets', 'filaments', 'knots']
#Linewidths
Linewidths = [1,1,1,2]
#Markers
Markers = ['o','s','>','']
#Differences
dif = [0, 0.1, 0.2, 0.3]

#==================================================================================================
#			CALCULATING ENVIRONMENT OF LG PAIR IN CLUES
#==================================================================================================
plt.figure(figsize=(16,8.5))
i_fold = 0
for fold in folds:
    print '\nCurrently in ', fold
        
    #Isolated Pairs datas
    isop = np.transpose( np.loadtxt( '%s%sIsoPairs_catalog.dat'%(foldglobal,fold) ) )
    Nisop = len(isop[0])		#Number of isolated pairs

    #Loading environment of each halo
    halos_envinroment = np.loadtxt("%s%s%s%d/Halos_Environment.dat"%(foldglobal, fold, Scheme, res[i_fold]))
    
    #Histogram of Halos in each environment
    LG_Environment = np.zeros( len(lambda_thr) )
    for i_lamb in xrange( len(lambda_thr) ):
	LG_Environment[i_lamb] = enviroment( halos_envinroment[LG_index[i_fold][0]-1], lambda_thr[i_lamb] )
		    
    #Plotting Environment
    plt.plot( lambda_thr, LG_Environment + dif[i_fold], color = Colors[i_fold], label = labels[i_fold], marker = Markers[i_fold] )
    plt.title('LG environment in CLUES')
    plt.ylabel('Environment')
    plt.xlabel('$\Lambda_{th}$')
    plt.yticks( [-1,0,1,2,3,4], ['', 'voids', 'sheets', 'filaments', 'knots', ''] )
    env_labels
    plt.legend( loc='upper left' )
    plt.grid()
    
    plt.savefig('LG_Environment.pdf', format = 'pdf')
	    
    i_fold += 1