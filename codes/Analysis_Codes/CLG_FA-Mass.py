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
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    
    if fold != 'BOLSHOI/':
	#Loading LG Pairs Systems
	LG = np.transpose(np.loadtxt('%s%s/C_LG_%s.dat'%(foldglobal,fold, catalog)))
	
	EnvL1 = eig[ 1,[LG[1]-1] ]
	EnvL2 = eig[ 2,[LG[1]-1] ]
	EnvL3 = eig[ 3,[LG[1]-1] ]
	
	FA_LG = Fractional_Anisotropy( EnvL1, EnvL2, EnvL3 )
	
	#Fractional Anisotropy - Total Mass
	plt.subplot( 1,2,1 )
	if i_fold == 2:
	    plt.plot( FA_LG, (LG[5]+LG[2])/1e12, 'o', markersize=10, color = "red", label='LG Sample' )
	else:
	    plt.plot( FA_LG, (LG[5]+LG[2])/1e12, 'o', markersize=10, color = "red")
	
	#Fractional Anisotropy - Mass Ratio
	plt.subplot( 1,2,2 )
	plt.plot( FA_LG, LG[5]/LG[2], 'o', markersize=10, color = "red" )
	
            
    if fold == 'BOLSHOI/':
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
	
	FA_CLG = Fractional_Anisotropy( EnvBL1, EnvBL2, EnvBL3 )
	FA_IP  = Fractional_Anisotropy( EnvBL1_IP, EnvBL2_IP, EnvBL3_IP )
	FA_GH  = Fractional_Anisotropy( eig[1], eig[2], eig[3] )

	#Fractional Anisotropy - Total Mass
	plt.subplot( 1,2,1 )
	Hist  = np.transpose(np.histogram2d( FA_IP, (IP[5]+IP[2])/1e12, 
	bins = 15, normed = False, range = ((0,1),(1,8)) )[0][::,::-1])
	plt.imshow( Hist, interpolation='nearest', aspect = 'auto',
	cmap = 'binary', extent = (0,1,1,8), alpha = 0.8 )
	
	plt.contour( Hist[::-1,::], 10, aspect = 'auto', 
	extent = (0,1,1,8), linewidth=2, interpolation = 'gaussian' )
	plt.colorbar()
	
	plt.plot( FA_CLG, (CLG[5]+CLG[2])/1e12, 'o', markersize=7, color = "blue", label='CLG Sample' )
	
	
	#Fractional Anisotropy - Mass Ratio
	plt.subplot( 1,2,2 )
	Hist  = np.transpose(np.histogram2d( FA_IP, IP[5]/IP[2], 
	bins = 15, normed = False, range = ((0,1),(0.1,1)) )[0][::,::-1])
	plt.imshow( Hist, interpolation='nearest', aspect = 'auto',
	cmap = 'binary', extent = (0,1,0.1,1), alpha = 0.8 )
	#plt.colorbar( shrink = 0.5, pad = 0.05)
	
	plt.contour( Hist[::-1,::], 6, aspect = 'auto', 
	extent = (0,1,0.1,1), linewidth=2, interpolation = 'gaussian' )
	plt.colorbar( shrink = 1.0)
	
	plt.plot( FA_CLG, CLG[5]/CLG[2], 'o', markersize=7, color = "blue" )


#Fractional Anisotropy - Total Mass
plt.subplot( 1,2,1 )
plt.ylabel( "$M_{tot} = M_A + M_B$ [$1 \\times 10^{12} h^{-1} M_{\odot}$]" )
plt.xlabel( "Fractional Anisotropy FA" )
plt.legend( loc='upper left', fancybox = True, shadow = True, ncol = 1, title="Samples" )
plt.grid()


#Fractional Anisotropy - Mass Ratio
plt.subplot( 1,2,2 )
plt.ylabel( "$\chi = M_B/M_A$" )
plt.xlabel( "Fractional Anisotropy FA" )
plt.grid()


plt.show()