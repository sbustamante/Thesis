execfile('_head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = [ "CLUES/16953/", "CLUES/2710/", "CLUES/10909/", "BOLSHOI/" ]
#Labels of graphs
labels = ["CLUES 16953", "CLUES 2710", "CLUES 10909", "Bolshoi"]
#Web type
webtype = 'Vweb/'
#Catalog type
catalog = ['FOF','FOF','FOF','FOF']
#Box lenght
Box_L = [64., 64., 64., 256.]
#Resolution
res = [64, 64, 64, 256]
#Smooth parameter
smooth = '_s1'
#Linewidths
LW = [1, 1, 1, 2.0]
#Colors
Colors = [ 'red', 'blue', 'green', 'black' ]
#Numbers of bins in each histogram
Nbins = [ 100, 100, 100, 500 ]


#==================================================================================================
#			CALCULATING HISTOGRAMS OF EIGENVALUES
#==================================================================================================
i_fold = 0
for fold in folds:
    print '\nCurrently in ', fold
 
    #Loading Environment Properties
    halos_envinroment = np.loadtxt("%s%s%s%d/Halos_Environment%s_%s.dat"
    %(foldglobal, fold, webtype, res[i_fold], smooth, catalog[i_fold]))
    
    plt.subplot(131)
    plt.hist( halos_envinroment[:,0], bins = Nbins[i_fold], normed = True, alpha = 1, 
    histtype='step', linewidth = LW[i_fold], color = Colors[i_fold] )
    
    plt.subplot(132)
    plt.hist( halos_envinroment[:,1], bins = Nbins[i_fold], normed = True, alpha = 1,
    histtype='step', linewidth = LW[i_fold], color = Colors[i_fold] )
    
    plt.subplot(133)
    plt.hist( halos_envinroment[:,2], bins = Nbins[i_fold], normed = True, alpha = 1,
    histtype='step', linewidth = LW[i_fold], color = Colors[i_fold] )

    i_fold += 1


#==================================================================================================
#			FORMAT OF PLOTS
#==================================================================================================
plt.subplot(131)
plt.xlabel( "$\lambda_1$" )
plt.ylabel( "Normalized distribution function" )
plt.grid()
plt.xlim( (-1,2) )
plt.title("$\lambda_1$")

plt.subplot(132)
plt.xlabel( "$\lambda_2$" )
plt.grid()
plt.xlim( (-1,1) )
plt.title("$\lambda_2$")
plt.legend(labels, fancybox = True, shadow = True, ncol = 4, title='Simulations',
markerscale = 0., loc = 'upper center', bbox_to_anchor = (0.5, -0.08))

plt.subplot(133)
plt.xlabel( "$\lambda_3$" )
plt.grid()
plt.xlim( (-2,1) )
plt.title("$\lambda_3$")
    
plt.show()

#Values to plot a optim size
#( 0.12, 0.18, 0.90, 0.90, 0.20, 0.20 )
