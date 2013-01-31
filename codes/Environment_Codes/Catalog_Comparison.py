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

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Global Fold
foldglobal = '../Data/'
#Simulation
fold = "BOLSHOI/"


#==================================================================================================
#			CODE
#==================================================================================================
#General Pairs Data
pairs = np.transpose( np.loadtxt( '%s%sPairs_catalog.dat'%(foldglobal,fold) ) )
Npair = len(pairs[0])		#Number of pairs

#Isolated Pairs Data
isop = np.transpose( np.loadtxt( '%s%sIsoPairs_catalog.dat'%(foldglobal,fold) ) )
#isop = np.transpose( np.loadtxt( '%s%sPairs_catalog.dat'%(foldglobal,fold) ) )
Nisop = len(isop[0])		#Number of isolated pairs

#Index of altern catalog (Forero 2011)
isopJ = np.transpose( np.loadtxt( '%s%sIsoPairs_catalog_J.dat'%(foldglobal,fold) ) )
NisopJ = len(isopJ[0])		#Number of isolated pairs


#Number of coincidences respecto to isolated systems (Forero 2011 and own data)
N_coincidences = 0
#Comparison of numbers of isolated pairs
for i in xrange(Nisop):
    for j in xrange(NisopJ):
	if (isop[1,i] == isopJ[0,j] and isop[4,i] == isopJ[1,j]) or \
	  (isop[1,i] == isopJ[1,j] and isop[4,i] == isopJ[0,j]):
	    N_coincidences += 1
    
