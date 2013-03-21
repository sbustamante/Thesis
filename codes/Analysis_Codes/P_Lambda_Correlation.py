execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["CLUES/10909/","CLUES/16953/","CLUES/2710/","BOLSHOI/"]
#Number of sections
N_sec = [64,64,64,256]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Vweb'

#==================================================================================================
#			CONSTRUCTING CORRELATION PLOTS
#==================================================================================================
N_sim = len( folds )

i_fold = 0
for fold in folds:
    if fold != "BOLSHOI/":
	i_fold += 1
	continue
    print fold
    
    #Loading IP catalog
    IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
    Nip = len(IP[0])
    
    #Loading CLG catalog
    CLG = np.transpose(np.loadtxt('%s%s/C_CLG_%s.dat'%(foldglobal,fold, catalog)))
    Nclg = len(CLG[0])
    
    #Loading environment properties of halos
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    
    eigIP = np.zeros( (Nip,6) )
    for i in xrange(Nip):
	i1 = IP[1,i] - 1
	i2 = IP[4,i] - 1
	
	for l in xrange(0,3):
	    eigIP[i,l] = eig[l+1,i1]
	    eigIP[i,l+3] = eig[l+1,i2]
	    
    eigCLG = np.zeros( (Nclg,6) )
    for i in xrange(Nclg):
	i1 = CLG[1,i] - 1
	i2 = CLG[4,i] - 1
	
	for l in xrange(0,3):
	    eigCLG[i,l] = eig[l+1,i1]
	    eigCLG[i,l+3] = eig[l+1,i2]
	    
    
    e1 = 1
    e2 = 3
    
    H, xedges, yedges = np.histogram2d( eig[e1], eig[e2], bins=(256,256))
    H.shape, xedges.shape, yedges.shape

    #extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
    extent = [np.min(eig[e1]), np.max(eig[e1]), np.min(eig[e2]), np.max(eig[e2])]

    #plt.imshow( np.transpose(np.log(H[::,::-1]+1)), extent=extent, interpolation='nearest')
    plt.imshow( np.transpose(H[::,::-1]), extent=extent)
	    
    #plt.plot( eig[e1], eig[e2], '.', color = 'black', markersize = 0.5 )    
    plt.plot( eigIP[:,0], eigIP[:,2], 'o', color = 'black', markersize = 2 )
    plt.plot( eigCLG[:,3], eigCLG[:,5], 'o', color = 'white', markersize = 6 )
    
    plt.grid()
    plt.xlim( (np.min(eig[e1]), np.max(eig[e1])) )
    plt.ylim( (np.min(eig[e2]), np.max(eig[e2])) )
    
plt.show()
	    
    