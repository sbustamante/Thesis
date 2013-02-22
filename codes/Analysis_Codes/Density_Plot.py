execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = [ "BOLSHOI/" ]
#Labels of graphs
labels = [ "BOLSHOI" ]
#Web type
webtype = 'Vweb/'
#Box lenght
Box_L = [ 256. ]
#Number of sections
N_sec = [ 256 ]
#Smooth parameter
smooth = '_s1'


#==================================================================================================
#			CALCULATING PLOT OF HALOS
#==================================================================================================
i_fold = 0
for fold in folds:
    print '\nCurrently in ', fold
    
    n = N_sec[i_fold]
    
    #Loading Density Data
    delta = np.transpose( np.loadtxt( '%s%s%s%d/density_sign%s.dat'%(foldglobal,fold,webtype,n,smooth), 
    dtype = int ) )
    delta = np.reshape( (n,n,n) )


    plt.xlabel('y [$h^{-1}$Mpc]')
    plt.ylabel('z [$h^{-1}$Mpc]')
    plt.title( 'Spatial distribution of dark matter halos (%s)'%labels[i_fold] )
    plt.savefig( "Halos_Spatial_Distribution(%s).png"%labels[i_fold], filetype = 'png' )
    plt.close('all')
    i_fold += 1