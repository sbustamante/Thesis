execfile('_head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Number of grids
M = 15
#Personalized cmap
my_cmapC = plt.cm.get_cmap('gray')
#Number of Particles
Np = 500
       
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
	if (i<4 or i>10) or (j<4 or j>10):
	    for p in xrange( int(Np*Rho[-j,i]/Norm) ):
		Xprt.append( (i + np.random.rand())/(1.0*M) )
		Yprt.append( (j + np.random.rand())/(1.0*M) )
#Mesh grid
plt.plot( Xprt, Yprt, 'o', color = 'white', markersize = 6 )
plt.xlim( (0,1) )
plt.ylim( (0,1) )
plt.xlabel( '$x$' )
plt.ylabel( '$y$' )
plt.title( 'Scheme of P$^3$M Method' )
plt.grid( color = 'black', linewidth = 1.5, linestyle = '-' )

#PP Scheme
plt.fill_between( (0.2666,0.7333), (0.2666,0.2666), (0.73333,0.7333), color=(0.7,0.7,0.7) )
plt.fill_between( (0.4,0.6), (0.4,0.4), (0.6,0.6), color=(1.0,1.0,1.0) )

XprtPP = (0.5, 0.48, 0.35, 0.65, 0.7, 0.45, 0.3, 0.56, 0.69, 0.36 )
YprtPP = (0.5, 0.55, 0.65, 0.55, 0.35, 0.3, 0.5, 0.69, 0.44, 0.36 )
#Lines bewteen particles
for i in xrange( 1, 10 ):
    plt.plot( (0.5, XprtPP[i]), (0.5, YprtPP[i]), '--', color = (0.3,0.3,0.3), linewidth=2 )
plt.plot( XprtPP , YprtPP, 'o', color = 'black', markersize = 8 )


plt.show()
