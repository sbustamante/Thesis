execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/","CLUES/10909/","CLUES/16953/","CLUES/2710/"]
#Labels of graphs
labels = ["BOLSHOI","CLUES 10909","CLUES 16953","CLUES 2710"]
#Box lenght
Box_L = [250,64,64,64]
#Number of sections
N_sec = [256,64,64,64]
#Smooth parameter
smooth = '_s1'
#Lambda Tweb
Lamb_Tweb = 0.3
#Lambda Vweb
Lamb_Vweb = 0.3


#Colors
my_cmap4 = plt.cm.get_cmap('gray', 4)
my_cmapC = plt.cm.get_cmap('gray')


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

for NZ in xrange(N_sec[0]):
    i_fold = 0
    #Define figure entorn
    fig = plt.figure( figsize=(14,5.6*N_sim) )
    
    for fold in folds:
	#Extent
	extent = [0, Box_L[i_fold], 0, Box_L[i_fold]]
  
	eigT_filename = '%s%sTweb/%d/Eigen%s'%(foldglobal,fold,N_sec[i_fold],smooth)
	eigV_filename = '%s%sVweb/%d/Eigen%s'%(foldglobal,fold,N_sec[i_fold],smooth)
	delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,fold,N_sec[i_fold],smooth)
	
	#Current label simulation
	label = labels[i_fold]
	    
	#Loading Fields
	delta = CutFieldZ( delta_filename, NZ, 32 )
	eigT1 = CutFieldZ( eigT_filename+"_1", NZ, 16 )
	eigT2 = CutFieldZ( eigT_filename+"_2", NZ, 16 )
	eigT3 = CutFieldZ( eigT_filename+"_3", NZ, 16 )
	eigV1 = CutFieldZ( eigV_filename+"_1", NZ, 16 )
	eigV2 = CutFieldZ( eigV_filename+"_2", NZ, 16 )
	eigV3 = CutFieldZ( eigV_filename+"_3", NZ, 16 )

	#First panel---------------------------------------
	ax0 = fig.add_subplot( N_sim, 3, 1 + 3*i_fold )
	pic01 = ax0.imshow( -np.log(1+delta), cmap = my_cmapC, extent = extent )
	ax0.set_title( "Density field" )
	ax0.set_ylabel( 'y [Mpc $h^{-1}$]' )
	ax0.set_xlabel( 'x [Mpc $h^{-1}$]' )


	#Second panel--------------------------------------
	schT = Scheme( eigT1, eigT2, eigT3, Lamb_Tweb )
	ax1 = fig.add_subplot( N_sim, 3, 2 + 3*i_fold )
	pic11 = ax1.imshow( -schT, cmap = my_cmap4, extent = extent, vmin=-3, vmax=0 )
	ax1.set_title( "%s SIMULATION\n\nT-web Scheme, $\lambda_{th}$ = %1.2f"%(label,Lamb_Tweb) )
	ax1.set_ylabel( 'y [Mpc $h^{-1}$]' )
	ax1.set_xlabel( 'x [Mpc $h^{-1}$]\nZ = %d'%NZ )
	
	
	#Third panel--------------------------------------
	schV = Scheme( eigV1, eigV2, eigV3, Lamb_Vweb )
	ax2 = fig.add_subplot( N_sim, 3, 3 + 3*i_fold )
	pic21 = ax2.imshow( -schV, cmap = my_cmap4, extent = extent, vmin=-3, vmax=0 )
	ax2.set_title( "V-web Scheme, $\lambda_{th}$ = %1.2f"%Lamb_Vweb )
	ax2.set_ylabel( 'y [Mpc $h^{-1}$]' )
	ax2.set_xlabel( 'x [Mpc $h^{-1}$]' )
	
	i_fold += 1
    
    fname='_tmp-%03d.png'%i_pic
    fig.savefig(fname)
    plt.close()
    i_pic += 1
    print 'NZ:', NZ
    
    
print 'Making movie animation.mpg - this make take a while'
os.system("ffmpeg -qscale 1 -r 5 -b 9600 -i _tmp-%03d.png  video.mp4")

os.system('rm -rf *.png')