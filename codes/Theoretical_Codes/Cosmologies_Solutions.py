execfile('_head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Matter density
Omega_m = 0.2669

#Radiation density
Omega_r = 8.24e-5

#Vacuum density
Omega_L = 0.734

#Hubble constant
H0 = 71.0


#==================================================================================================
#			DIFFERENTS COSMOLOGIES
#==================================================================================================

def Einstein_deSitter( a ):
    ta = 2*a**(3/2.)/3.
    return ta
    
def Radiation_Universe( a ):
    ta = a**2/2.
    return ta
    
def Closed_Radiation_Universe( a, Omega_r ):
    ta = 1/(Omega_r-1)*( Omega_r**0.5 - ( a**2*(1 - Omega_r) + Omega_r )**0.5 )
    return ta
    
def Vacuum_Universe( a ):
    ta = 1/(Omega_L**0.5)*np.log( a*(Omega_L/(1 - Omega_L))**0.5 + \
    ( 1 + Omega_L/(1 - Omega_L)*a**2 )**0.5 )
    return ta
    
def WMAP7_Universe( a ):
    ta = []
    for ai in a:
	ta.append(  integ.quad(lambda ap:
	(Omega_m/ap + Omega_r/ap**2 + Omega_L*ap**2)**(-0.5), 0.001, ai )[0])
    return ta
    
    

#==================================================================================================
#			PLOTTING RESULTS
#==================================================================================================
#Scale Factor array
A = np.linspace( 0, 2, 1000 )

#Einsten-de Sitter
ta_ES = Einstein_deSitter( A )  
ta_ES = Einstein_deSitter( A )  - 	\
Einstein_deSitter( 1.0 )  	+	\
Einstein_deSitter( interp.interp1d( ta_ES, A )(1.0) )
  #Plot
plt.plot( ta_ES, A, color = 'burlywood', linewidth = 2, label='Einsten-de Sitter universe' )


#Radiation Universe
ta_R = Radiation_Universe( A )
ta_R = Radiation_Universe( A )  -	\
Radiation_Universe( 1.0 )  	+	\
Radiation_Universe( interp.interp1d( ta_R, A )(1.0) )
  #Plot
plt.plot( ta_R, A, color = 'blue', linewidth = 2, label='Flat radiation universe' )


#Close Radiation Universe
ta_CR = Closed_Radiation_Universe( A, 2 )
ta_CR = Closed_Radiation_Universe( A, 2 )-	\
Closed_Radiation_Universe( 1.0, 2 )  	 +	\
Closed_Radiation_Universe( interp.interp1d( ta_CR[:700], A[:700] )(1.0), 2.0 )
  #Plot
plt.plot( ta_CR, A, color = 'red', linewidth = 2 )
plt.plot( 2*ta_CR[706]-ta_CR, A, color = 'red', linewidth = 2, label='Closed radiation universe' )


#Vacuum Universe
ta_L = Vacuum_Universe( A )
ta_L = Vacuum_Universe( A )	-	\
Vacuum_Universe( 1.0 )  	+	\
Vacuum_Universe( interp.interp1d( ta_L, A )(1.0) )
  #Plot
plt.plot( ta_L, A, color = 'green', linewidth = 2, label='Vacuum universe' )


#WMAP7 Universe
ta_WMAP = WMAP7_Universe( A )
plt.plot( ta_WMAP, A, color = 'black', linewidth = 2, label = 'WMAP7 universe' )

plt.xlabel( "time $t$ [$H_0^{-1}$]" )
plt.ylabel( "factor scale $a$" )
plt.text( 1.5, 0.9, "current factor scale $a_0=1$", fontsize = 11)
plt.text( 0.88, 1.05, "current universe age $t_0=1/H_0$", fontsize = 11, rotation=90)
plt.title( "Scale factor $a(t)$ for differents cosmologies" )
plt.grid()
plt.legend( loc='lower right', fancybox = True, shadow = True, title="Universes" )

plt.hlines( 1, 0, 3.0, linestyle = '--', linewidth = 2, color = 'gray' )
plt.vlines( 1.0, 0, 2, linestyle = '--', linewidth = 2, color = 'gray' )
plt.xlim( (0,3) )
plt.show()





