execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["CLUES/10909/","CLUES/16953/","CLUES/2710/","BOLSHOI/"]
#Box lenght
Box_L = [64,64,64,250]
#Number of sections
N_sec = [64,64,64,256]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Vweb'

#==================================================================================================
#			CONSTRUCTING FILES WITH HALOS ENVIRONMENT
#==================================================================================================
N_sim = len( folds )
ax = np.zeros( (3, N_sim) )

i_fold = 0
for fold in folds:
    #if fold != "CLUES/2710/":
    if fold != "BOLSHOI/":
	i_fold += 1
	continue
    print "\n"+fold
    
    #Box Lenght
    L = Box_L[i_fold]
    
    #Loading Eigenvalues Vweb filename
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)

    #Loading All properties of Halos
    halos = np.transpose(np.loadtxt('%s%s/C_GH_%s.dat'%(foldglobal,fold, catalog)))
    datos = np.transpose(np.loadtxt('%s%s/C_GH_%s.dat'%(foldglobal,fold, catalog)))
    Nhalos = len(halos[0])
    
    eig = np.transpose(np.loadtxt( '%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    #eig = np.transpose(np.loadtxt( '%s%sVweb/%d/Halos_Environment%s_%s.dat'%(foldglobal,fold,N_sec[i_fold],smooth,catalog)))
    ex = 1
        
    X = 10
    Lam = 0.3
    temp, index = CutHaloX( X, 1, datos, plot=False )
    
    eig1 = CutFieldZ( eigV_filename+"_1", X, res=16, Coor = 1 )
    eig2 = CutFieldZ( eigV_filename+"_2", X, res=16, Coor = 1 )
    eig3 = CutFieldZ( eigV_filename+"_3", X, res=16, Coor = 1 )
    
    delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,fold,N_sec[i_fold],smooth)
    delta = CutFieldZ( delta_filename, X, res=32, Coor = 1 )
    
    plt.subplot(121)
    plt.imshow( np.transpose(Scheme( eig1, eig2, eig3, Lam )[::,::-1]), extent = [ 0,L,0,L ] )


    YY_f = [0,]
    ZZ_f = [0,]

    YY_s = [0,]
    ZZ_s = [0,]
    
    YY_v = [0,]
    ZZ_v = [0,]
    
    for i in xrange( len(index) ):
	ind = index[i] - 1
	if eig[0+ex,ind] > Lam and eig[1+ex,ind] <= Lam and eig[2+ex,ind] <= Lam :
	    YY_s.append( halos[2,ind] )
	    ZZ_s.append( halos[3,ind] )
	if eig[0+ex,ind] > Lam and eig[1+ex,ind] > Lam and eig[2+ex,ind] <= Lam :
	    YY_f.append( halos[2,ind] )
	    ZZ_f.append( halos[3,ind] )
	if eig[0+ex,ind] <= Lam and eig[1+ex,ind] <= Lam and eig[2+ex,ind] <= Lam :
	    YY_v.append( halos[2,ind] )
	    ZZ_v.append( halos[3,ind] )
	    

    plt.plot( YY_s, ZZ_s, 'o', color = "red", markersize = 6 )
    plt.plot( YY_v, ZZ_v, 'o', color = "white", markersize = 6 )
    plt.plot( YY_f, ZZ_f, 'o', color = (61/245.,1,0), markersize = 6 )
    plt.plot( temp[0], temp[1], '.', color = "black", markersize = 3 )
    plt.xlim( (0,L) )
    plt.ylim( (0,L) )
    
    
    plt.subplot(122)
    plt.imshow( np.transpose(np.log(1+delta[::,::-1])), extent = [ 0,L,0,L ], cmap = 'binary' )
    plt.plot( temp[0], temp[1], '.', color = "black", markersize = 3 )
    plt.xlim( (0,L) )
    plt.ylim( (0,L) )
    
    i_fold += 1
    
plt.show() 