execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/", "CLUES/10909/","CLUES/16953/","CLUES/2710/"]
#Number of sections
N_sec = [256,64,64,64]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Numver of intervals
Nd_IP  = 200
Nd_CLG = 100

#==================================================================================================
#			CONSTRUCTING EIGENVALUES EXTREME VALUES
#==================================================================================================
N_sim = len( folds )

plt.figure( figsize = (6,6) )
MeanLG = []

i_fold = 0
for fold in folds:
    print fold
  
    if fold == "BOLSHOI/":	
	#Loading Isolated Pairs Systems
	IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
	Nip = len(IP[0])
	#Total Pair Mass
	plt.plot( IP[5]+IP[2], IP[5]/IP[2], '.', markersize=2, color = "black", label='IP Sample' )
	#plt.imshow( np.transpose((np.histogram2d( IP[5]+IP[2], IP[5]/IP[2], bins=10 )[0])[::,::-1]), 
	#extent = (1e12,9e12,0.1,1.), aspect='auto' )
	
	#Loading CLG Pairs Systems
	CLG = np.transpose(np.loadtxt('%s%s/C_CLG_%s.dat'%(foldglobal,fold, catalog)))
	Nclg = len(CLG[0])
	#Total Pair Mass
	plt.plot( CLG[5]+CLG[2], CLG[5]/CLG[2], 'o', markersize=7, color = "blue", label='CLG Sample' )


    if fold != "BOLSHOI/":
	#Loading LG Pairs Systems
	LG = np.loadtxt('%s%s/C_LG_%s.dat'%(foldglobal,fold, catalog))
	MeanLG += [[(LG[5]+LG[2]),(LG[5]/LG[2])]]
	if i_fold == 1:
	    plt.plot( (LG[5]+LG[2],), (LG[5]/LG[2],), 'o', color = 'red', markersize = 10,
	    label = 'LG Sample' )
	else:
	    plt.plot( (LG[5]+LG[2],), (LG[5]/LG[2],), 'o', color = 'red', markersize = 10)
	        
    i_fold += 1



#Function to plot sigma regions of distros
def SigmaRegion( Mean_Mass, Std_Mass, Mean_Ratio, Std_Ratio, sigma, color, alpha ):
    MassErr = np.linspace( Mean_Mass - Sigma*Std_Mass, Mean_Mass + Sigma*Std_Mass, 10 )
    RatErrU = np.ones(10)*( Mean_Ratio + Sigma*Std_Ratio )
    RatErrD = np.ones(10)*( Mean_Ratio - Sigma*Std_Ratio )
    plt.fill_between( MassErr, RatErrU, RatErrD, color = color, alpha = alpha )
    return None


#Region of 2 sigma
Mean_Mass  = (MeanLG[0][0] + MeanLG[1][0] + MeanLG[2][0])/3.
Mean_Ratio = (MeanLG[0][1] + MeanLG[1][1] + MeanLG[2][1])/3.
Std_Mass   = np.sqrt((Mean_Mass - MeanLG[0][0])**2 + (Mean_Mass - MeanLG[1][0])**2 + (Mean_Mass - MeanLG[2][0])**2)
Std_Ratio  = np.sqrt((Mean_Ratio- MeanLG[0][1])**2 + (Mean_Ratio- MeanLG[1][1])**2 + (Mean_Ratio- MeanLG[2][1])**2)
#Sigma level
Sigma = 1

print "Mean Mass:\n \tIP Bolshoi: %1.3e\tCLG Bolshoi: %1.3e\tLG CLUES: %1.3e"%(\
np.mean( IP[5]+IP[2] ), np.mean( CLG[5]+CLG[2] ), Mean_Mass )
print "Deviation Mass:\n \tIP Bolshoi: %1.3e\tCLG Bolshoi: %1.3e\tLG CLUES: %1.3e\n"%(\
np.std( IP[5]+IP[2] ), np.std( CLG[5]+CLG[2] ), Std_Mass )

print "Mean Ratio:\n \tIP Bolshoi: %1.3e\tCLG Bolshoi: %1.3e\tLG CLUES: %1.3e"%(\
np.mean( IP[5]/IP[2] ), np.mean( CLG[5]/CLG[2] ), Mean_Ratio )
print "Deviation Ratio:\n \tIP Bolshoi: %1.3e\tCLG Bolshoi: %1.3e\tLG CLUES: %1.3e\n"%(\
np.std( IP[5]/IP[2] ), np.std( CLG[5]/CLG[2] ), Std_Ratio )

#Sigma Region of LG
SigmaRegion( Mean_Mass, Std_Mass, Mean_Ratio, Std_Ratio, 1, 'red', 0.3 )

#Sigma Region of IP
SigmaRegion( np.mean( IP[5]+IP[2] ), np.std( IP[5]+IP[2] ), \
np.mean( IP[5]/IP[2] ), np.std( IP[5]/IP[2] ), 1, 'black', 0.3 )

#Sigma Region of CLG
SigmaRegion( np.mean( CLG[5]+CLG[2] ), np.std( CLG[5]+CLG[2] ), \
np.mean( CLG[5]/CLG[2] ), np.std( CLG[5]/CLG[2] ), 1, 'blue', 0.3 )


#==================================================================================================
#Plot configuration 
#==================================================================================================

#Inferior Limit
Xe = np.linspace( 0,1, 100 )
plt.plot( 5e11*(1+1/Xe), Xe, '--', color = 'brown', linewidth = 2 )
plt.fill_betweenx( Xe, 5e11*(1+1/Xe), Xe*0, color = (0.6,0.6,0.6) )
plt.text( 1.2e12, 0.12, "$M_{min} = M_{*}(1+1/\chi)$", color = (0.2,0.2,0.2) )

plt.xlim( (1e12,9e12) )
plt.ylim( (0.1,1.0) )
plt.ylabel('$\\chi = M_B/M_A$')
plt.xlabel('$M_{tot} = M_A + M_B$ [$h^{-1}M_{\odot}$]')
plt.legend( fancybox = True, shadow = True, title="Samples", ncol = 1, loc='upper right')
plt.grid()
plt.show()
