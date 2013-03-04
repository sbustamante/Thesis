execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = [ "CLUES/16953/", "CLUES/2710/", "CLUES/10909/", "BOLSHOI/" ]
#Labels of graphs
labels = ["CLUES_16953","CLUES_2710", "CLUES_10909", "BOLSHOI"]
#Web type
webtype = 'Tweb/'
#Box lenght
Box_L = 64
#Number of sections
N_sec = 64
#Smooth parameter
smooth = '_s1'
#Lambda Threshold minim
L_min = 0.0
#Lambda Threshold maxim
L_max = 1.0
#Lambda Threshold intervals
L_N = 140
#Cut in Z axe for fields
NZ = 2
#Colors
colors = ['blue', 'green', 'red', 'black']

#Colors
my_cmap4 = plt.cm.get_cmap('gray', 4)
my_cmap2 = plt.cm.get_cmap('gray', 2)
my_cmapC = plt.cm.get_cmap('gray')
#Extent
extent = [0, Box_L, 0, Box_L]


#==================================================================================================
#			CALCULATING CORRELATION HISTOGRAMS
#==================================================================================================

for i in xrange(64):
  
    corr = np.transpose( np.loadtxt( '../../data/Correlations/%sBOLSHOI_%02d.dat'%(webtype,i) ) )
    
    plt.semilogy( corr[0], corr[9]/corr[5], color='magenta' )


i_fold = 0
for fold in folds:  
    #Loading correlations
    corr = np.transpose( np.loadtxt( '../../data/Correlations/%s%s.dat'%(webtype,labels[i_fold]) ) )
    
    plt.semilogy( corr[0], corr[9]/corr[5], label = labels[i_fold], linewidth=2, color = colors[i_fold] )
    
    i_fold += 1
      
    
plt.legend()
plt.xticks( np.linspace(0,1,21) )
plt.xlim( (0,1.0) )
plt.grid()
plt.show()
    
