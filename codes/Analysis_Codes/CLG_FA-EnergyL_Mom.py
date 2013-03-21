execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/", "CLUES/10909/","CLUES/16953/","CLUES/2710/"]
#Number of sections
N_sec = [256,64,64,64]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Vweb'

#Resolution of FA Histograms
N_IP = 100
N_CLG = 100


#==================================================================================================
#			CONSTRUCTING FA HISTOGRAMS
#==================================================================================================

i_fold = -1
N_sim = len(folds)

plt.figure( figsize = (12,5) )
for fold in folds:
    i_fold += 1
    print fold

    #Loading environment properties of halos
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    
    #Loading Halos Data
    halos = np.transpose( np.loadtxt( '%s%sC_GH_%s.dat'%(foldglobal,fold,catalog) ) )
    Nhalos = len(halos[0])		#Number of halos
    
    if fold != 'BOLSHOI/':
	#Loading LG Pairs Systems
	LG = np.transpose(np.loadtxt('%s%s/C_LG_%s.dat'%(foldglobal,fold, catalog)))
	
	EnvL1 = eig[ 1,[LG[1]-1] ]
	EnvL2 = eig[ 2,[LG[1]-1] ]
	EnvL3 = eig[ 3,[LG[1]-1] ]
	
	FA_LG = Fractional_Anisotropy( EnvL1, EnvL2, EnvL3 )
	
	#Energy and Angular Momentum
	I1 = list([LG[1]-1,])
	M1 = halos[ 8, I1 ]
	x1 = halos[ 1, I1 ];  y1 = halos[ 2, I1 ]; z1 = halos[ 3, I1 ]
	vx1 = halos[ 4, I1 ]; vy1 = halos[ 5, I1 ]; vz1 = halos[ 6, I1 ]
	
	I2 = list([LG[4]-1,])
	M2 = halos[ 8, I2 ]
	x2 = halos[ 1, I2 ];  y2 = halos[ 2, I2 ]; z2 = halos[ 3, I2 ]
	vx2 = halos[ 4, I2 ]; vy2 = halos[ 5, I2 ]; vz2 = halos[ 6, I2 ]
	
	E_LG, L_LG = \
	Energy_AngularM( M1, x1, y1, z1, vx1, vy1, vz1, M2, x2, y2, z2, vx2, vy2, vz2)
	
	#Fractional Anisotropy - Energy
	plt.subplot( 1,2,1 )
	if i_fold == 2:
	    plt.plot( FA_LG, E_LG/1e-36, 'o', markersize=10, color = "red", label='LG Sample' )
	else:
	    plt.plot( FA_LG, E_LG/1e-36, 'o', markersize=10, color = "red")
	
	#Fractional Anisotropy - Mass Ratio
	plt.subplot( 1,2,2 )
	plt.plot( FA_LG, np.sqrt(L_LG[:,0]**2 + L_LG[:,1]**2 + L_LG[:,2]**2), 
	'o', markersize=10, color = "red" )
	
            
    if fold == 'BOLSHOI/':
	#Loading IP Pairs Systems---------------------------------------------------
	IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
	
	EnvBL1_IP = eig[ 1,[IP[1]-1] ][0]
	EnvBL2_IP = eig[ 2,[IP[1]-1] ][0]
	EnvBL3_IP = eig[ 3,[IP[1]-1] ][0]	
	FA_IP  = Fractional_Anisotropy( EnvBL1_IP, EnvBL2_IP, EnvBL3_IP )
	
	#Energy and Angular Momentum
	I1 = list(IP[1]-1)
	M1 = halos[ 8, I1 ]
	x1 = halos[ 1, I1 ];  y1 = halos[ 2, I1 ]; z1 = halos[ 3, I1 ]
	vx1 = halos[ 4, I1 ]; vy1 = halos[ 5, I1 ]; vz1 = halos[ 6, I1 ]
	
	I2 = list(IP[4]-1)
	M2 = halos[ 8, I2 ]
	x2 = halos[ 1, I2 ];  y2 = halos[ 2, I2 ]; z2 = halos[ 3, I2 ]
	vx2 = halos[ 4, I2 ]; vy2 = halos[ 5, I2 ]; vz2 = halos[ 6, I2 ]
	
	E_IP, L_IP = \
	Energy_AngularM( M1, x1, y1, z1, vx1, vy1, vz1, M2, x2, y2, z2, vx2, vy2, vz2)


	#Loading CLG Pairs Systems--------------------------------------------------
	CLG = np.transpose(np.loadtxt('%s%s/C_CLG_%s.dat'%(foldglobal,fold, catalog)))
	
	EnvBL1 = eig[ 1,[CLG[1]-1] ][0]
	EnvBL2 = eig[ 2,[CLG[1]-1] ][0]
	EnvBL3 = eig[ 3,[CLG[1]-1] ][0]
	FA_CLG = Fractional_Anisotropy( EnvBL1, EnvBL2, EnvBL3 )
	
	#Energy and Angular Momentum
	I1 = list(CLG[1]-1)
	M1 = halos[ 8, I1 ]
	x1 = halos[ 1, I1 ];  y1 = halos[ 2, I1 ]; z1 = halos[ 3, I1 ]
	vx1 = halos[ 4, I1 ]; vy1 = halos[ 5, I1 ]; vz1 = halos[ 6, I1 ]
	
	I2 = list(CLG[4]-1)
	M2 = halos[ 8, I2 ]
	x2 = halos[ 1, I2 ];  y2 = halos[ 2, I2 ]; z2 = halos[ 3, I2 ]
	vx2 = halos[ 4, I2 ]; vy2 = halos[ 5, I2 ]; vz2 = halos[ 6, I2 ]
	
	E_CLG, L_CLG = \
	Energy_AngularM( M1, x1, y1, z1, vx1, vy1, vz1, M2, x2, y2, z2, vx2, vy2, vz2)


	#Fractional Anisotropy - Total Mass
	plt.subplot( 1,2,1 )
	Hist  = np.transpose(np.histogram2d( FA_IP, E_IP/1e-36, 
	bins = 15, normed = False, range = ((0,1),(-8,0)) )[0][::,::-1])
	plt.imshow( Hist, interpolation='nearest', aspect = 'auto',
	cmap = 'binary', extent = (0,1,-8,0), alpha = 0.8 )
	
	plt.contour( Hist[::-1,::], 10, aspect = 'auto', 
	extent = (0,1,-10,0), linewidth=2, interpolation = 'gaussian' )
	plt.colorbar()
	
	plt.plot( FA_CLG, E_CLG/1e-36, 'o', markersize=7, color = "blue", label='CLG Sample' )
	
	
	#Fractional Anisotropy - Mass Ratio
	plt.subplot( 1,2,2 )
	Hist  = np.transpose(np.histogram2d( FA_IP, 
	np.sqrt(L_IP[:,0]**2 + L_IP[:,1]**2 + L_IP[:,2]**2), 
	bins = 15, normed = False, range = ((0,1),(0,30)) )[0][::,::-1])
	plt.imshow( Hist, interpolation='nearest', aspect = 'auto',
	cmap = 'binary', extent = (0,1,0,30), alpha = 0.8 )
	#plt.colorbar( shrink = 0.5, pad = 0.05)
	
	plt.contour( Hist[::-1,::], 10, aspect = 'auto', 
	extent = (0,1,0,30), linewidth=2, interpolation = 'gaussian' )
	plt.colorbar( shrink = 1.0)
	
	plt.plot( FA_CLG, 
	np.sqrt(L_CLG[:,0]**2 + L_CLG[:,1]**2 + L_CLG[:,2]**2), 
	'o', markersize=7, color = "blue" )


#Fractional Anisotropy - Energy
plt.subplot( 1,2,1 )
plt.ylim( (-8,0) )
plt.xlim( (0,1) )
plt.ylabel('$e_{tot}$ [$10^{-36}$ Mpc$^2$s$^{-2}$]')
plt.xlabel( "Fractional Anisotropy FA" )
plt.legend( loc='upper left', fancybox = True, shadow = True, ncol = 1, title="Samples" )
plt.grid()


#Fractional Anisotropy - Mass Ratio
plt.subplot( 1,2,2 )
plt.ylim( (0,30) )
plt.xlim( (0,1) )
plt.ylabel('$L_{orb}$ [Mpc km s$^{-1}$]')
plt.xlabel( "Fractional Anisotropy FA" )
plt.grid()


plt.show()