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

#Environmet Histogram
L2D = '1'


#==================================================================================================
#			CONSTRUCTING EIGENVALUES 1D HISTOGRAMS
#==================================================================================================

i_fold = 0
N_sim = len(folds)

plt.figure( figsize=(4,4) )
for fold in folds:
    print fold

    #Loading environment properties of halos
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    
    
    #CLUES simulation
    if fold != "BOLSHOI/":
	#Loading LG Pairs Systems
	LG = np.loadtxt('%s%s/C_LG_%s.dat'%(foldglobal,fold, catalog))
	if L2D == '1':
	    plt.plot( (eig[ 1,LG[1]-1 ],),(eig[ 1,LG[4]-1 ],), 'o', color='red', markersize = 7)
	if L2D == '2':
	    plt.plot( (eig[ 2,LG[1]-1 ],),(eig[ 2,LG[4]-1 ],), 'o', color='red', markersize = 7)
	if L2D == '3':
	    plt.plot( (eig[ 3,LG[1]-1 ],),(eig[ 3,LG[4]-1 ],), 'o', color='red', markersize = 7)
	
    
    
    #Cosmic Variance and Bolshoi simulation
    if fold == "BOLSHOI/":
      	#Loading CLG Pairs Systems
	CLG = np.transpose(np.loadtxt('%s%s/C_CLG_%s.dat'%(foldglobal,fold, catalog)))
	
	#Loading IP Pairs Systems
	IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
	
	if L2D == '1':
	    EnvBL1_h1 = eig[ 1,[CLG[1]-1] ]
	    EnvBL1_h2 = eig[ 1,[CLG[4]-1] ]
	    EnvBL1_IP_h1 = eig[ 1,[IP[1]-1] ]	
	    EnvBL1_IP_h2 = eig[ 1,[IP[4]-1] ]
	    
	    plt.plot( EnvBL1_IP_h1, EnvBL1_IP_h2, '.', color='black', markersize = 2)
	    plt.plot( EnvBL1_h2, EnvBL1_h1, 'o', color='blue', markersize = 5)
	if L2D == '2':
	    EnvBL1_h1 = eig[ 2,[CLG[1]-1] ]
	    EnvBL1_h2 = eig[ 2,[CLG[4]-1] ]
	    EnvBL1_IP_h1 = eig[ 2,[IP[1]-1] ]	
	    EnvBL1_IP_h2 = eig[ 2,[IP[4]-1] ]
	    
	    plt.plot( EnvBL1_IP_h1, EnvBL1_IP_h2, '.', color='black', markersize = 2)
	    plt.plot( EnvBL1_h2, EnvBL1_h1, 'o', color='blue', markersize = 5)
	if L2D == '3':
	    EnvBL1_h1 = eig[ 3,[CLG[1]-1] ]
	    EnvBL1_h2 = eig[ 3,[CLG[4]-1] ]
	    EnvBL1_IP_h1 = eig[ 3,[IP[1]-1] ]	
	    EnvBL1_IP_h2 = eig[ 3,[IP[4]-1] ]
	    
	    plt.plot( EnvBL1_IP_h1, EnvBL1_IP_h2, '.', color='black', markersize = 2)
	    plt.plot( EnvBL1_h2, EnvBL1_h1, 'o', color='blue', markersize = 5)
	    
	
    i_fold += 1


plt.grid()
if L2D == '1':
    plt.xlim( (0,1) )
    plt.ylim( (0,1) )
    plt.xlabel( "$\lambda_1$ Halo A" )
    plt.ylabel( "$\lambda_1$ Halo B" )
    plt.plot( (-10,), (-10,), 'o', color='red', markersize = 7, label = 'LG Sample' )
    plt.plot( (-10,), (-10,), 'o', color='blue', markersize = 5, label = 'CLG Sample')
    plt.plot( (-10,), (-10,), '.', color='black', markersize = 2, label = 'IP Sample')
    
    plt.legend( fancybox = True, shadow = True, title="Samples", ncol = 1, loc='upper left')
    
if L2D == '2':
    plt.xlim( (-0.2,0.8) )
    plt.ylim( (-0.2,0.8) )
    plt.xlabel( "$\lambda_2$ Halo A" )
    plt.ylabel( "$\lambda_2$ Halo B" )
    
if L2D == '3':
    plt.xlim( (-0.5,0.5) )
    plt.ylim( (-0.5,0.5) )
    plt.xlabel( "$\lambda_3$ Halo A" )
    plt.ylabel( "$\lambda_3$ Halo B" )
    
plt.subplots_adjust( right = 0.98, left = 0.19, top = 0.98, bottom = 0.12 )
plt.show()