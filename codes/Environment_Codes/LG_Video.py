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

import halo_cuts as HC

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Global Fold
foldglobal = '../Data/'
#Data filename
folds=["CLUES/16953/","CLUES/2710/", "CLUES/10909/"]
#Labels of each Simulation
labels=["CLUES 16953","CLUES 2710", "CLUES 10909"]
#Lambda files
lambda_thr = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6,\
0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0,1.1, 1.2]
#LG index in each simulation
LG_index = [ [889,1107], [643,831], [675,895] ]

#Resolution
n_x = 128
#Subplots options
subplot = ['221','222','223','224']
#Box_lenght
Box_lenght = 64.
#Extent in imshow graphic
extent = [0, Box_lenght, 0, Box_lenght]
#Colors
Colors = ['red', 'green', 'blue', 'black']
jet3 = plt.cm.get_cmap('jet', 3)

#==================================================================================================
#			CALCULATING ENVIROMENT
#==================================================================================================
i_thr = 0
for n in xrange(0,len(lambda_thr)):
    #Image size
    plt.figure( figsize=(12,12) )
    
    #Sweeping in CLUES's
    i_fold = 0
    for fold in folds:	    
	plt.subplot(subplot[i_fold])
	#==========================================================================================
	#			HALOS AND ENVIRONMENT DATA
	#==========================================================================================
	#Halos Datas
	halos = np.transpose( np.loadtxt( '%s%sHalos_catalog.dat'%(foldglobal,fold) ) )
	Nhalos = len(halos[0])		#Number of halos
	
	#Environment data
	datos = np.loadtxt( "%s%s%d/enviroment_Lamb_%1.2f.dat"%(foldglobal,fold,n_x,lambda_thr[n]) )
	enviroment = datos.reshape([n_x,n_x,n_x])

	#==========================================================================================
	#			LOCAL GROUP OF CURRENT SIMULATION
	#==========================================================================================
	i_xLG = int( (halos[1,LG_index[i_fold][1]]/Box_lenght)*n_x )
	
	#[y,z] positions for LG halos
	Y_01 = [ halos[2,  LG_index[i_fold][0]-1  ], halos[2,  LG_index[i_fold][1]-1  ] ]
	Z_01 = [ halos[3,  LG_index[i_fold][0]-1  ], halos[3,  LG_index[i_fold][1]-1  ] ]
	
	#==========================================================================================
	#			PICTURES OF VIDEO
	#==========================================================================================
	plt.imshow( np.transpose(enviroment[i_xLG,:,::-1]), extent=extent, vmin=0, vmax=2, cmap = jet3 )
	plt.plot( Y_01, Z_01, 'o', color = Colors[i_fold], markersize = 10 )
	    
	plt.xlim( (0,Box_lenght) )
	plt.ylim( (0,Box_lenght) )
	plt.title( "%s\t$\lambda_{thr}$ = %1.2f, x=%1.2f"%(labels[i_fold],lambda_thr[n],halos[1,LG_index[i_fold][1]]) )
	plt.xlabel('y [$h^{-1}$Mpc]')
	plt.ylabel('z [$h^{-1}$Mpc]')
	
	i_fold += 1
	
    plt.subplot('224')
    plt.imshow( np.transpose([[0,1,2],[0,1,2],[0,1,2]]), vmin=0, vmax=2, cmap = jet3 )
    plt.xticks( [0], '' )
    plt.yticks( [0], '' )
    plt.text(0.5,2.0, 'FILAMENT', fontsize=18, color = 'white')
    plt.text(0.5,1.0, '  SHEET ', fontsize=18, color = 'black')
    plt.text(0.5,0.0, '  VOID  ', fontsize=18, color = 'white')
	
    fname='_tmp-%03d.png'%i_thr
    plt.savefig(fname)
    plt.close()
    i_thr += 1
    print 'n_thr', i_thr

print 'Making movie animation.mpg - this make take a while'
os.system("ffmpeg -qscale 1 -r 10 -b 9600 -i _tmp-%03d.png  video.mp4")

os.system('rm -rf *.png')