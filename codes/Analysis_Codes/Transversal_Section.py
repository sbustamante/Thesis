execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
#folds = ["CLUES/10909/","CLUES/16953/","CLUES/2710/"]
##Box lenght
#Box_L = 64
##Number of sections
#N_sec = 64

#Simulation
folds = ["BOLSHOI/"]
#Box lenght
Box_L = 250
#Number of sections
N_sec = 256

#Labels of graphs
labels = ["CLUES 10909","CLUES 16953","CLUES 2710","BOLSHOI"]
#Smooth parameter
smooth = '_s1'
#Lambda Vweb
Lamb_Vweb = 0.3
#Lambda Tweb
Lamb_Tweb = 0.3


#Colors
my_cmap4 = plt.cm.get_cmap('gray', 4)
my_cmapC = plt.cm.get_cmap('gray')
#Extent
extent = [0, Box_L, 0, Box_L]


#==================================================================================================
#			PLOTING RESULTS AND VIDEO
#==================================================================================================
'''
FIGURE SCHEME
-------------------
|  1  |  2  |  3  |
-------------------
'''

i_pic = 0
N_sim = len( folds )
ax = np.zeros( (3, N_sim) )

i_fold = 0
#Define figure entorn
fig = plt.figure( figsize=(14,5.6*N_sim))

NZ = 50

for fold in folds:

    eigV_filename = '%s%sVweb/%d/Eigen%s'%(foldglobal,fold,N_sec,smooth)
    eigT_filename = '%s%sTweb/%d/Eigen%s'%(foldglobal,fold,N_sec,smooth)
    delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,fold,N_sec,smooth)
    
    #Current label simulation
    label = labels[i_fold]
	
    #Loading Fields
    delta = CutFieldZ( delta_filename, NZ, 32 )
    
    eigV1 = CutFieldZ( eigV_filename+"_1", NZ, 16 )
    eigV2 = CutFieldZ( eigV_filename+"_2", NZ, 16 )
    eigV3 = CutFieldZ( eigV_filename+"_3", NZ, 16 )
    
    eigT1 = CutFieldZ( eigT_filename+"_1", NZ, 16 )
    eigT2 = CutFieldZ( eigT_filename+"_2", NZ, 16 )
    eigT3 = CutFieldZ( eigT_filename+"_3", NZ, 16 )

    #First panel---------------------------------------
    ax0 = fig.add_subplot( "%d3%d"%(N_sim, 1 + 3*i_fold) )
    pic01 = ax0.imshow( -np.log(1+delta), cmap = my_cmapC, extent = extent )
    ax0.set_title( "Density field" )
    ax0.set_ylabel( 'y [Mpc $h^{-1}$]' )
    ax0.set_xlabel( 'x [Mpc $h^{-1}$]' )
    
    
    #Second panel--------------------------------------
    schV = Scheme( eigT1, eigT2, eigT3, Lamb_Tweb )
    ax2 = fig.add_subplot( "%d3%d"%(N_sim, 2 + 3*i_fold) )
    pic21 = ax2.imshow( -schV, cmap = my_cmap4, extent = extent, vmin=-3, vmax=0 )
    ax2.set_title( "T-web Scheme, $\lambda_{th}$ = %1.2f"%Lamb_Tweb )
    ax2.set_ylabel( 'y [Mpc $h^{-1}$]' )
    ax2.set_xlabel( 'x [Mpc $h^{-1}$]' )
    
    
    #Third panel--------------------------------------
    schV = Scheme( eigV1, eigV2, eigV3, Lamb_Vweb )
    ax3 = fig.add_subplot( "%d3%d"%(N_sim, 3 + 3*i_fold) )
    pic31 = ax3.imshow( -schV, cmap = my_cmap4, extent = extent, vmin=-3, vmax=0 )
    ax3.set_title( "V-web Scheme, $\lambda_{th}$ = %1.2f"%Lamb_Vweb )
    ax3.set_ylabel( 'y [Mpc $h^{-1}$]' )
    ax3.set_xlabel( 'x [Mpc $h^{-1}$]' )
    
    i_fold += 1
    
    
    
plt.show()
