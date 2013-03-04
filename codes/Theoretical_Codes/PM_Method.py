execfile('_head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Number of grids
M = 20
#Personalized cmap
my_cmapC = plt.cm.get_cmap('gray')
#Number of Particles
Np = 5000
       
#==================================================================================================
#			FUNCTIONS
#==================================================================================================
#Arbitrary Density Function
def rho( x, y ):
    return 1+np.sin(5*(x+0.5)**0.5*(y+0.5)**0.5)*np.cos(10*x)*np.cos(10*y) + \
    1+np.sin(4*(x + y +0.5)**0.5*(y+0.5)**0.5)*np.sin(-8*(x-2*y))*np.cos(6*y)
    
       
#==================================================================================================
#			PLOTTING RESULTS
#==================================================================================================
#Density Plot---------------------------------------------------------------
#X array
X = np.linspace( 0, 1, M )
#Y array
Y = np.linspace( 0, 1, M )
#Density
Rho = np.zeros( (M,M) )

for i in xrange(M):
    for j in xrange(M):
	Rho[j,-i] = rho( X[i], Y[j] )
	
plt.imshow( -Rho, extent = (0,1,0,1), cmap = 'hot')
plt.xticks( np.linspace( 0, 1, M+1 ),('') )
plt.yticks( np.linspace( 0, 1, M+1 ),('') )


#Particles Plot-------------------------------------------------------------
Norm = np.sum(Rho)
Xprt = []
Yprt = []
for i in xrange( 0, M ):
    for j in xrange( 0, M ):
	for p in xrange( int(Np*Rho[-j,i]/Norm) ):
	    Xprt.append( (i + np.random.rand())/(1.0*M) )
	    Yprt.append( (j + np.random.rand())/(1.0*M) )

plt.plot( Xprt, Yprt, 'o', color = 'white', markersize = 2.1 )
plt.xlim( (0,1) )
plt.ylim( (0,1) )
plt.xlabel( '$x$' )
plt.ylabel( '$y$' )
plt.title( 'Scheme of PM Method' )
plt.grid( color = 'black', linewidth = 1.1, linestyle = '-' )
plt.show()