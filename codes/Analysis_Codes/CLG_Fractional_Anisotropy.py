execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/"]
#Number of sections
N_sec = [256]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Vweb'

#Resolution of FA Histograms
N_IP = 100
N_CLG = 100


#==================================================================================================
#			CONSTRUCTING FA HISTOGRAMS
#==================================================================================================

i_fold = 0
N_sim = len(folds)

plt.figure( figsize = (6,6) )
for fold in folds:
    print fold

    #Loading environment properties of halos
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
            
    #Loading CLG Pairs Systems
    CLG = np.transpose(np.loadtxt('%s%s/C_CLG_%s.dat'%(foldglobal,fold, catalog)))
    
    #Loading IP Pairs Systems
    IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
    
    EnvBL1 = eig[ 1,[CLG[1]-1] ][0]
    EnvBL2 = eig[ 2,[CLG[1]-1] ][0]
    EnvBL3 = eig[ 3,[CLG[1]-1] ][0]
    
    EnvBL1_IP = eig[ 1,[IP[1]-1] ][0]
    EnvBL2_IP = eig[ 2,[IP[1]-1] ][0]
    EnvBL3_IP = eig[ 3,[IP[1]-1] ][0]
    
    FA_CLG = Fractional_Anisotropy( EnvBL1, EnvBL2, EnvBL3 )
    FA_IP  = Fractional_Anisotropy( EnvBL1_IP, EnvBL2_IP, EnvBL3_IP )
    FA_GH  = Fractional_Anisotropy( eig[1], eig[2], eig[3] )
    

    #plt.hist( FA_GH, bins = 100, normed = True, cumulative = 1, color = 'gray', linewidth = 2, 
    #range = (0,1.01), histtype = "step", linestyle = 'dashed' )
    #plt.plot( (0,), (0,), '--',linewidth=2, color = "gray", label='GH Sample' )
      
    plt.hist( FA_IP, bins = 100, normed = True, cumulative = 1, color = 'black', linewidth = 3, 
    range = (0,1.01), histtype = "step" )
    plt.plot( (0,), (0,), linewidth=3, color = "black", label='IP Sample' )
    
    plt.hist( FA_CLG, bins = 100, normed = True, cumulative = 1, color = 'blue', linewidth = 2, 
    range = (0,1.01), histtype = "step" )
    plt.plot( (0,), (0,),linewidth=2, color = "blue", label='CLG Sample' )


    #FA_ran_CLG, C_FA_CLG = Hist1D( FA_CLG, 1, 2*N_CLG )
    #FA_ran_IP, C_FA_IP = Hist1D( FA_IP, 1, 2*N_IP )
    #plt.plot( FA_ran_IP, C_FA_IP/(np.sum(C_FA_IP)*1./N_IP), color = 'black', linewidth = 3, 
    #label='IP Sample' )
    #plt.plot( FA_ran_CLG, C_FA_CLG/(np.sum(C_FA_CLG)*1./N_IP), color = 'blue', linewidth = 2, 
    #label='CLG Sample' )



#Fractional Anisotropy
plt.ylabel( "Number fraction [<FA]" )
plt.xlabel( "Fractional Anisotropy FA" )
plt.legend( loc='upper left', fancybox = True, shadow = True, ncol = 1, title="Samples" )
plt.grid()
plt.xlim( (0,1) )
plt.ylim( (0,1) )


plt.show()