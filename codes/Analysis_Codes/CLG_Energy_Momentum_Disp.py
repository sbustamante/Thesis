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
#Numver of intervals
Nd_IP  = 200
Nd_CLG = 100

#==================================================================================================
#			CONSTRUCTING EIGENVALUES EXTREME VALUES
#==================================================================================================
N_sim = len( folds )

plt.figure( figsize = (8,6) )
LG1 = []
LG2 = []

i_fold = 0
for fold in folds:
    print fold
  
    #Loading Halos Data
    halos = np.transpose( np.loadtxt( '%s%sC_GH_%s.dat'%(foldglobal,fold,catalog) ) )
    Nhalos = len(halos[0])		#Number of halos
  
    if fold == "BOLSHOI/":
	#Loading Pairs Systems----------------------------------------------
	P = np.transpose(np.loadtxt('%s%s/C_P_%s.dat'%(foldglobal,fold, catalog)))
	#Energy and Angular Momentum
	I1 = list(P[1]-1)
	M1 = halos[ 8, I1 ]
	x1 = halos[ 1, I1 ];  y1 = halos[ 2, I1 ]; z1 = halos[ 3, I1 ]
	vx1 = halos[ 4, I1 ]; vy1 = halos[ 5, I1 ]; vz1 = halos[ 6, I1 ]
	
	I2 = list(P[4]-1)
	M2 = halos[ 8, I2 ]
	x2 = halos[ 1, I2 ];  y2 = halos[ 2, I2 ]; z2 = halos[ 3, I2 ]
	vx2 = halos[ 4, I2 ]; vy2 = halos[ 5, I2 ]; vz2 = halos[ 6, I2 ]
	
	E_P, L_P = \
	Energy_AngularM( M1, x1, y1, z1, vx1, vy1, vz1, M2, x2, y2, z2, vx2, vy2, vz2)
	
	#plt.plot( E_IP/(1e-36), np.sqrt(L_IP[:,0]**2 + L_IP[:,1]**2 + L_IP[:,2]**2) ,
	#'.', markersize=2, color = "black", label='IP Sample' )
	Hist  = np.transpose(np.histogram2d( E_P/1e-36,
	np.sqrt(L_P[:,0]**2 + L_P[:,1]**2 + L_P[:,2]**2), 
	bins = 15, normed = False, range = ((-10,0),(0,30)) )[0][::,::-1])
	
	plt.imshow( Hist, interpolation='nearest', aspect = 'auto',
	cmap = 'binary', extent = (-10,0,0,30) )	
	plt.colorbar()
	
	#plt.contour( Hist[::-1,::], 10, aspect = 'auto', 
	#extent = (-15,0,0,30), linewidth=2, interpolation = 'gaussian' )
	#plt.colorbar()
	
      
	#Loading Isolated Pairs Systems----------------------------------------------
	IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
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
	
	#plt.plot( E_IP/(1e-36), np.sqrt(L_IP[:,0]**2 + L_IP[:,1]**2 + L_IP[:,2]**2) ,
	#'.', markersize=2, color = "black", label='IP Sample' )
	Hist  = np.transpose(np.histogram2d( E_IP/1e-36,
	np.sqrt(L_IP[:,0]**2 + L_IP[:,1]**2 + L_IP[:,2]**2), 
	bins = 15, normed = False, range = ((-10,0),(0,30)) )[0][::,::-1])
	
	#plt.imshow( Hist, interpolation='nearest', aspect = 'auto',
	#cmap = 'binary', extent = (-15,0,0,30) )	
	#plt.colorbar()
	
	plt.contour( Hist[::-1,::], 7, aspect = 'auto', 
	extent = (-10,0,0,30), linewidth=1.5, interpolation = 'gaussian' )
	plt.colorbar()
	
	
	
	#Loading CLG Pairs Systems --------------------------------------------------
	CLG = np.transpose(np.loadtxt('%s%s/C_CLG_%s.dat'%(foldglobal,fold, catalog)))
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
	
	plt.plot( E_CLG/(1e-36), np.sqrt(L_CLG[:,0]**2 + L_CLG[:,1]**2 + L_CLG[:,2]**2) ,
	'o', markersize=7, color = "blue", label='CLG Sample' )


    if fold != "BOLSHOI/":
	#Loading LG Pairs Systems----------------------------------------------------
	LG = np.loadtxt('%s%s/C_LG_%s.dat'%(foldglobal,fold, catalog))
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
	
	LG1.append( E_LG )
	LG2.append( np.sqrt(L_LG[:,0]**2 + L_LG[:,1]**2 + L_LG[:,2]**2) )
	
	if i_fold == 2:
	    plt.plot( E_LG/(1e-36), np.sqrt(L_LG[:,0]**2 + L_LG[:,1]**2 + L_LG[:,2]**2) ,
	    'o', markersize=10, color = "red", label='LG Sample' )
	else:
	    plt.plot( E_LG/(1e-36), np.sqrt(L_LG[:,0]**2 + L_LG[:,1]**2 + L_LG[:,2]**2) ,
	    'o', markersize=10, color = "red" )

	        
    i_fold += 1



#Function to plot sigma regions of distros
def SigmaRegion( Mean_1, Std_1, Mean_2, Std_2, sigma, color, alpha ):
    Err1 = np.linspace( Mean_1 - sigma*Std_1, Mean_1 + sigma*Std_1, 10 )
    Err2U = np.ones(10)*( Mean_2 + sigma*Std_2 )
    Err2D = np.ones(10)*( Mean_2 - sigma*Std_2 )
    plt.fill_between( Err1, Err2U, Err2D, color = color, alpha = alpha )
    return None


sigma = 0
#Sigma Region of LG
SigmaRegion( np.mean( np.array(LG1)/1e-36 ), np.std( np.array(LG1)/1e-36 ), \
np.mean( LG2 ), np.std( LG2 ), sigma, 'red', 0.3 )

#Sigma Region of IP
SigmaRegion( np.mean( E_IP/1e-36 ), np.std( E_IP/1e-36 ), \
np.mean( L_IP ), np.std( L_IP ), sigma, 'black', 0.3 )

#Sigma Region of CLG
SigmaRegion( np.mean( E_CLG/1e-36 ), np.std( E_CLG/1e-36 ), \
np.mean( L_CLG ), np.std( L_CLG ), sigma, 'blue', 0.3 )


#==================================================================================================
#Plot configuration 
#==================================================================================================

plt.xlim( (-10,0) )
plt.ylim( (0,30) )
plt.ylabel('$L_{orb}$ [Mpc km s$^{-1}$]')
plt.xlabel('$e_{tot}$ [$10^{-36}$ Mpc$^2$s$^{-2}$]')
plt.legend( fancybox = True, shadow = True, title="Samples", ncol = 1, loc='upper left')
plt.grid()
plt.show()
