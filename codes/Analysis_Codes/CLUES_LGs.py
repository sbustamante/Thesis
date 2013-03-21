execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["CLUES/10909/","CLUES/16953/","CLUES/2710/"]
#Labels of graphs
labels = ["CLUES 10909","CLUES 16953","CLUES 2710"]
#Box lenght
Box_L = [64,64,64]
#Number of sections
N_sec = [64,64,64]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Coordinate to cut (1 -- X, 2 -- Y, 3 -- Z)
axe = 2
#Coordinates in plots
axe_label = ["x","y","z","x","y","z"]

#Colors
my_cmapC = plt.cm.get_cmap('gray')


#==================================================================================================
#			PLOTING EACH CLUES SIMULATION AND RESPECTIVE LG
#==================================================================================================
'''
FIGURE SCHEME
-------------------
|  1  |  2  |  3  |
-------------------
'''

N_sim = len( folds )
ax = np.zeros( (3, N_sim) )

i_fold = 0


for fold in folds:
    #Extent
    extent = [0, Box_L[i_fold], 0, Box_L[i_fold]]

    #Loading Density filename
    delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,fold,N_sec[i_fold],smooth)
    #Loading LG index of each simulation
    LG_Index = np.loadtxt('%s%s/LG_index_%s.dat'%(foldglobal,fold, catalog))
    #Loading All properties of Halos
    halos = np.transpose(np.loadtxt('%s%s/C_GH_%s.dat'%(foldglobal,fold, catalog)))
    
    LG_prop = [ halos[0:4,int(LG_Index[0]-1)], halos[0:4,int(LG_Index[1]-1)] ]

    #Current label simulation
    label = labels[i_fold]
	
    #Loading Fields
    Ns = int((LG_prop[0][axe]/Box_L[i_fold])*N_sec[i_fold])
    delta = CutFieldZ( delta_filename, Ns, 32, Coor = axe )

    #Plotting
    plt.subplot( 1, N_sim, i_fold+1 )
    plt.imshow( np.log(1+np.transpose(delta[::,::-1])), extent = extent, cmap = "binary" )
    plt.title( "Density field for %s\n%s = %1.2f"%
    ( labels[i_fold],axe_label[axe-1], Box_L[i_fold]*Ns/N_sec[i_fold] ) )
    plt.ylabel( '%s [Mpc $h^{-1}$]'%(axe_label[axe]) )
    plt.xlabel( '%s [Mpc $h^{-1}$]'%(axe_label[axe+1]) )

    if axe == 1:
	plt.plot( 
	(LG_prop[0][2],LG_prop[1][2]), 
	(LG_prop[0][3],LG_prop[1][3]), 
	'o', markersize = 10, color = 'red', label='LG' )
	datos = CutHaloX( Ns, 1, halos, plot=False, color='black' )
    if axe == 2:
	plt.plot( 
	(LG_prop[0][1],LG_prop[1][1]), 
	(LG_prop[0][3],LG_prop[1][3]), 
	'o', markersize = 10, color = 'red', label='LG' )
	datos = CutHaloY( Ns, 1, halos, plot=False, color='black' )
    if axe == 3:
	plt.plot( 
	(LG_prop[0][1],LG_prop[1][1]), 
	(LG_prop[0][2],LG_prop[1][2]), 
	'o', markersize = 10, color = 'red', label='LG' )
	datos = CutHaloZ( Ns, 1, halos, plot=False, color='black' )
	
    plt.plot( datos[0], datos[1], 'o', color = 'black', markersize = 1 )
    
    plt.xlim( (0,Box_L[i_fold]) )
    plt.ylim( (0,Box_L[i_fold]) )

    i_fold += 1
    
plt.show()