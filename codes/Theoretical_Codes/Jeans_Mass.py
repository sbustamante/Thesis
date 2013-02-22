import pylab as plt
import numpy as np
import scipy as sp
import scipy.integrate as integ
import scipy.fftpack as fourier

Graphic = 1
#========================================================================================
# GRAPH 1		(JEANS MASS)
#========================================================================================
if Graphic==1:
    #Radiation parameter
    OmegaR = 2.44e-5
    #Matter Parameter
    OmegaB = 0.266
    #Equivalent redshift
    z_eq = 12098.
    #Recombination redshift
    z_rc = 1000.
  
    def MJ(a):
	z = 1/a-1
	mj = 1.86927e29*(  ( 1+3/4.*OmegaB/OmegaR*1/(1+z) )*( 1+OmegaB/OmegaR*1/(1+z) )  )**-1.5*(1+z)**-3*OmegaB
	return mj
	
    def MJpost(a):
	z = 1/a-1
	mj = 2.11e5*OmegaB**-0.5*((1+z)/z_rc)**1.5
	return mj

    def MJ_Approx(a):
	z = 1/a-1
	mj = 1.86927e29*(1+z)**-3*OmegaB
	return mj
	
    def MJz(z):
	mj = 1.86927e29*(  ( 1+3/4.*OmegaB/OmegaR*1/(1+z) )*( 1+OmegaB/OmegaR*1/(1+z) )  )**-1.5*(1+z)**-3*OmegaB
	return mj
	
    def MJpostz(z):
	mj = 2.11e5*OmegaB**-0.5*((1+z)/z_rc)**1.5
	return mj
	
    def MJz_Approx(z):
	mj = 1.86927e29*(1+z)**-3*OmegaB
	return mj

    #plt.subplot( 121 )
    a = np.linspace( 1e-7,1/(z_rc+1),200000 )
    m = MJ(a)
    a1 = np.linspace( 1/(z_rc+1),0.1,200000 )
    m = list(m) + list(MJpost(a1))
    a = list(a)+ list(a1)
    plt.loglog( a, m, label='$M_J(a)$', color='blue', linewidth=2 );
    
    a = np.linspace( 1e-7,1.0,200000 )
    plt.loglog( a, MJ_Approx(a), '--', color='black' );
    
    a = np.linspace( 1/(z_rc+1),1,200000 )
    plt.loglog( a, MJ(a), '--', color='gray', linewidth=2 );
    
    plt.legend( loc='upper left', fancybox = True, shadow = True )
    
    #Epoca de igualdad radiacion materia
    plt.vlines( 1/(z_eq+1), 1E1, 1E20 )
    plt.text( 1.3/(z_eq+1),1E6, 'Epoch of $\\rho_{m}=\\rho_{r}$', rotation=90, fontsize=10 )
    #z de epoca de recombinacion
    plt.vlines( 1/(z_rc+1), 1E1, 1E20 )
    plt.text( 1.6/(z_rc+1),1E6, 'Epoch of recombination', rotation=90, fontsize=10 )
    
    a = np.linspace( 1e-7, 0.1, 100 )
    plt.fill_between( a, 1e13*np.ones(100), 1e17*np.ones(100), color = 'blue', alpha = 0.3 )
    plt.text( 2e-7, 10**14.5, 'Galaxy Clusters \nand Superclusters', color='blue', alpha = 0.4 )
    
    plt.fill_between( a, 1e7*np.ones(100), 1e13*np.ones(100), color = 'green', alpha = 0.3 )
    plt.text( 2e-7, 10**9.5, 'Galaxies', color='green', alpha = 0.4 )
    
    plt.fill_between( a, 1e3*np.ones(100), 1e7*np.ones(100), color = 'red', alpha = 0.3 )
    plt.text( 2e-7, 10**4.5, 'Globular Clusters', color='red', alpha = 0.4 )
    
    plt.fill_between( a, 1e1*np.ones(100), 1e3*np.ones(100), color = 'gray', alpha = 0.3 )
    plt.text( 2e-7, 10**1.5, 'Open Clusters', color='gray', alpha = 0.4 )
    

    plt.title( "Jeans Mass evolution" )
    plt.xlabel( "Scale factor $[a_0]$" )
    plt.ylabel( 'Mass [M$_{\odot}$]' )
    plt.ylim( (1e1,1e20) )
    plt.xlim( (1e-7,0.1) )
    plt.grid()
    
    #plt.subplot( 122 )
    
    
    #z = np.linspace( z_rc,1e7,200000 )
    #m = MJz(z)
    #z1 = np.linspace( 0.01, z_rc,200000 )
    #m = list(MJpostz(z1)) + list(m)
    #z = list(z1)+list(z)
    #plt.loglog( z, m, label='Jean Mass', color='blue', linewidth=2 );
    
    #z = np.linspace( 0.01, 1e7, 300000 )
    #plt.loglog( z, MJz_Approx(z), '--', color='black' );
    
    #z = np.linspace( 0.01, z_rc ,200000 )
    #plt.loglog( z, MJz(z), '--', color='gray', linewidth=2 );
    
    #plt.legend( loc='upper left' )
    
    ##Epoca de igualdad radiacion materia
    #plt.vlines( z_eq, 1E1, 1E20 )
    #plt.text( 1.3*z_eq,1E6, 'Epoch of $\\rho_{m}=\\rho_{r}$', rotation=90, fontsize=10 )
    ##z de epoca de recombinacion
    #plt.vlines( z_rc, 1E1, 1E20 )
    #plt.text( 1.6*z_rc,1E6, 'Epoch of recombination', rotation=90, fontsize=10 )

    #plt.title( "Jean Mass evolution" )
    #plt.xlabel( "Redshift z" )
    #plt.ylabel( 'Mass [M$_{\odot}$]' )
    #plt.ylim( (1e1,1e20) )
    
    plt.show()


#========================================================================================
# GRAPH 2		(JEANS MASS + SILK MASS)
#========================================================================================
if Graphic==2:
    #Radiation parameter
    OmegaR = 2.44e-5
    #Matter Parameter
    OmegaB = 0.266
    #Equivalent redshift
    z_eq = 12098.
    #Recombination redshift
    z_rc = 1000.
  
    def MJ(a):
	z = 1/a-1
	mj = 1.86927e29*(  ( 1+3/4.*OmegaB/OmegaR*1/(1+z) )*( 1+OmegaB/OmegaR*1/(1+z) )  )**-1.5*(1+z)**-3*OmegaB
	return mj
	
    def MJpost(a):
	z = 1/a-1
	mj = 2.11e5*OmegaB**-0.5*((1+z)/z_rc)**1.5
	return mj

    def MJ_Approx(a):
	z = 1/a-1
	mj = 1.86927e29*(1+z)**-3*OmegaB
	return mj
	
	
    def M_SILK1(a):
	z = 1/a-1
	ms = 3.38e26*OmegaB**-0.5*(1+z)**(-9/2.)
	return ms
	
    def M_SILK2(a):
	z = 1/a-1
	ms = 4.708*10**22.5*OmegaB**(-5/4.)*(1+z)**(-15/4.)
	return ms
	
	
    def MJz(z):
	mj = 1.86927e29*(  ( 1+3/4.*OmegaB/OmegaR*1/(1+z) )*( 1+OmegaB/OmegaR*1/(1+z) )  )**-1.5*(1+z)**-3*OmegaB
	return mj
	
    def MJpostz(z):
	mj = 2.11e5*OmegaB**-0.5*((1+z)/z_rc)**1.5
	return mj
	
    def MJz_Approx(z):
	mj = 1.86927e29*(1+z)**-3*OmegaB
	return mj
	
    def M_SILK1z(z):
	ms = 3.38e26*OmegaB**-0.5*(1+z)**(-9/2.)
	return ms
	
    def M_SILK2z(z):
	ms = 4.708*10**22.5*OmegaB**(-5/4.)*(1+z)**(-15/4.)
	return ms
	

    plt.subplot( 121 )
    a = np.linspace( 1e-7,1/(z_rc+1),200000 )
    m = MJ(a)
    a1 = np.linspace( 1/(z_rc+1),0.1,200000 )
    m = list(m) + list(MJpost(a1))
    a = list(a)+ list(a1)
    plt.loglog( a, m, label='Jean Mass', color='blue', linewidth=2 )
    
    a = np.linspace( 1e-7,1.,200000 )
    plt.loglog( a, MJ_Approx(a), '--', color='black' )
    
    a = np.linspace( 1/(z_rc+1),1,200000 )
    plt.loglog( a, MJ(a), '--', color='gray', linewidth=2 )
    
    
    #SILK MASS
    a = np.linspace( 1e-7,1/(z_eq+1),200000 )
    ms = M_SILK1(a)
    a1 = np.linspace( 1/(z_eq+1), 1/(z_rc+1),200000 )
    ms = list(ms) + list(M_SILK2(a1))
    a = list(a) + list(a1)
    plt.loglog( a, ms, label='Silk Mass', color='red', linewidth=2 )
    
    
    plt.legend( loc='upper left' )
    
    #Epoca de igualdad radiacion materia
    plt.vlines( 1/(z_eq+1), 1E1, 1E20 )
    plt.text( 1.3/(z_eq+1),1E6, 'Epoch of $\\rho_{m}=\\rho_{r}$', rotation=90, fontsize=10 )
    #z de epoca de recombinacion
    plt.vlines( 1/(z_rc+1), 1E1, 1E20 )
    plt.text( 1.6/(z_rc+1),1E6, 'Epoch of recombination', rotation=90, fontsize=10 )

    plt.title( "Jean Mass evolution" )
    plt.xlabel( "Scale factor $[a_0]$" )
    plt.ylabel( 'Mass [M$_{\odot}$]' )
    plt.ylim( (1e1,1e20) )
    
    plt.subplot( 122 )
    
    
    z = np.linspace( z_rc,1e7,200000 )
    m = MJz(z)
    z1 = np.linspace( 0.01, z_rc,200000 )
    m = list(MJpostz(z1)) + list(m)
    z = list(z1)+list(z)
    plt.loglog( z, m, label='Jean Mass', color='blue', linewidth=2 )
    
    z = np.linspace( 0.01, 1e7, 300000 )
    plt.loglog( z, MJz_Approx(z), '--', color='black' )
    
    z = np.linspace( 0.01, z_rc ,200000 )
    plt.loglog( z, MJz(z), '--', color='gray', linewidth=2 )
    
    
    #SILK MASS	
    z = np.linspace( z_eq, 1e7, 200000 )
    ms = M_SILK1z(z)
    z1 = np.linspace( z_rc, z_eq, 200000 )
    ms = list(M_SILK2z(z1)) + list(ms)
    z = list(z1) + list(z)
    plt.loglog( z, ms, label='Silk Mass', color='red', linewidth=2 )
    
    
    plt.legend( loc='upper left' )
    
    #Epoca de igualdad radiacion materia
    plt.vlines( z_eq, 1E1, 1E20 )
    plt.text( 1.3*z_eq,1E6, 'Epoch of $\\rho_{m}=\\rho_{r}$', rotation=90, fontsize=10 )
    #z de epoca de recombinacion
    plt.vlines( z_rc, 1E1, 1E20 )
    plt.text( 1.6*z_rc,1E6, 'Epoch of recombination', rotation=90, fontsize=10 )

    plt.title( "Jean Mass evolution" )
    plt.xlabel( "Redshift z" )
    plt.ylabel( 'Mass [M$_{\odot}$]' )
    plt.ylim( (1e1,1e20) )
    
    plt.show()

#========================================================================================
# GRAPH 3		(MATTER INSTABILITY EVOLUTION)
#========================================================================================
if Graphic==3:
  
    #RK 4 Integrator
    def odestep(odesys,Yini,t,h):
	k1 = odesys( Yini	  , t	    )
	k2 = odesys( Yini+0.5*h*k1, t+0.5*h )
	k3 = odesys( Yini+0.5*h*k2, t+0.5*h )
	k4 = odesys( Yini+h*k3    , t+h     )
	Y = Yini + h*(k1+2*k2+2*k3+k4)/6
	return Y
	
    #Hubble Function of Matter Dominated Regime
    def H2( z ):
	h2 = H0**2*( (1-OmegaM)*(1+z)**2 + OmegaM*(1+z)**3 )
	return h2
	
    #Dynamic Function 
    def F( Y, z ):
	FY = np.zeros( len(Y) )
	#G derivative
	FY[0] = H0**2/(2*H2(z))*OmegaM*(1+z)*( 3*Y[1] - (1+z)*Y[0] )
	#D derivative
	FY[1] = Y[0]
	return FY

    #Numeric Configuration==========================================
    #Maxim redshift
    Zmax = 3000.
    #Step Numbers 1
    Nstep = 10000.
    #Hubble Constant
    H0 = 0.71
    
    #Model with 	OmegaM = 0.1 ===============================
    #Matter Parameter
    OmegaM = 0.1
    
    #First interval --------------------------------    
    Zlog = np.linspace( 0, np.log(Zmax+1), Nstep )
    Z = np.exp( Zlog ) - 1
    
    delta = []
    #initial Conditions ( G(0)=1  D(0)=1 )
    G0 = 1/4.*( OmegaM - ( OmegaM*(OmegaM + 24) )**0.5 )
    Y = [G0,1.]
    i = 0
    for z in Z[:-2]:
        #Redshift step
	h = Z[i+1] - Z[i]
	
	Y = odestep(F,Y,z,h)
	delta.append( Y[1] )
	i += 1
    Z = Z[:-2]
  
    plt.plot( np.log10(1+Z), G0*np.log10((1+Z)), label='$\Omega_{m0}$=%.1f'%OmegaM )
        
    #Model with 	OmegaM = 0.2 ===============================
    #Matter Parameter
    OmegaM = 0.2
    
    #First interval --------------------------------    
    Zlog = np.linspace( 0, np.log(Zmax+1), Nstep )
    Z = np.exp( Zlog ) - 1
    
    delta = []
    #initial Conditions ( G(0)=1  D(0)=1 )
    G0 = 1/4.*( OmegaM - ( OmegaM*(OmegaM + 24) )**0.5 )
    Y = [G0,1.]
    i = 0
    for z in Z[:-2]:
        #Redshift step
	h = Z[i+1] - Z[i]
	
	Y = odestep(F,Y,z,h)
	delta.append( Y[1] )
	i += 1
    Z = Z[:-2]
    plt.plot( np.log10(1+Z), G0*np.log10((1+Z)), label='$\Omega_{m0}$=%.1f'%OmegaM )


    #Model with 	OmegaM = 0.3 ===============================
    #Matter Parameter
    OmegaM = 0.3
    
    #First interval --------------------------------    
    Zlog = np.linspace( 0, np.log(Zmax+1), Nstep )
    Z = np.exp( Zlog ) - 1
    
    delta = []
    #initial Conditions ( G(0)=1  D(0)=1 )
    G0 = 1/4.*( OmegaM - ( OmegaM*(OmegaM + 24) )**0.5 )
    Y = [G0,1.]
    i = 0
    for z in Z[:-2]:
        #Redshift step
	h = Z[i+1] - Z[i]
	
	Y = odestep(F,Y,z,h)
	delta.append( Y[1] )
	i += 1
    Z = Z[:-2]
    plt.plot( np.log10(1+Z), G0*np.log10((1+Z)), label='$\Omega_{m0}$=%.1f'%OmegaM )

    
    #Model with 	OmegaM = 0.5 ===============================
    #Matter Parameter
    OmegaM = 0.5
    
    #First interval --------------------------------    
    Zlog = np.linspace( 0, np.log(Zmax+1), Nstep )
    Z = np.exp( Zlog ) - 1
    
    delta = []
    #initial Conditions ( G(0)=1  D(0)=1 )
    G0 = 1/4.*( OmegaM - ( OmegaM*(OmegaM + 24) )**0.5 )
    Y = [G0,1.]
    i = 0
    for z in Z[:-2]:
        #Redshift step
	h = Z[i+1] - Z[i]
	
	Y = odestep(F,Y,z,h)
	delta.append( Y[1] )
	i += 1
    Z = Z[:-2]
    plt.plot( np.log10(1+Z), G0*np.log10((1+Z)), label='$\Omega_{m0}$=%.1f'%OmegaM )


    #Model with 	OmegaM = 0.9 ===============================
    #Matter Parameter
    OmegaM = 0.9
    
    #First interval --------------------------------    
    Zlog = np.linspace( 0, np.log(Zmax+1), Nstep )
    Z = np.exp( Zlog ) - 1
    
    delta = []
    #initial Conditions ( G(0)=1  D(0)=1 )
    G0 = 1/2.-OmegaM/4. - 1/4.*( OmegaM**2 + 20*OmegaM + 4 )**0.5
    Y = [G0,1.]
    i = 0
    for z in Z[:-2]:
        #Redshift step
	h = Z[i+1] - Z[i]
	
	Y = odestep(F,Y,z,h)
	delta.append( Y[1] )
	i += 1
    Z = Z[:-2]
    plt.plot( np.log10(1+Z), G0*np.log10((1+Z)), label='$\Omega_{m0}$=%.1f'%OmegaM )


    #Model with 	OmegaM = 1.0 ===============================
    #Matter Parameter
    OmegaM = 1
    
    #First interval --------------------------------    
    Zlog = np.linspace( 0, np.log(Zmax+1), Nstep )
    Z = np.exp( Zlog ) - 1
    
    delta = []
    #initial Conditions ( G(0)=1  D(0)=1 )
    G0 = 1/2.-OmegaM/4. - 1/4.*( OmegaM**2 + 20*OmegaM + 4 )**0.5
    Y = [G0,1.]
    i = 0
    for z in Z[:-2]:
        #Redshift step
	h = Z[i+1] - Z[i]
	
	Y = odestep(F,Y,z,h)
	delta.append( Y[1] )
	i += 1
    Z = Z[:-2]
    plt.plot( np.log10(1+Z), G0*np.log10((1+Z)), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    
    plt.title( 'Matter perturbations evolution' )
    plt.xlabel( '$\log(1+z)$' )
    plt.ylabel( '$\log D(z)$' )
    plt.xlim( (np.log10(1+Z[0]),np.log10(1+Z[-1])) )
    plt.ylim( (-3.,0) )
    plt.legend( loc='lower left' )
    plt.show()
    
    
    
#========================================================================================
# GRAPH 4		(MATTER+VACUUM INSTABILITY EVOLUTION)
#========================================================================================
if Graphic==4:
  
    #Hubble Constant
    H0 = 71.0

  
    #Hubble Function of Matter Dominated Regime
    def H( a ):
	h = H0*( OmegaV + OmegaM*a**-3 )**0.5
	return h
	
    #Dynamic Function 
    def Delta( a ):
	d = []
	for i in xrange( 0, len(a) ):
	    dd = H0*integ.quad( lambda x: 1/( x**3*H( x )**(3) ) , 0, a[i] )[0]
	    d.append( 5/2.*H( a[i] )*dd*OmegaM )
	return d
	
	
    #Maxim Redshift
    Zmax = 30.
    #Scale factor
    a = np.linspace( 1/(Zmax+1.), 1., 1000 )
    
    #FACTOR SCALE GRAPHIC================================================================================
    plt.subplot( 122 )
    
    #Matter Parameter
    OmegaM = 0.1
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10(a), np.log10(Delta(a)/Delta([a[-1]])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.2
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10(a), np.log10(Delta(a)/Delta([a[-1]])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.3
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10(a), np.log10(Delta(a)/Delta([a[-1]])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.5
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10(a), np.log10(Delta(a)/Delta([a[-1]])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 1.
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10(a), np.log10(Delta(a)/Delta([a[-1]])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )



    plt.title( 'Matter+Vacuum perturbations evolution\n ($\Omega_{m0}+\Omega_{\lambda 0}=1\ $ model)' )
    plt.xlabel( '$\log(a)$' )
    plt.ylabel( '$\log D(a)$' )
    
    plt.xlim( (np.log10(a[0]), np.log10(a[-1]) ) )
    plt.ylim( (-1.6,0) )
    plt.legend( loc='upper left' )
    
    
    #REDSHIFT GRAPHIC====================================================================================
    plt.subplot(121)
    
    #Scale factor
    z = np.linspace( 0, Zmax, 1000 )
    
    #Matter Parameter
    OmegaM = 0.1
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10( z + 1), np.log10(Delta( 1/(1+z) )/Delta([1/(1+z[0])])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.2
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10( z + 1), np.log10(Delta( 1/(1+z) )/Delta([1/(1+z[0])])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.3
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10( z + 1), np.log10(Delta( 1/(1+z) )/Delta([1/(1+z[0])])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.5
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10( z + 1), np.log10(Delta( 1/(1+z) )/Delta([1/(1+z[0])])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 1.
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10( z + 1), np.log10(Delta( 1/(1+z) )/Delta([1/(1+z[0])])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )


    plt.title( 'Matter+Vacuum perturbations evolution\n ($\Omega_{m0}+\Omega_{\lambda 0}=1\ $ model)' )
    plt.xlabel( '$\log(1+z)$' )
    plt.ylabel( '$\log D(z)$' )
    
    plt.xlim( (np.log10(z[0]+1), np.log10(z[-1]+1) ) )
    #plt.xlim( (np.log10(1+Z[0]),np.log10(1+Z[-1])) )
    plt.ylim( (-1.6,0) )
    plt.legend( loc='lower left' )
    
    
    plt.show()
    
    
#========================================================================================
# GRAPH 5		(MATTER+VACUUM INSTABILITY EVOLUTION)
#========================================================================================
if Graphic==5:
  
    #Hubble Constant
    H0 = 71.0

  
    #Hubble Function of Matter Dominated Regime
    def H( a ):
	h = H0*( (1-OmegaM)*a**-2 + OmegaM*a**-3 )**0.5
	return h
	
	
    #Dynamic Function 
    def Delta( a ):
	d = []
	for i in xrange( 0, len(a) ):
	    dd = H0*integ.quad( lambda x: 1/( x**3*H( x )**(3) ) , 0, a[i] )[0]
	    d.append( 5/2.*H( a[i] )*dd*OmegaM )
	return d
	
	
    #Maxim Redshift
    Zmax = 30.
    #Scale factor
    a = np.linspace( 1/(Zmax+1.), 1., 1000 )
    
    #FACTOR SCALE GRAPHIC================================================================================
    plt.subplot( 122 )
    
    #Matter Parameter
    OmegaM = 0.1
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10(a), np.log10(Delta(a)/Delta([a[-1]])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.2
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10(a), np.log10(Delta(a)/Delta([a[-1]])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.3
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10(a), np.log10(Delta(a)/Delta([a[-1]])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.5
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10(a), np.log10(Delta(a)/Delta([a[-1]])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 1.
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10(a), np.log10(Delta(a)/Delta([a[-1]])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )



    plt.title( 'Matter perturbations evolution' )
    plt.xlabel( '$\log(a)$' )
    plt.ylabel( '$\log D(a)$' )
    
    plt.xlim( (np.log10(a[0]), np.log10(a[-1]) ) )
    plt.ylim( (-1.6,0) )
    plt.legend( loc='lower right' )
    
    
    #REDSHIFT GRAPHIC====================================================================================
    plt.subplot(121)
    
    #Scale factor
    z = np.linspace( 0, Zmax, 1000 )
    
    #Matter Parameter
    OmegaM = 0.1
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10( z + 1), np.log10(Delta( 1/(1+z) )/Delta([1/(1+z[0])])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.2
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10( z + 1), np.log10(Delta( 1/(1+z) )/Delta([1/(1+z[0])])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.3
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10( z + 1), np.log10(Delta( 1/(1+z) )/Delta([1/(1+z[0])])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 0.5
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10( z + 1), np.log10(Delta( 1/(1+z) )/Delta([1/(1+z[0])])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )
    
    #Matter Parameter
    OmegaM = 1.
    #Vacuum Parameter
    OmegaV = 1.0 - OmegaM
    plt.plot( np.log10( z + 1), np.log10(Delta( 1/(1+z) )/Delta([1/(1+z[0])])[0]), label='$\Omega_{m0}$=%.1f'%OmegaM )


    plt.title( 'Matter perturbations evolution' )
    plt.xlabel( '$\log(1+z)$' )
    plt.ylabel( '$\log D(z)$' )
    
    plt.xlim( (np.log10(z[0]+1), np.log10(z[-1]+1) ) )
    #plt.xlim( (np.log10(1+Z[0]),np.log10(1+Z[-1])) )
    plt.ylim( (-1.6,0) )
    plt.legend( loc='lower left' )
    
    plt.show()


#========================================================================================
# GRAPH 6		(F FUNCTION)
#========================================================================================
if Graphic==6:
  
    #Hubble Constant
    H0 = 71.0

  
    #Hubble Function of Matter Dominated Regime
    def H( a, OmegaM ):
	OmegaV = 1 - OmegaM
	h = H0*( OmegaV + OmegaM*a**(-3) )**0.5
	return h
	
    #Dynamic Function 
    def Delta( z, OmegaM ):
      	a = 1/(z+1.)
	d = []
	for i in xrange( 0, len(OmegaM) ):
	    dd = H0*integ.quad( lambda x: 1/( x**3*H( x, OmegaM[i] )**(3) ) , 0, a )[0]
	    d.append( 5/2.*H( a, OmegaM[i] )*OmegaM[i]*dd )
	return d
	
    #F Function 
    def F( z, OmegaM ):
	d = []
	for i in xrange( 0, len(OmegaM) ):
	    f = lambda x: (Delta(x,[OmegaM[i]])[0])
	    d.append( -((1+z)/Delta(z,[OmegaM[i]])[0])*sp.derivative( f , z, dx = 0.00001 ) )
	return d
	
	
    #OmegaM
    OmegaM = np.linspace( 0, 1.0, 500 )
    #F FUNCTION GRAPHIC================================================================================    
    plt.plot( OmegaM , F(0.00, OmegaM), label='Theorical', linewidth=2 )
    plt.plot( OmegaM , OmegaM**0.6, label='$\Omega_m^{0.6}$' )
    
    plt.title( '$f(\Omega_m, z=0)$ function\n ($\Omega_{m0}+\Omega_{\lambda 0}=1\ $ model)' )
    plt.xlabel( '$\Omega_m$' )
    plt.ylabel( '$f(\Omega_m, z=0)$' )
    
    plt.legend( loc='upper left' )
    plt.show()
    
#========================================================================================
# GRAPH 7		(DISTRIBUTION FUNCTION)
#========================================================================================
if Graphic==7:
    def Fr(r):
	return r*np.exp( -r**2/2. )
	
    def Fphi(phi):
	return phi/phi*2*np.pi
	
    
    plt.subplot(122)
    Phi = np.linspace( 0, 2*np.pi, 1000 )
    plt.plot( Phi, Fphi(Phi) )
    
    plt.title( 'Angular Distribution Function $P_{\\phi}( \phi_k )$' )
    plt.xlabel( '$\phi_k$' )
    plt.ylabel( '$P_{\\phi}(\phi_k)$' )
    plt.xlim( (0, 2*np.pi) )
    
    
    plt.subplot(121)
    R = np.linspace( 0, 5, 1000 )
    plt.plot( R, Fr(R) )
    
    plt.title( 'Radial Distribution Function $P_{r}(r_k)$' )
    plt.xlabel( '$r_k/\sqrt{ V_u^{-1}P(k) }$' )
    plt.ylabel( '$P_{r}(r_k)$' )
    plt.xlim( (0, 5) )
    
    plt.show()
	
#========================================================================================
# GRAPH 8		(PERTURBATION FIELD)
#========================================================================================

#def fft2D( X ):
    #f = np.zeros( (N,N), 'complex' )
    #for m in xrange(0,N):
	#for n in xrange(0,N):
	    #for l in xrange(0,N):
		#for k in xrange(0,N):
		    #f[m,n] += 1/(1.0*N)*X[k,l]*np.exp( 2*np.pi*( 1j )*( m*k/(1.0*N) + n*l/(1.0*N) ) )

    #return f
if Graphic==8:
    #Number of matrix sample
    N = 128*4
    #Power Spectrum
    n = 1.
    #Dimension of box
    L = 1.
    
    
    def Pk(k):
	return k**n
    
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
    while( kk<N*N ):
	i = np.random.randint( N )
	j = np.random.randint( N )
	r = np.random.rand()
	kx = 2*np.pi*i/L
	ky = 2*np.pi*j/L
	k = np.sqrt( kx**2 + ky**2 )
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

    #Radial k density component
    #plt.matshow(phi)
    #plt.title( 'Angular sample of $\delta_{k}$' )
    #plt.xlabel( '$n_x$' )
    #plt.ylabel( '$n_y$' )
    
    #Radial k density component
    #plt.matshow( R )
    #plt.title( 'Radial sample of $\delta_{k}$ for $P(k)=k^%d$'%n )
    #plt.xlabel( '$n_x$' )
    #plt.ylabel( '$n_y$' )


    #Real density Field!!
    frr = np.real(fourier.ifft2(X))
    plt.matshow(frr)
    plt.title( 'Real contrast density field for $P(k)=k^%d$'%n )
    plt.xlabel( '$x$ $[L/N]$' )
    plt.ylabel( '$y$ $[L/N]$' )

    plt.show()
    
    #Histograms==============================================================================================
    #Number of hsitograms
    #Nf = 50
    
    #def P1(dd, sigma2):
	#return 1/np.sqrt( 2*np.pi*sigma2 )*np.exp( -dd**2/(2*sigma2) )
      
	
    #Fflat = np.hstack(frr)
    ##Fflat = Fflat/np.max(abs(frr))
    #D_Tam = 1500
    #Delta = np.linspace( -D_Tam, D_Tam, Nf )
    #Ncount = np.zeros( Nf )
    
    #for dd in Fflat:
	#for i in xrange(0,Nf-1):
	    #if dd>Delta[i] and dd<=Delta[i+1]:
		#Ncount[i] += 1
		
    #Ncount = Ncount/(N*N*1.0)*Nf/(2*D_Tam)
    #sigma2 = np.max(Ncount)**-2/(2*np.pi)
		
    #plt.plot( Delta, Ncount, 'o-' )
    #plt.plot( Delta, P1(Delta, sigma2) )
    #plt.title( 'Histograms for contrast density field, for $P(k)=k^%d$\n$\sigma^2=\chi(0)=%2.3f$'%(n,sigma2) )
    #plt.ylabel( 'Number of contrast' )
    #plt.xlabel( '$\delta_{k}$' )
    
    #plt.show()