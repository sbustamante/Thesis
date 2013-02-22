import pylab as plt
import numpy as np
import scipy as sp
import scipy.integrate as integ
import scipy.fftpack as fourier

#========================================================================================
# PERTURBATION FIELD
#========================================================================================
    
#Plot density map    
Plot_map2D = False

#Plot density histograms
Plot_Histogram = False

#Plot Transfer Function
Plot_transfer = True

#Number of matrix sample
N = 128
#Power Spectrum
n = 1.
#Dimension of box (1e3Mpc)
L = 1e6
#8/h Kpc
l8 = 8000.
#sigma8
sigma8 = 0.801

#Normalization spectrum===========================================================================================
#Windows function
def W(x):
    if x<=1:
	return 1
    if x>1:
	return 0

#Variance function
def sigma2( R ):
    sig2 = integ.quad( lambda k: k**2 * k**n * W(k*R)**2/(2*np.pi**2), 0, 2*np.pi*N/L )[0]
    return sig2
    
#Constant of normalization
A = sigma8**2/sigma2(l8)
AA = 2*np.pi**2*(n+3)*sigma8**2*l8**(n+3)
    
#Initial Spectrum
def Pk( k ):
    return AA*k**n
        
#Transfer Function
def T(q):
    Tk = np.log( 1 + 2.34*q )/(2.34*q)*( 1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4 )**(-1/4.)
    return Tk
    
    
q = np.linspace( 0, 10, 1000 )


if Plot_transfer == True:
    #Funcion de Transferencia
    plt.subplot(121)
    plt.title( "Transfer Function $T_k$" )
    plt.xlabel( "$q  = k/( \Omega_0 h^2$Mpc $^{-1})$" )
    plt.ylabel( "$T_k$" )
    plt.loglog( q, T(q), linewidth = 2 )
    plt.grid()

    plt.subplot(122)
    plt.title( "Power Spectrum $\sigma_k^2$" )
    plt.xlabel( "$q  = k/( \Omega_0 h^2$Mpc $^{-1})$" )
    plt.ylabel( "$\sigma_k/ A$" )
    plt.loglog( q, Pk( q )*T(q)**2, label='Processed Spectrum $\sigma_k(z = 0)$', linewidth = 2 )
    plt.loglog( q, Pk( q ), label='Harrison-Zeldovich Spectrum', linewidth = 2 )
    plt.legend( loc = 'lower left' )
    plt.grid()
    
    
    plt.show()


#2D density map
if Plot_map2D == True:

    #Phase distribution===============================================================================================
    phi = np.zeros( (N,N) )
    k = 0
    while( k<N*N ):
	i = np.random.randint( N )
	j = np.random.randint( N )
	if phi[i,j] == 0:
	    phi[i,j] = np.random.rand()*2*np.pi
	    k += 1
	    if i>0 and j>0:
		phi[N-i,N-j] = 2*np.pi-phi[i,j]
		k += 1
    phi[0,0] = np.random.rand()*2*np.pi

    for i in xrange(1,N):
	phi[0,i] = 2*np.pi-phi[0,N-i]
	phi[i,0] = 2*np.pi-phi[N-i,0]
    #=================================================================================================================
	    
    #Radial distribution==============================================================================================
    R = np.zeros( (N,N) )
    kk = 0
    K = []
    while( kk<N*N ):
	i = np.random.randint( N )
	j = np.random.randint( N )
	r = np.random.rand()
	kx = 2*np.pi*i/L
	ky = 2*np.pi*j/L
	k = np.sqrt( kx**2 + ky**2 )
	K.append(k)
	sig2 = L**-3*Pk(k)
	if R[i,j] == 0:
	    R[i,j] = np.sqrt( 2*sig2*abs( np.log(1-r) ) )
	    kk += 1
	    if i>0 and j>0:
		R[N-i,N-j] = R[i,j]
		kk += 1
    r = np.random.rand()
    kx = 2*np.pi*i/L
    ky = 2*np.pi*j/L
    k = np.sqrt( kx**2 + ky**2 )
    sig2 = L**-3*Pk(k)
    R[0,0] = np.sqrt( 2*sig2*abs( np.log(1-r) ) )

    for i in xrange(1,N):
	R[0,i] = R[0,N-i]
	R[i,0] = R[N-i,0]
    #=================================================================================================================

    #Complex Field
    X = np.zeros( (N,N), 'complex' )
    for i in xrange(0,N):
	for j in xrange(0,N):
	    X[i,j] = R[i,j]*np.cos(phi[i,j]) + 1j*R[i,j]*np.sin(phi[i,j])
    X[N/2,0] = X[0,N/2] = np.real(X[0,N/2])

    frr = np.real(fourier.ifft2(X))

    plt.imshow(frr, extent = [0,64,0,64])
    #plt.xticks( (0,1),("","") )
    #plt.yticks( (0,1),("","") )
    plt.title( 'Density fiels $\delta(r)$ for a\n Harrison-Zeldovich spectrum' )
    #plt.colorbar()
    plt.xlabel( '$x$' )
    plt.ylabel( '$y$' )

    plt.show()


#Histograms==============================================================================================
if Plot_Histogram == True:
    #Number of histograms
    Nf = 100

    def P1(dd, sigma2):
	return 1/np.sqrt( 2*np.pi*sigma2 )*np.exp( -dd**2/(2*sigma2) )
      
	
    Fflat = np.hstack(frr)
    #Fflat = Fflat/np.max(abs(frr))
    D_Tam = 2e-5
    Delta = np.linspace( -D_Tam, D_Tam, Nf )
    Ncount = np.zeros( Nf )

    for dd in Fflat:
	for i in xrange(0,Nf-1):
	    if dd>Delta[i] and dd<=Delta[i+1]:
		Ncount[i] += 1
		
    Ncount = Ncount/(N*N*1.0)*Nf/(2*D_Tam)
    sigma2 = np.max(Ncount)**-2/(2*np.pi)
		
    plt.plot( Delta, Ncount, 'o-' )
    plt.plot( Delta, P1(Delta, sigma2) )
    plt.title( 'Histograms for contrast density field, for $P(k)=k^%d$\n$\sigma^2=\chi(0)=%2.3e$'%(n,sigma2) )
    plt.ylabel( 'Number of contrast' )
    plt.xlabel( '$\delta_{k}$' )
    plt.xlim( (-D_Tam, D_Tam) )

    plt.show()

