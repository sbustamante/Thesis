# -*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import sys
import matplotlib.pylab as plt
import os

#==================================================================================================
#			FUNCTIONS
#==================================================================================================
#Cutting in X axe
def CutX( X, thick, ii, plot=True, color='black' ):
    #Sorting in x axe
    argx = list( np.argsort( datos[1] ) )
    for i in xrange(0, ncol):
	datos[i] = datos[i][argx]
    for i in xrange(0, 3):
	halos_envinroment[i] = halos_envinroment[i][argx]
    
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
	    
    for i in xrange(i1,i2):
	env = 0
	for l in xrange(3):
	    if halos_envinroment[l][i] >=  lambda_thr:
		env += 1
	lambda_grid[ int(datos[2][i]*Nres/Box_lenght) , int(datos[3][i]*Nres/Box_lenght) ] = env
	    
    #Plotting results
    extent = [0, Box_lenght, 0, Box_lenght]
    jet3 = plt.cm.get_cmap('jet', 4)
    
    if plot == True:
	plt.title('Cut in X axes between %3.1f and %3.1f'%(X, X + thick))
	plt.imshow( np.transpose(lambda_grid[:,::-1]), extent=extent, vmin=0, vmax=3, cmap = jet3 )
	plt.colorbar()
	plt.plot( datos[2][i1:i2], datos[3][i1:i2], '.', color=color, markersize=2.0 )
	plt.xlim( (0,Box_lenght) )
	plt.ylim( (0,Box_lenght) )
	plt.xlabel('y [$h^{-1}$Mpc]')
	plt.ylabel('z [$h^{-1}$Mpc]')
	fname='_tmp-%03d.png'%ii
	plt.savefig(fname)
	plt.close()
    else:
	return [datos[2][i1:i2], datos[3][i1:i2]]


#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Global Fold
foldglobal = '../Data/'
#Simulation
folds = [ "CLUES/16953/", "CLUES/2710/", "CLUES/10909/", "BOLSHOI/" ]
#Lambdas_Threshold
lambda_thr = 0.3
#Classification Scheme of environment
Scheme = 'Tweb/'
#Labels of graphs
labels = ["CLUES_16953","CLUES_2710", "CLUES_10909", "BOLSHOI"]
#Box lenght
Box_L = [64., 64., 64., 256.]
#Resolutions
res = [128, 128, 128, 512]
#Grid resolution
Gres = np.array([128, 128, 128, 512/2])/2
#Gaussian smoothing of 1-cell
smooth = ""

#==================================================================================================
#			VIDEO GENERATION
#==================================================================================================
i_fold = 0
for fold in folds:
    #if fold != 'BOLSHOI/':
	#i_fold += 1
	#continue
      
    print '\nCurrently in ', fold
    
    #Loading Halos Data
    datos = np.transpose( np.loadtxt( '%s%sHalos_catalog.dat'%(foldglobal,fold) ) )
    nrow = len(datos[0])		#Number of columns
    ncol = len(datos)			#Number of rows
    
    #Current box lenght
    Box_lenght = Box_L[i_fold]
    #Resolution
    Nres = Gres[i_fold]

    #Loading environment of each halo
    halos_envinroment = np.transpose(np.loadtxt("%s%s%s%d/Halos_Environment%s.dat"%(foldglobal, fold, Scheme, res[i_fold], smooth)))
    
    #Video Construction
    for i in xrange(Nres):
	#Environment Scheme
	lambda_grid = np.zeros( (Nres, Nres) )
	X = Box_lenght*i/Nres
	CutX( X, Box_lenght/Nres, i )
	
    print 'Making movie animation.mpg - this make take a while'
    os.system("ffmpeg -qscale 1 -r 5 -b 9600 -i _tmp-%03d.png  video.mp4")
    os.system("mv video.mp4 ./video_%s.mp4"%(labels[i_fold]))
    os.system('rm -rf *.png')
    i_fold += 1