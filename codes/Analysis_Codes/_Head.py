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
import matplotlib.gridspec as gridspec


#==================================================================================================
#			VARIABLES
#==================================================================================================
#Global Fold
foldglobal = '../../data/'



#==================================================================================================
#			FUNCTIONS
#==================================================================================================

#..................................................................................................
#Cutting Halos in X axe
#..................................................................................................
def CutHaloX( X, thick, datos, plot=True, color='black' ):
    #Initial data
    ncol = len(datos)		#Number of columns
    nrow = len(datos[0])	#Number of rows
    Box_lenght = np.max( tuple(datos[1])+tuple(datos[2])+tuple(datos[3]) )#h^-1 Mpc

    
    #Sorting in x axe
    argx = list( np.argsort( datos[1] ) )
    for i in xrange(0, ncol):
	datos[i] = datos[i][argx]
    
    if X<=thick:
	i_star = 0
    else:
	i_star = int(Box_lenght/(X - thick))
    
    i1 = 0
    i2 = -1
    for i in xrange(i_star,nrow):
	if datos[1][i] >= X and i1==0:
	    i1 = i
	if datos[1][i] >= X + thick and i2==-1:
	    i2 = i
	    break

    #Plotting results
    if plot == True:
	plt.title('Cut in X axes between %3.1f and %3.1f'%(X, X + thick))
	plt.plot( datos[2][i1:i2], datos[3][i1:i2], '.', color=color )
	plt.xlim( (0,Box_lenght) )
	plt.ylim( (0,Box_lenght) )
	plt.xlabel('y [$h^{-1}$Mpc]')
	plt.ylabel('z [$h^{-1}$Mpc]')
	plt.show()
    else:
	return [datos[2][i1:i2], datos[3][i1:i2]]


#..................................................................................................
#Cutting Halos in Y axe 
#..................................................................................................
def CutHaloY( Y, thick, datos, plot=True, color='black' ):
    #Initial data
    ncol = len(datos)		#Number of columns
    nrow = len(datos[0])	#Number of rows
    Box_lenght = np.max( tuple(datos[1])+tuple(datos[2])+tuple(datos[3]) )#h^-1 Mpc
  
    #Sorting in x axe
    argx = list( np.argsort( datos[2] ) )
    for i in xrange(0, ncol):
	datos[i] = datos[i][argx]
    
    if Y<=thick:
	i_star = 0
    else:
	i_star = int(Box_lenght/(Y - thick))
    
    i1 = 0
    i2 = -1
    for i in xrange(i_star,nrow):
	if datos[2][i] >= Y and i1==0:
	    i1 = i
	if datos[2][i] >= Y + thick and i2==-1:
	    i2 = i
	    break

    #Plotting results	    
    if plot == True:    
	plt.title('Cut in Y axes between %3.1f and %3.1f'%(Y, Y + thick))
	plt.plot( datos[1][i1:i2], datos[3][i1:i2], '.', color=color )
	plt.xlim( (0,Box_lenght) )
	plt.ylim( (0,Box_lenght) )
	plt.xlabel('x [$h^{-1}$Mpc]')
	plt.ylabel('z [$h^{-1}$Mpc]')
	plt.show()
    else:
	return [datos[1][i1:i2], datos[3][i1:i2]]


#..................................................................................................
#Cutting Halos in Z axe
#..................................................................................................
def CutHaloZ( Z, thick, datos, plot=True, color='black' ):
    #Initial data
    ncol = len(datos)		#Number of columns
    nrow = len(datos[0])	#Number of rows
    Box_lenght = np.max( tuple(datos[1])+tuple(datos[2])+tuple(datos[3]) )#h^-1 Mpc

    #Sorting in x axe
    argx = list( np.argsort( datos[3] ) )
    for i in xrange(0, ncol):
	datos[i] = datos[i][argx]
    
    if Y<=thick:
	i_star = 0
    else:
	i_star = int(Box_lenght/(Z - thick))
    
    i1 = 0
    i2 = -1
    for i in xrange(i_star,nrow):
	if datos[3][i] >= Y and i1==0:
	    i1 = i
	if datos[3][i] >= Y + thick and i2==-1:
	    i2 = i
	    break

    #Plotting results	    
    if plot == True:    
	plt.title('Cut in Z axes between %3.1f and %3.1f'%(Y, Y + thick))
	plt.plot( datos[1][i1:i2], datos[2][i1:i2], '.', color=color )
	plt.xlim( (0,Box_lenght) )
	plt.ylim( (0,Box_lenght) )
	plt.xlabel('x [$h^{-1}$Mpc]')
	plt.ylabel('y [$h^{-1}$Mpc]')
	plt.show()
    else:
	return [datos[1][i1:i2], datos[3][i1:i2]]
	
	
	
#..................................................................................................
#Cutting Density field in Z axe
#..................................................................................................
def CutFieldZ( filename, X, res=32 ):
    os.system( "./Field_Cut%d.out %s %d temp.tmp"%( res, filename, X ) )
    datos = np.loadtxt( 'temp.tmp' )
    N = int(np.sqrt(len( datos )))
    datos = datos.reshape( (N, N) )
    os.system( "rm temp.tmp" )
    return datos
    
    
#..................................................................................................
#Correlation bewteen density and eigenvalues
#..................................................................................................
def Correlation( filename_eig, filename_delta, min_L, max_L, N_L ):
    os.system( "./Lambda_Correlation.out %s %s %f %f %d"%( 
    filename_eig, filename_delta, min_L, max_L, N_L ) )
    datos = np.transpose( np.loadtxt( 'correlation.dat' ) )
    os.system( "rm correlation.dat" )
    return datos
    
    
#..................................................................................................
#Classification Scheme
#..................................................................................................
def Scheme( eig1, eig2, eig3, Lamb ):
    N = len( eig1 )
    sch = 0*eig1
    
    for i in xrange(N):
	for j in xrange(N):
	    if eig1[i,j] > Lamb:
		sch[i,j] += 1
	    if eig2[i,j] > Lamb:
		sch[i,j] += 1
	    if eig3[i,j] > Lamb:
		sch[i,j] += 1
    return sch