execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["CLUES/10909/","CLUES/16953/","CLUES/2710/","BOLSHOI/"]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Mass range
Mrang = [ 5e11, 5e12 ]


#==================================================================================================
#			CONSTRUCTING CLG SAMPLE
#==================================================================================================
N_sim = len( folds )

i_fold = 0
for fold in folds:
    print fold
    #Loading halos catalogs
    halos = np.transpose(np.loadtxt('%s%s/C_GH_%s.dat'%(foldglobal,fold, catalog)))
    Nhalos = len(halos[0])
    
    count = 0
    for i in xrange(Nhalos):
	if Mrang[0]<=halos[8,i]<=Mrang[1]:
	    count += 1
    print count