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

#==================================================================================================
#			FUNCTIONS
#==================================================================================================
def read_CIC_scalar(filename, double=False):
    f = open(filename, "rb")
    dumb = f.read(38)

    dumb = f.read(4)
    n_x = f.read(4)
    n_y = f.read(4)
    n_z = f.read(4)
    nodes = f.read(4)
    x0 = f.read(4)
    y0 = f.read(4)
    z0 = f.read(4)
    dx = f.read(4)
    dy = f.read(4)
    dz = f.read(4)
    dumb = f.read(4)

    n_x = (unpack('i', n_x))[0]
    n_y = (unpack('i', n_y))[0]
    n_z = (unpack('i', n_z))[0]
    nodes = (unpack('i', nodes))[0]
    dx = (unpack('f', dx))[0]
    dy = (unpack('f', dy))[0]
    dz = (unpack('f', dz))[0]
    x0 = (unpack('f', x0))[0]
    y0 = (unpack('f', y0))[0]
    z0 = (unpack('f', z0))[0]
    print n_x, n_y, n_z, nodes, dx, dy, dz

    total_nodes = n_x * n_y * n_z
    dumb = f.read(4)
    if(double==False):
        array_data = f.read(total_nodes*4)
        format_s = str(total_nodes)+'f'
    else:
        array_data = f.read(total_nodes*8)
        format_s = str(total_nodes)+'d'
    dumb = f.read(4)

    array_data = unpack(format_s, array_data)
    f.close()
    array_data  = np.array(array_data)
    new_array_data = np.reshape(array_data, (n_x,n_y,n_z), order='F')
    return new_array_data, n_x, dx


def enviroment_lambda( r ):
    '''
    FUNCTION: Return the local enviroment in a given r coordinate
    ARGUMENTS: r - Local coordinate
	       n - Number of lambda
    RETURN:   Enviroment
	      0 - Void
	      1 - Filament
	      2 - Knot
    '''
    i = np.int(r[0]/Box_lenght*n_x)
    j = np.int(r[1]/Box_lenght*n_x)
    k = np.int(r[2]/Box_lenght*n_x)
    
    return [lambda_val[0][i,j,k], lambda_val[1][i,j,k], lambda_val[2][i,j,k]]


#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Global Fold
#foldglobal = '../Data/'
foldglobal = './'
#Simulation
folds = [ "CLUES/16953/", "CLUES/2710/", "CLUES/10909/", "BOLSHOI/" ]
#Lambda_Filename
#eigen_file = [ "snap_190.eigen_", "snap_191.eigen_", "snap_190.eigen_", "PMcrsFULL.0416.DAT.eigen_" ]
eigen_file = [ "snap_191.s1.00.eigen_", "snap_191.s1.00.eigen_", "snap_190.s1.00.eigen_", "PMcrsFULL.0416.DAT.s1.00.eigen_" ]
#Resolutions of each simulation
res = [ 128, 128, 128, 512 ]
#Box lenghts of each simulation
Box_L = [ 64, 64, 64, 256 ]


#==================================================================================================
#			CALCULATING ENVIROMENT
#==================================================================================================
i_fold = 0
for fold in folds:
    print '\nCurrently in ', fold
    
    #Loading Lambda Files for each simulation
    lambda_val = []
    for i in xrange(0,3):
	lv,n_x,dx =read_CIC_scalar("%s%s%d/%s%d"%(foldglobal, fold, res[i_fold], eigen_file[i_fold], i+1) )
	lambda_val.append( lv )

    #Current Box lenght
    Box_lenght = Box_L[i_fold]

    #Loading Halos Data
    halos = np.transpose( np.loadtxt( '%s%sHalos_catalog.dat'%(foldglobal,fold) ) )
    Nhalos = len(halos[0])		#Number of halos

    #Environment of each halo
    halos_envinroment = np.zeros( (Nhalos, 3) )

    for i in xrange(Nhalos):
	halos_envinroment[i] = enviroment_lambda( halos[1:4,i] )

    #Saving File
    np.savetxt("%s%s%d/Halos_Environment.dat"%(foldglobal, fold, res[i_fold]), halos_envinroment )
    
    i_fold += 1