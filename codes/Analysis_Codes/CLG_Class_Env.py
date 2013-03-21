execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/"]
#Number of sections
N_sec = [256]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Vweb'

#Environmet Histogram
L2D = '1'


#==================================================================================================
#			CONSTRUCTING EIGENVALUES 1D HISTOGRAMS
#==================================================================================================

i_fold = 0
N_sim = len(folds)

plt.figure( figsize=(4.5*2,3*2.3) )
for fold in folds:
    print fold

    #Loading environment properties of halos
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
            
    #Loading CLG Pairs Systems
    CLG = np.transpose(np.loadtxt('%s%s/C_CLG_%s.dat'%(foldglobal,fold, catalog)))
    
    #Loading IP Pairs Systems
    IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
    
    EnvBL1 = eig[ 1,[CLG[1]-1] ][0]
    EnvBL2 = eig[ 2,[CLG[1]-1] ][0]
    EnvBL3 = eig[ 3,[CLG[1]-1] ][0]
    
    EnvBL1_IP = eig[ 1,[IP[1]-1] ][0]
    EnvBL2_IP = eig[ 2,[IP[1]-1] ][0]
    EnvBL3_IP = eig[ 3,[IP[1]-1] ][0]
    
    L_th, Nc_CLG = Scheme1D( EnvBL1, EnvBL2, EnvBL3, 0.0, 1.0, 100 )
    L_th, Nc_IP  = Scheme1D( EnvBL1_IP, EnvBL2_IP, EnvBL3_IP, 0.0, 1.0, 100 )
    L_th, Nc_GH  = Scheme1D( eig[1], eig[2], eig[3], 0.0, 1.0, 100 )
      
    plt.subplot( 2,2,1 )
    plt.plot( L_th, Nc_GH[0,:]/np.sum(Nc_GH[:,0]), '--', color = 'gray', linewidth = 2)
    plt.plot( L_th, Nc_IP[0,:]/np.sum(Nc_IP[:,0]), color = 'black', linewidth = 3 )
    plt.plot( L_th, Nc_CLG[0,:]/np.sum(Nc_CLG[:,0]), color = 'blue', linewidth = 2 )

    
    plt.subplot( 2,2,2 )
    plt.plot( L_th, Nc_GH[1,:]/np.sum(Nc_GH[:,0]), '--', color = 'gray', linewidth = 2,
    label='GH Sample' )
    plt.plot( L_th, Nc_IP[1,:]/np.sum(Nc_IP[:,0]), color = 'black', linewidth = 3,
    label='IP Sample')
    plt.plot( L_th, Nc_CLG[1,:]/np.sum(Nc_CLG[:,0]), color = 'blue', linewidth = 2,
    label='CLG Sample' )
    
    plt.subplot( 2,2,3 )
    plt.plot( L_th, Nc_GH[2,:]/np.sum(Nc_GH[:,0]), '--', color = 'gray', linewidth = 2)
    plt.plot( L_th, Nc_IP[2,:]/np.sum(Nc_IP[:,0]), color = 'black', linewidth = 3 )
    plt.plot( L_th, Nc_CLG[2,:]/np.sum(Nc_CLG[:,0]), color = 'blue', linewidth = 2 )

    plt.subplot( 2,2,4 )
    plt.plot( L_th, Nc_GH[3,:]/np.sum(Nc_GH[:,0]), '--', color = 'gray', linewidth = 2)
    plt.plot( L_th, Nc_IP[3,:]/np.sum(Nc_IP[:,0]), color = 'black', linewidth = 3 )
    plt.plot( L_th, Nc_CLG[3,:]/np.sum(Nc_CLG[:,0]), color = 'blue', linewidth = 2 )

    i_fold += 1


#plt.subplots_adjust( bottom = 0.08, top = 0.97 )

#Mean Density
plt.subplot( 2,2,1 )
#plt.title(" Pairs fraction in regions")
plt.ylabel( "Number fraction" )
plt.grid()
plt.text( 0.62, 0.22, 'Vacuums' )
plt.ylim( (0,1) )

plt.subplot( 2,2,2 )
#plt.ylabel( "Pairs fraction" )
plt.grid()
plt.text( 0.62, 0.22, 'Sheets' )
plt.ylim( (0,1) )
plt.legend( loc='upper right', fancybox = True, shadow = True, ncol = 1, title="Samples" )

plt.subplot( 2,2,3 )
plt.ylabel( "Number fraction" )
plt.xlabel( "$\lambda_{th}$" )
plt.grid()
plt.text( 0.62, 0.22, 'Filaments' )
plt.ylim( (0,1) )

plt.subplot( 2,2,4 )
#plt.ylabel( "Pairs fraction" )
plt.xlabel( "$\lambda_{th}$" )
plt.grid()
plt.text( 0.62, 0.22, 'Knots' )
plt.ylim( (0,1) )

plt.show()