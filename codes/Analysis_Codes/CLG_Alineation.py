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

plt.figure( figsize = (12,4) )
for fold in folds:
  
    #if fold == 'BOLSHOI/':
	#i_fold += 1
	#continue
      
    i_fold += 1
    print fold

    #Loading environment properties of halos
    eigV = np.transpose(np.loadtxt('%s%s%s/%d/EV_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    
    #Loading Halos Data
    halos = np.transpose( np.loadtxt( '%s%sC_GH_%s.dat'%(foldglobal,fold,catalog) ) )
    Nhalos = len(halos[0])		#Number of halos
    
    if fold != 'BOLSHOI/':
	#Loading LG Pairs Systems
	LG = np.transpose(np.loadtxt('%s%s/C_LG_%s.dat'%(foldglobal,fold, catalog)))
	
	EnvLv1 = np.transpose(eigV[ 0:3,[LG[1]-1] ])[0]
	EnvLv2 = np.transpose(eigV[ 3:6,[LG[1]-1] ])[0]
	EnvLv3 = np.transpose(eigV[ 6:9,[LG[1]-1] ])[0]
	
	
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
	
	#Ev1 dot L_LG
	plt.subplot( 1,3,1 )
	angle1 = abs(np.dot( EnvLv1, L_LG[0] )/( norm(L_LG)*norm(EnvLv1) ))
	if i_fold == 2:
	    plt.vlines( angle1, 0, 1, linestyle = '--', linewidth = 1.5, 
	    color = 'red', label = 'LG Sample' )
	else:
	    plt.vlines( angle1, 0, 1, linestyle = '--', linewidth = 1.5, color = 'red')
	
	#Ev2 dot L_LG
	plt.subplot( 1,3,2 )
	angle2 = abs(np.dot( EnvLv2, L_LG[0] )/( norm(L_LG)*norm(EnvLv2) ))
	plt.vlines( angle2, 0, 1, linestyle = '--', linewidth = 1.5, color = 'red' )
	
	#Ev3 dot L_LG
	plt.subplot( 1,3,3 )
	angle3 = abs(np.dot( EnvLv3, L_LG[0] )/( norm(L_LG)*norm(EnvLv3) ))	
	plt.vlines( angle3, 0, 1, linestyle = '--', linewidth = 1.5, color = 'red' )
	
            
    if fold == 'BOLSHOI/':
	#Loading IP Pairs Systems---------------------------------------------------
	IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
	Nip = len( IP[0] )
	
	EnvLv1_IP = eigV[ 0:3,[IP[1]-1] ]
	EnvLv1_IP = np.array([ EnvLv1_IP[0][0], EnvLv1_IP[1][0], EnvLv1_IP[2][0] ])
	
	EnvLv2_IP = eigV[ 3:6,[IP[1]-1] ]
	EnvLv2_IP = np.array([ EnvLv2_IP[0][0], EnvLv2_IP[1][0], EnvLv2_IP[2][0] ])
	
	EnvLv3_IP = eigV[ 6:9,[IP[1]-1] ]
	EnvLv3_IP = np.array([ EnvLv3_IP[0][0], EnvLv3_IP[1][0], EnvLv3_IP[2][0] ])
	
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
	Nclg = len( CLG[0] )
	
	EnvLv1_CLG = eigV[ 0:3,[CLG[4]-1] ]
	EnvLv1_CLG = np.array([ EnvLv1_CLG[0][0], EnvLv1_CLG[1][0], EnvLv1_CLG[2][0] ])
	
	EnvLv2_CLG = eigV[ 3:6,[CLG[4]-1] ]
	EnvLv2_CLG = np.array([ EnvLv2_CLG[0][0], EnvLv2_CLG[1][0], EnvLv2_CLG[2][0] ])
	
	EnvLv3_CLG = eigV[ 6:9,[CLG[4]-1] ]
	EnvLv3_CLG = np.array([ EnvLv3_CLG[0][0], EnvLv3_CLG[1][0], EnvLv3_CLG[2][0] ])
	
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


	#ANGLES CALCULATION
  
	angle1_IP = []
	angle2_IP = []
	angle3_IP = []
	for i in xrange( Nip ):
	    angle1_IP.append( abs(np.dot( EnvLv1_IP[:,i], L_IP[i] )/( norm(L_IP[i])*norm(EnvLv1_IP[:,i]) )))
	    angle2_IP.append( abs(np.dot( EnvLv2_IP[:,i], L_IP[i] )/( norm(L_IP[i])*norm(EnvLv2_IP[:,i]) )))
	    angle3_IP.append( abs(np.dot( EnvLv3_IP[:,i], L_IP[i] )/( norm(L_IP[i])*norm(EnvLv3_IP[:,i]) )))
	    
	angle1_CLG = []
	angle2_CLG = []
	angle3_CLG = []
	for i in xrange( Nclg ):
	    angle1_CLG.append( abs(np.dot( EnvLv1_CLG[:,i], L_CLG[i] )/( norm(L_CLG[i])*norm(EnvLv1_CLG[:,i]) )))
	    angle2_CLG.append( abs(np.dot( EnvLv2_CLG[:,i], L_CLG[i] )/( norm(L_CLG[i])*norm(EnvLv2_CLG[:,i]) )))
	    angle3_CLG.append( abs(np.dot( EnvLv3_CLG[:,i], L_CLG[i] )/( norm(L_CLG[i])*norm(EnvLv3_CLG[:,i]) )))


	Nbin_IP = 100
	Nbin_CLG = 100
	
	#Ev1 dot L_LG	
	plt.subplot( 1,3,1 )
	plt.hist( angle1_IP, range = (0,1), histtype = 'step', linewidth = 3, bins = Nbin_IP,
	color = 'black', cumulative = 1, normed = True, label = 'IP Sample')
	
	plt.hist( angle1_CLG, range = (0,1), histtype = 'step', linewidth = 2, bins = Nbin_CLG,
	color = 'blue', cumulative = 1, normed = True, label = 'CLG Sample')
	
	#Ev2 dot L_LG
	plt.subplot( 1,3,2 )
	plt.hist( angle2_IP, range = (0,1), histtype = 'step', linewidth = 3, bins = Nbin_IP,
	color = 'black', cumulative = 1, normed = True, label = 'IP Sample')
	
	plt.hist( angle2_CLG, range = (0,1), histtype = 'step', linewidth = 2, bins = Nbin_CLG,
	color = 'blue', cumulative = 1, normed = True, label = 'CLG Sample')
	
	#Ev3 dot L_LG
	plt.subplot( 1,3,3 )
	plt.hist( angle3_IP, range = (0,1), histtype = 'step', linewidth = 3, bins = Nbin_IP,
	color = 'black', cumulative = 1, normed = True, label = 'IP Sample')

	plt.hist( angle3_CLG, range = (0,1), histtype = 'step', linewidth = 2, bins = Nbin_CLG,
	color = 'blue', cumulative = 1, normed = True, label = 'CLG Sample')


#Ev1 dot L_LG	
plt.subplot( 1,3,1 )
plt.xlabel( '|$\cos(\phi_1)$|' )
plt.ylabel( 'P(<|$\cos(\phi_1)$|)' )
plt.legend( loc='upper left', fancybox = True, shadow = True, ncol = 1, title="Samples" )
plt.grid()
plt.ylim( (0,1) )
plt.xlim( (0,1) )

#Ev2 dot L_LG	
plt.subplot( 1,3,2 )
plt.xlabel( '|$\cos(\phi_2)$|' )
plt.ylabel( 'P(<|$\cos(\phi_2)$|)' )
plt.grid()
plt.ylim( (0,1) )
plt.xlim( (0,1) )

#Ev3 dot L_LG	
plt.subplot( 1,3,3 )
plt.xlabel( '|$\cos(\phi_3)$|' )
plt.ylabel( 'P(<|$\cos(\phi_3)$|)' )
plt.grid()
plt.ylim( (0,1) )
plt.xlim( (0,1) )

plt.show()