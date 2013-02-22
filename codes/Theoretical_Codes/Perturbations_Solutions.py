execfile('_head.py')

#==================================================================================================
#			FUNCTION
#==================================================================================================
#Reference Scale Factor
a_ref = 1e-4
#Matter Dominated Perturbations
def EinstendeSitterDelta( a ):
    return (a/a_ref)**1
    
#Radiation Dominated Perturbations
def RadiationDelta( a ):
    return (a/a_ref)**(1.22)
    
#Radiation Dominated Perturbations
def VacuumDelta( a ):
    return (a/a_ref)**(0.58)

#==================================================================================================
#			PLOTTING RESULTS
#==================================================================================================
#Scale Factor array
A = np.linspace( 0, 1, 10000 )

#Einsten-de Sitter
delta_ES = EinstendeSitterDelta( A )
  #Plot
plt.semilogy( A, delta_ES, color = 'red', linewidth = 2, label='Matter perturbations' )


#Radiation Universe
delta_R = RadiationDelta( A )
  #Plot
plt.semilogy( A, delta_R, color = 'blue', linewidth = 2, label='Radiation perturbations' )


#Vacuum Universe
delta_L = VacuumDelta( A )
  #Plot
plt.loglog( A, delta_L, color = 'green', linewidth = 2, label='Vacuum perturbations' )



plt.xlabel( "factor scale $a$ [$a_0$]" )
plt.ylabel( "Density parameter [$\delta_{k, 0 }$]" )

plt.title( "Density parameter $\delta_{k}(t)$ for differents cosmologies" )
plt.grid()
plt.legend( loc='upper left', fancybox = True, shadow = True, title="Universes" )

plt.xlim( (1e-4,1) )
plt.show()