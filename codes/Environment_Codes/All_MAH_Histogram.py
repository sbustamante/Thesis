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
Linewidths = [0.5,0.5,0.5,2]
#Markers
Markers = ['','','','']

#Numbers of division for lambdas
N_lambda = 50
#Values in lambda interval
L_min = -2
L_max = 2
#Time intervals to MAH Histograms
int_MAH = 20
T_min = 0
T_max = 0.134331E+02
#Threshold time in T_track value
T_th_track = 13.0

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
    lgsamp = np.transpose( np.loadtxt( '%s%sLG_catalog.dat'%(foldglobal,fold) ) )
    Nlg = len(lgsamp[0])		#Number of isolated pairs
    
    #Loading environment of each halo
    halos_envinroment = np.loadtxt("%s%s%d/Halos_Environment.dat"%(foldglobal, fold, res[i_fold]))
    
    #Loading Mass Acretion Histories
    halos_MAH = np.transpose(np.loadtxt("%s%s/MAH.dat"%(foldglobal, fold)) )
    N_MAH = len( halos_MAH[0] )
    
    #Times Histograms
    Halos_MAH_hist = np.zeros( (3,int_MAH) )
    Isop_MAH_hist = np.zeros( (3,int_MAH) )
    LG_MAH_hist = np.zeros( (3,int_MAH) )
    #Time Interval
    Times = np.linspace( T_min, T_max, int_MAH+1 )
    
    for i_MAH in xrange( int_MAH ):
	for l in xrange( 3 ):
	    #Halos Histogram
	    for i_hal in xrange( N_MAH ):
		if halos_MAH[l+2,i_hal] > Times[i_MAH] and \
		halos_MAH[5,i_hal] > T_th_track and \
		halos_MAH[5,i_hal] != -1:
		    Halos_MAH_hist[l,i_MAH] += 1
		    
	    #Isolated Pairs Histogram
	    for i_iso in xrange( Nisop ):
		i1 = isop[1,i_iso] - 1
		i2 = isop[4,i_iso] - 1
		#Halo 1
		if halos_MAH[l+2,i1] > Times[i_MAH] and \
		halos_MAH[5,i1] > T_th_track and \
		halos_MAH[5,i1] != -1:
		    Isop_MAH_hist[l,i_MAH] += 1
  		#Halo 2
		if halos_MAH[l+2,i2] > Times[i_MAH] and \
		halos_MAH[5,i2] > T_th_track and \
		halos_MAH[5,i2] != -1:
		    Isop_MAH_hist[l,i_MAH] += 1
		    
	    #LG sample Histogram
	    for i_lg in xrange( Nlg ):
		i1 = lgsamp[1,i_lg] - 1
		i2 = lgsamp[4,i_lg] - 1
		#Halo 1
		if  halos_MAH[l+2,i1] > Times[i_MAH] and \
		halos_MAH[5,i1] > T_th_track and \
		halos_MAH[5,i1] != -1:
		    LG_MAH_hist[l,i_MAH] += 1
  		#Halo 2
		if  halos_MAH[l+2,i2] > Times[i_MAH] and \
		halos_MAH[5,i2] > T_th_track and \
		halos_MAH[5,i2] != -1:
		    LG_MAH_hist[l,i_MAH] += 1
		    
    #TREE_T_FORM
    plt.subplot(131)
    plt.plot( Times[:-1], Halos_MAH_hist[0]/np.sum(Halos_MAH_hist[0,0]), linestyle = '-', label = 'Halos Sample' )
    plt.plot( Times[:-1], Isop_MAH_hist[0]/np.sum(Isop_MAH_hist[0,0]), linestyle = '--', label = 'Isolated Pairs Sample' )
    plt.plot( Times[:-1], LG_MAH_hist[0]/np.sum(LG_MAH_hist[0,0]), linestyle = '-.', label = 'LG Sample' )
    plt.title("$t_{form}$")
    plt.ylabel("Fraction")
    plt.xlabel("Time [Gyr]")
    plt.legend(loc='lower left')
    plt.grid()
    
    #TREE_T_ASSEMBLY
    plt.subplot(132)
    plt.plot( Times[:-1], Halos_MAH_hist[1]/np.sum(Halos_MAH_hist[1,0]), linestyle = '-' )
    plt.plot( Times[:-1], Isop_MAH_hist[1]/np.sum(Isop_MAH_hist[1,0]), linestyle = '--' )
    plt.plot( Times[:-1], LG_MAH_hist[1]/np.sum(LG_MAH_hist[1,0]), linestyle = '-.' )
    plt.title("$t_{assembly}$")
    plt.ylabel("Fraction")
    plt.xlabel("Time [Gyr]")
    plt.grid()
    
    #TREE_T_MERGER
    plt.subplot(133)
    plt.plot( Times[:-1], Halos_MAH_hist[2]/np.sum(Halos_MAH_hist[2,0]), linestyle = '-' )
    plt.plot( Times[:-1], Isop_MAH_hist[2]/np.sum(Isop_MAH_hist[2,0]), linestyle = '--' )
    plt.plot( Times[:-1], LG_MAH_hist[2]/np.sum(LG_MAH_hist[2,0]), linestyle = '-.' )
    plt.title("$t_{merger}$")
    plt.ylabel("Fraction")
    plt.xlabel("Time [Gyr]")
    plt.grid()
    
plt.savefig("All_MAH_Histogram.pdf", filetype='pdf')
plt.show()