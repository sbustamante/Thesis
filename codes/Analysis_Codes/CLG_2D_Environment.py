execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/","CLUES/10909/","CLUES/16953/","CLUES/2710/"]
#Number of sections
N_sec = [256,64,64,64]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Vweb'

#N Lambda
N_l_Bolsh = 100
N_l_Clues = 100
#Lambdas Extreme
L_ext = 0.8

#Environmet Histogram
L2D = '12'


#==================================================================================================
#			CONSTRUCTING EIGENVALUES 1D HISTOGRAMS
#==================================================================================================

i_fold = 0
Lambda13 = np.zeros( (N_l_Clues,N_l_Clues) )
Lambda12 = np.zeros( (N_l_Clues,N_l_Clues) )
N_sim = len(folds)

plt.figure( figsize=(5.3,4) )
for fold in folds:
    print fold

    #Loading environment properties of halos
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    
    
    #CLUES simulation
    if fold != "BOLSHOI/":
	#Loading LG Pairs Systems
	LG = np.loadtxt('%s%s/C_LG_%s.dat'%(foldglobal,fold, catalog))
	EnvL1 = (eig[ 1,LG[1]-1 ], eig[ 1,LG[4]-1 ])
	EnvL2 = (eig[ 2,LG[1]-1 ], eig[ 2,LG[4]-1 ])
	EnvL3 = (eig[ 3,LG[1]-1 ], eig[ 3,LG[4]-1 ])
	#if L2D == '13':
	    #plt.plot( EnvL1, EnvL3, 'o', color='red', markersize = 7)
	#if L2D == '12':
	    #plt.plot( EnvL1, EnvL2, 'o', color='red', markersize = 7)
	
    
    
    #Cosmic Variance and Bolshoi simulation
    if fold == "BOLSHOI/":
      	#Loading CLG Pairs Systems
	CLG = np.transpose(np.loadtxt('%s%s/C_CLG_%s.dat'%(foldglobal,fold, catalog)))
	EnvBL1 = eig[ 1,[CLG[1]-1] ]
	EnvBL2 = eig[ 2,[CLG[1]-1] ]
	EnvBL3 = eig[ 3,[CLG[1]-1] ]
	
	#Loading IP Pairs Systems
	IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
	EnvBL1_IP = eig[ 1,[IP[1]-1] ]
	EnvBL2_IP = eig[ 2,[IP[1]-1] ]
	EnvBL3_IP = eig[ 3,[IP[1]-1] ]

	if L2D == '13':
	    #Cells
	    #LambdaB13  = EigenHist2D( eigV_filename, L_ext, N_l_Bolsh, '13' )
	    #Halos
	    LambdaB13  = np.transpose(np.histogram2d( eig[1], eig[3], bins = N_l_Bolsh, 
	    normed = True, range = ((-L_ext,L_ext),(-L_ext,L_ext)))[0][::,::-1])
	    
	    plt.imshow( LambdaB13/(np.sum(LambdaB13)*4*L_ext**2/N_l_Bolsh**2.),
	    extent = [-L_ext,L_ext,-L_ext,L_ext])
	    plt.colorbar( orientation='vertical',shrink=1.0 ) 
	    plt.title( "Bolshoi ($\lambda_{1}-\lambda_{3}$)" )
	    plt.plot( EnvBL1_IP, EnvBL3_IP, '.', color='black', markersize = 2)
	    plt.plot( EnvBL1, EnvBL3, 'o', color='white', markersize = 5)
	
	if L2D == '12':
	    #Cells
	    #LambdaB12  = EigenHist2D( eigV_filename, L_ext, N_l_Bolsh, '12' )
	    #Halos
	    LambdaB12  = np.transpose(np.histogram2d( eig[1], eig[2], bins = N_l_Bolsh, 
	    normed = True, range = ((-L_ext,L_ext),(-L_ext,L_ext)))[0][::,::-1])
	    
	    plt.imshow( LambdaB12/(np.sum(LambdaB12)*4*L_ext**2/N_l_Bolsh**2.),
	    extent = [-L_ext,L_ext,-L_ext,L_ext])
	    plt.colorbar( orientation='vertical',shrink=1.0 ) 
	    plt.title( "Bolshoi ($\lambda_{1}-\lambda_{2}$)" )
	    plt.plot( EnvBL1_IP, EnvBL2_IP, '.', color='black', markersize = 2, )
	    plt.plot( EnvBL1, EnvBL2, 'o', color='white', markersize = 5)
	    
	
    i_fold += 1


plt.grid()
plt.xlabel( "$\lambda_1$" )
if L2D == '13':
    plt.ylabel( "$\lambda_3$" )
    plt.text( -0.38,0.05, "$\lambda_3>\lambda_1$\nregion", color = (0.3,0.3,0.3) )
    plt.ylim( (-L_ext,L_ext) )
    plt.xlim( (-L_ext,L_ext) )
    #plt.plot( (-10,), (-10,), 'o', color='red', markersize = 7, label = 'LG Sample' )
    plt.plot( (-10,), (-10,), 'o', color='white', markersize = 5, label = 'CLG Sample')
    plt.plot( (-10,), (-10,), '.', color='black', markersize = 2, label = 'IP Sample')
    
    plt.legend( fancybox = True, shadow = True, title="Samples", ncol = 1, loc='upper left')
    
if L2D == '12':
    plt.ylabel( "$\lambda_2$" )
    plt.text( -0.15,0.15, "$\lambda_2>\lambda_1$\nregion", color = (0.3,0.3,0.3) )
    plt.ylim( (-L_ext/4,L_ext) )
    plt.xlim( (-L_ext/4,L_ext) )
    
Ld = np.linspace( -L_ext, L_ext, 100 )
Lu = L_ext*np.ones( 100 )
plt.fill_between( Ld, Lu, Ld, color = (0.6,0.6,0.6) )
#plt.subplots_adjust(left=, bottom=0.11, right=None, top=0.93)


plt.show()