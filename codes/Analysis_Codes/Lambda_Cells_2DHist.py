execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/","CLUES/10909/","CLUES/16953/","CLUES/2710/"]
#Number of sections
N_sec = [256,64,64,64]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Vweb'

#N Lambda
N_l_Bolsh = 100
N_l_Clues = 100
#Lambdas Extreme
L_ext = 0.5


#==================================================================================================
#			CONSTRUCTING EIGENVALUES 1D HISTOGRAMS
#==================================================================================================

i_fold = 0
Lambda13 = np.zeros( (N_l_Clues,N_l_Clues) )
Lambda12 = np.zeros( (N_l_Clues,N_l_Clues) )


plt.figure( figsize=(5.3,4) )
for fold in folds:
    print fold

    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    
    
    #CLUES simulation
    if fold != "BOLSHOI/":
	#tmp  = EigenHist2D( eigV_filename, L_ext, N_l_Clues, '13' )
	#Lambda13 += tmp
	#if i_fold == len(folds)-1:
	    #plt.imshow( Lambda13/(np.sum(Lambda13)*4*L_ext**2/N_l_Clues**2), 
	    #extent = [-L_ext,L_ext,-L_ext,L_ext])
	    ##plt.colorbar()
	    #plt.colorbar( orientation='vertical',shrink=1.0 ) 
	    #plt.title( "CLUES ($\lambda_{1}-\lambda_{3}$)" )
	    
	tmp  = EigenHist2D( eigV_filename, L_ext, N_l_Clues, '12' )
	Lambda12 += tmp
	if i_fold == len(folds)-1:
	    plt.imshow( Lambda12/(np.sum(Lambda12)*4*L_ext**2/N_l_Clues**2), 
	    extent = [-L_ext,L_ext,-L_ext,L_ext])
	    #plt.colorbar()
	    plt.colorbar( orientation='vertical',shrink=1.0 ) 
	    plt.title( "CLUES ($\lambda_{1}-\lambda_{2}$)" )
	    
    
    
    #Cosmic Variance and Bolshoi simulation
    if fold == "BOLSHOI/":
	None
	#LambdaB13  = EigenHist2D( eigV_filename, L_ext, N_l_Bolsh, '13' )
	#plt.imshow( LambdaB13/(np.sum(LambdaB13)*4*L_ext**2/N_l_Bolsh**2.),
	#extent = [-L_ext,L_ext,-L_ext,L_ext])
	#plt.colorbar( orientation='vertical',shrink=1.0 ) 
	#plt.title( "Bolshoi ($\lambda_{1}-\lambda_{3}$)" )
	
	#LambdaB12  = EigenHist2D( eigV_filename, L_ext, N_l_Bolsh, '12' )
	#plt.imshow( LambdaB12/(np.sum(LambdaB12)*4*L_ext**2/N_l_Bolsh**2.),
	#extent = [-L_ext,L_ext,-L_ext,L_ext])
	#plt.colorbar( orientation='vertical',shrink=1.0 ) 
	#plt.title( "Bolshoi ($\lambda_{1}-\lambda_{2}$)" )
	    
	
    i_fold += 1


#Lambda 13
plt.grid()
plt.xlabel( "$\lambda_1$" )
plt.ylabel( "$\lambda_2$" )
Ld = np.linspace( -L_ext, L_ext, 100 )
Lu = L_ext*np.ones( 100 )
plt.fill_between( Ld, Lu, Ld, color = (0.6,0.6,0.6) )
plt.text( -0.38,0.05, "$\lambda_2>\lambda_1$\nregion", color = (0.3,0.3,0.3) )
#plt.subplots_adjust(left=, bottom=0.11, right=None, top=0.93)


plt.show()