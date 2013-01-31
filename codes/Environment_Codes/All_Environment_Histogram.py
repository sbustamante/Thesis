'''********************************************************
This code calculate environment histograms for Bolshoi 
simulation, based in general halos catalog of simulation,
isolated pairs constructed catalog and finally the LG 
catalog constructed based in constrained simulations CLUES.
The final results are four graphics for each environment 
type (knots, filaments, sheets and voids), when it's
plotted the general halos and isolates pairs distributions
with the numbers of objects in each respective environment,
this with the porpuse of comparison. Finally it's also 
plotted the environment distribution of Bolshoi LG sample
and some random samples with the same size of LG, with the
aim of discarding variance effects by selection process
********************************************************'''


#==========================================================
#	HEADERS
#==========================================================
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


#==========================================================
#	PARAMETERS
#==========================================================
#Global Fold
foldglobal = '../Data/'
#Simulation
folds = "BOLSHOI/"
#Lambdas_Threshold
lambda_thr = np.linspace(0,1,21)
#Labels of graph
labels = "BOLSHOI"
#Box lenght
Box_L = 256
#Resolution
res = 512
#Number of random sample in isolated pairs catalog
N_rand = 20

#Colors array
Colors = ['red', 'green', 'blue', 'black']
#Enviroment Labels
env_labels = ['voids', 'sheets', 'filaments', 'knots']
#Linewidths
Linewidths = [1,1,1,2]
#Markers
Markers = ['','','','']


#==========================================================
#	CALCULATING HISTOGRAM OF SAMPLES
#==========================================================
i_fold = 0
for fold in folds:
    #......................................................
    #	Loading external data
    #......................................................
    #Loading Halos Data
    halos = np.transpose( np.loadtxt( '%s%sHalos_catalog.dat'%(foldglobal,fold) ) )
    Nhalos = len(halos[0])		#Number of halos
    #Isolated Pairs datas
    isop = np.transpose( np.loadtxt( '%s%sIsoPairs_catalog.dat'%(foldglobal,fold) ) )
    Nisop = len(isop[0])		#Number of isolated pairs
    #LG Pairs datas
    lg_smp = np.transpose( np.loadtxt( '%s%sLG_catalog.dat'%(foldglobal,fold) ) )
    Nlg_smp = len(lg_smp[0])		#Number of isolated pairs
    #Loading environment of each halo
    halos_envinroment = np.loadtxt("%s%s%d/Halos_Environment_s1.dat"%(foldglobal, fold, res[i_fold]))
    #Load Volume fraction respect to lambda_th for this simulation
    volumen_environment = np.loadtxt( "%s%s%d/Volume_s1.dat"%(foldglobal,fold,res[i_fold]) )[:,1:-1]

    #......................................................
    #	Loading external data
    #......................................................
    #Histogram of Halos in each environment
    number_isop_env = np.ones((len(lambda_thr), 4))
    for i_lamb in xrange( len(lambda_thr) ):
	for i_iso in xrange(Nisop):
	    for l in xrange(4):
		if enviroment( halos_envinroment[isop[1,i_iso]-1], lambda_thr[i_lamb] ) == l:
		    number_isop_env[i_lamb, l] += 1


    #......................................................
    #	Constructing random samples
    #......................................................
    
    

		    
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
    
    
    plt.savefig('LG_Number_Histogram(%s_%d).pdf'%(labels[i_fold], res[i_fold]), format = 'pdf')
	    
    i_fold += 1