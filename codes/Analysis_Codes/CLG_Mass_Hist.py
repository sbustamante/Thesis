execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["CLUES/10909/","CLUES/16953/","CLUES/2710/","BOLSHOI/"]
#Number of sections
N_sec = [64,64,64,256]
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

plt.figure( figsize = (5,5) )
i_fold = 0
for fold in folds:
    print fold
  
    if fold == "BOLSHOI/":
	#Loading Isolated Pairs Systems
	IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
	Nip = len(IP[0])
	#Total Pair Mass
	plt.hist( IP[2]+IP[5], bins = Nd_IP, range=(0.95e12,10e12), cumulative=-1, normed=True, 
	histtype='step',linewidth=3, color = "black" )
	plt.plot( (0,), (0,), linewidth=3, color = "black", label='IP Sample' )
	
	#Loading CLG Pairs Systems
	CLG = np.transpose(np.loadtxt('%s%s/C_CLG_%s.dat'%(foldglobal,fold, catalog)))
	Nclg = len(CLG[0])
	#Total Pair Mass
	plt.hist( CLG[2]+CLG[5], bins = Nd_CLG, range=(0.95e12,10e12), cumulative=-1, normed=True, 
	histtype='step',linewidth=2, color = "blue" )
	plt.plot( (0,), (0,),linewidth=2, color = "blue", label='CLG Sample' )


    if fold != "BOLSHOI/":
	#Loading LG Pairs Systems
	LG = np.loadtxt('%s%s/C_LG_%s.dat'%(foldglobal,fold, catalog))
	if i_fold == 0:
	    plt.vlines( LG[2]+LG[5], 0, 1, color = 'red', linewidth = 1.5, linestyle='--', 
	    label = 'LG Sample' )
	else:
	    plt.vlines( LG[2]+LG[5], 0, 1, color = 'red', linewidth = 1.5, linestyle='--')
    
    i_fold += 1

plt.ylim( (0,1) )
plt.xlim( (1.e12,10e12) )
#plt.xscale('log')
#plt.yscale('log')
plt.ylabel('Pairs fraction ($>M$)')
plt.xlabel('$M_{tot} = M_A + M_B$ [$h^{-1}M_{\odot}$]')
plt.legend( fancybox = True, shadow = True, title="Samples", ncol = 1, loc='upper right')
plt.grid()
plt.show()
