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
scheme = 'Tweb/'
#Simulation
folds = [ "BOLSHOI/","CLUES/16953/", "CLUES/2710/", "CLUES/10909/", "BOLSHOI/"]
#Resolutions
res = [256, 64, 64, 64, 512]


#==================================================================================================
#			CALCULATING LG SAMPLE
#==================================================================================================
#Loading 
Lambda_Range = np.loadtxt('%sLG_definition_Vweb_s1.dat'%foldglobal)

i_fold = 0
for fold in folds:
    print '\nCurrently in ', fold
        
    #Loading environment of each halo
    halos_envinroment = np.loadtxt("%s%s%s%d/Halos_Environment_s1_BDM.dat"%(foldglobal, fold, scheme, res[i_fold]))
    
    #Isolated Pairs datas
    isop = np.transpose( np.loadtxt( '%s%sIsoPairs_catalog_BDM.dat'%(foldglobal,fold) ) )
    Nisop = len(isop[0])		#Number of isolated pairs
    
    Index = []
    for i_iso in xrange(Nisop):
	i1 = isop[1, i_iso] - 1
	i2 = isop[4, i_iso] - 1
	Condition = True
	
	for l in xrange(3):
	    if Lambda_Range[l][0] <= halos_envinroment[i1][l] and halos_envinroment[i1][l] <= Lambda_Range[l][1] and\
	    Lambda_Range[l][0] <= halos_envinroment[i2][l] and halos_envinroment[i2][l] <= Lambda_Range[l][1] and\
	    Condition == True:
		Condition = True
	    else:	
		Condition = False
		
	if Condition == True:
	    Index.append(i_iso)

    np.savetxt('%s%s%s%d/LG_catalog_s1.dat'%(foldglobal,fold,scheme,res[i_fold]), np.transpose(isop[:,Index]),\
    fmt="%d\t%d\t%1.4e\t%d\t%d\t%1.4e\t%d\t%4.3f\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%d\t%d" )

    i_fold += 1