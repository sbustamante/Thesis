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
#Scheme of environment classification
scheme = 'Vweb/'
#Simulation
folds = [ "CLUES/16953/", "CLUES/2710/", "CLUES/10909/"]
#Labels of graphs
labels = ["CLUES_16953","CLUES_2710", "CLUES_10909", "BOLSHOI", "BOLSHOI"]
#Resolutions
res = [64, 64, 64, 512, 256]
#Index of each LG halos
LG_index = [ [889,1107], [643,831], [675,895], False, False ]


#==================================================================================================
#			CALCULATING LAMBDA PROPERTIES DEFINITION
#==================================================================================================
#Lambda_Range
Lambda_Range = [ [False,False], [False,False], [False,False] ]

i_fold = 0
for fold in folds:
    print '\nCurrently in ', fold
    
    #Loading environment of each halo
    halos_envinroment = np.loadtxt("%s%s%s%d/Halos_Environment_s1.dat"%(foldglobal, fold, scheme, res[i_fold]))
    
    #Ranges in each EigenValues of LG sample
    for i in xrange(3):
	print LG_index[i_fold][0], i, halos_envinroment[ LG_index[i_fold][0]-1 ][i], LG_index[i_fold][1], halos_envinroment[ LG_index[i_fold][1]-1 ][i]
      
	#Minim Value in Range
	if Lambda_Range[i][0] == False:
	    Lambda_Range[i][0] = np.min( (halos_envinroment[ LG_index[i_fold][0]-1 ][i],\
					 halos_envinroment[ LG_index[i_fold][1]-1 ][i]) )
	else:
	    Lambda_Range[i][0] = np.min( (halos_envinroment[ LG_index[i_fold][0]-1 ][i],\
					 halos_envinroment[ LG_index[i_fold][1]-1 ][i],\
					 Lambda_Range[i][0]) )
	#Maxim Value in Range
	if Lambda_Range[i][1] == False:
	    Lambda_Range[i][1] = np.max( (halos_envinroment[ LG_index[i_fold][0]-1 ][i],\
					 halos_envinroment[ LG_index[i_fold][1]-1 ][i]) )
	else:
	    Lambda_Range[i][1] = np.max( (halos_envinroment[ LG_index[i_fold][0]-1 ][i],\
					 halos_envinroment[ LG_index[i_fold][1]-1 ][i],\
					 Lambda_Range[i][1]) )
    i_fold += 1
	    
np.savetxt('LG_definition.dat', Lambda_Range)