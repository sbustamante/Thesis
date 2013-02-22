execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
fold = "CLUES/2710/"
#Labels of graphs
label = "CLUES 2710"
#Web type
webtype = 'Vweb/'
#Box lenght
Box_L = 64
#Number of sections
N_sec = 64
#Smooth parameter
smooth = '_s1'
#Lambda Threshold minim
L_min = -0.4
#Lambda Threshold maxim
L_max = 1.0
#Lambda Threshold intervals
L_N = 140
#Cut in Z axe for fields
NZ = 2

#Colors
my_cmap4 = plt.cm.get_cmap('gray', 4)
my_cmap2 = plt.cm.get_cmap('gray', 2)
my_cmapC = plt.cm.get_cmap('gray')
#Extent
extent = [0, Box_L, 0, Box_L]


#==================================================================================================
#			CALCULATING CORRELATION HISTOGRAMS
#==================================================================================================

eig_filename = '%s%s%s%d/Eigen%s'%(foldglobal,fold,webtype,N_sec,smooth)
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,fold,N_sec,smooth)

#Calculating correlations
corr = Correlation( eig_filename, delta_filename, L_min, L_max, L_N )


#==================================================================================================
#			PLOTING RESULTS
#==================================================================================================
'''
FIGURE SCHEME
-------------
|     0	    |
-------------
|  1  |  3  |
-------------
|  2  |  4  |
-------------
'''
#Loading Fields
delta = CutFieldZ( delta_filename, NZ, 32 )
eig1 = CutFieldZ( eig_filename+"_1", NZ, 16 )
eig2 = CutFieldZ( eig_filename+"_2", NZ, 16 )
eig3 = CutFieldZ( eig_filename+"_3", NZ, 16 )


i_pic = 0
for Lamb in np.linspace(L_min, L_max, L_N):
    #Define figure entorn
    fig = plt.figure( figsize=(8,11) )
    #Creating plot grid
    gs = gridspec.GridSpec(3, 2)

    #Upper panel---------------------------------------
    ax0 = fig.add_subplot( gs[0,:] )
    pic01 = ax0.plot( corr[0], corr[1]/corr[9], linewidth = 2, color = 'blue',
    label = " subdensity and divergent flux" )
    pic02 = ax0.plot( corr[0], corr[3]/corr[10], linewidth = 2, color = 'green',
    label = " overdensity and convergent flux")
    pic03 = ax0.vlines( Lamb, 0, 1.5, linewidth = 2, linestyle = '--', color = 'gray' )
    ax0.set_ylim( (0,1.5) )
    ax0.set_xlabel( "$\lambda_{th}$" )
    ax0.set_ylabel( "$N_{fraction}$" )
    ax0.set_title( "Correlation Index for %s Simulation"%(label), fontsize = 16 )
    ax0.grid()

    #Middle left panel----------------------------------
    ax1 = fig.add_subplot( gs[0,2] )
    pic11 = ax1.matshow( -delta/abs(delta), cmap = my_cmap2, extent = extent )
    ax1.set_ylabel( 'y [Mpc $h^{-1}$]' )

    #Lower left panel----------------------------------
    ax2 = fig.add_subplot( gs[1,1] )
    pic21 = ax2.imshow( -np.log(1+delta), cmap = my_cmapC, extent = extent )
    ax2.set_ylabel( 'y [Mpc $h^{-1}$]' )
    ax2.set_xlabel( 'x [Mpc $h^{-1}$]' )

    #Middle right panel---------------------------------
    ax3 = fig.add_subplot( gs[1,0] )
    pic31 = ax3.matshow( -(eig1 + eig2 + eig3 - 3*Lamb)/abs((eig1 + eig2 + eig3 - 3*Lamb)), 
    cmap = my_cmap2, extent = extent )

    #Lower right panel---------------------------------
    sch = Scheme( eig1, eig2, eig3, Lamb )
    ax4 = fig.add_subplot( gs[1,2] )
    pic41 = ax4.imshow( -sch, cmap = my_cmap4, extent = extent, vmin=-3, vmax=0 )
    ax4.set_xlabel( 'x [Mpc $h^{-1}$]' )
    
    fname='_tmp-%03d.png'%i_pic
    fig.savefig(fname)
    plt.close()
    i_pic += 1
    print 'Lambda:', Lamb
    

print 'Making movie animation.mpg - this make take a while'
os.system("ffmpeg -qscale 1 -r 10 -b 9600 -i _tmp-%03d.png  video.mp4")

os.system('rm -rf *.png')