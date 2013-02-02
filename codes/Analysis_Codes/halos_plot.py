execfile('_head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = [ "CLUES/16953/", "CLUES/2710/", "CLUES/10909/", "BOLSHOI/" ]
#Labels of graphs
labels = ["CLUES_16953","CLUES_2710", "CLUES_10909", "BOLSHOI"]
#Box lenght
Box_L = [64., 64., 64., 256.]
#Number of sections
N_sec = [64, 64, 64, 256]


#==================================================================================================
#			CALCULATING ENVIROMENT DENSITY DIAGRAM
#==================================================================================================
i_fold = 0
for fold in folds:
    print '\nCurrently in ', fold
    #Color Diagram
    Colors = np.linspace( 1, 0, N_sec[i_fold] )
    
    #Loading Halos Data
    halos = np.transpose( np.loadtxt( '%s%sHalos_catalog.dat'%(foldglobal,fold) ) )
    Nhalos = len(halos[0])		#Number of halos

    #Plotting cuts
    for i in xrange( N_sec[i_fold] ):
	x = i*Box_L[i_fold]/(1.0*N_sec[i_fold])
	dx = Box_L[i_fold]/(1.0*N_sec[i_fold])
	
	Y, Z = HC.CutX( x, dx, halos, plot = False )
	#plt.plot( Y, Z, '.', color = ( Colors[i]**(1/1.7), Colors[i]**(1/1.7), Colors[i]**(1/1.7) ), markersize = 6 )
	plt.plot( Y, Z, '.', color = ( np.sqrt(Colors[i]), np.sqrt(Colors[i]), np.sqrt(Colors[i]) ), markersize = 6 )
	plt.xlim( (0,Box_L[i_fold] ) )
	plt.ylim( (0,Box_L[i_fold] ) )

    plt.xlabel('y [$h^{-1}$Mpc]')
    plt.ylabel('z [$h^{-1}$Mpc]')
    plt.title( 'Spatial distribution of dark matter halos (%s)'%labels[i_fold] )
    plt.savefig( "Halos_Spatial_Distribution(%s).png"%labels[i_fold], filetype = 'png' )
    plt.close('all')
    i_fold += 1