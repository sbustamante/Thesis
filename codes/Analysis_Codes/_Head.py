#==================================================================================================
#			HEADERS
#==================================================================================================
from __future__ import division
from struct import *
import numpy as np
import sys
import matplotlib
import os
import matplotlib.pyplot as plt
from pylab import *
import scipy.integrate as integ
import scipy.interpolate as interp
import matplotlib.gridspec as gridspec
from matplotlib.patches import Ellipse


#==================================================================================================
#			VARIABLES
#==================================================================================================
#Global Fold
foldglobal = '../../data/'



#==================================================================================================
#			FUNCTIONS
#==================================================================================================

#..................................................................................................
#Cutting Halos in X axe
#..................................................................................................
def CutHaloX( X, thick, datos, plot=True, color='black' ):
    #Initial data
    ncol = len(datos)		#Number of columns
    nrow = len(datos[0])	#Number of rows
    Box_lenght = np.max( tuple(datos[1])+tuple(datos[2])+tuple(datos[3]) )#h^-1 Mpc

    
    #Sorting in x axe
    argx = list( np.argsort( datos[1] ) )
    for i in xrange(0, ncol):
	datos[i] = datos[i][argx]
    
    if X<=thick:
	i_star = 0
    else:
	i_star = int(Box_lenght/(X - thick))
    
    i1 = 0
    i2 = -1
    for i in xrange(i_star,nrow):
	if datos[1][i] >= X and i1==0:
	    i1 = i
	if datos[1][i] >= X + thick and i2==-1:
	    i2 = i
	    break

    #Plotting results
    if plot == True:
	plt.title('Cut in X axes between %3.1f and %3.1f'%(X, X + thick))
	plt.plot( datos[2][i1:i2], datos[3][i1:i2], '.', color=color )
	plt.xlim( (0,Box_lenght) )
	plt.ylim( (0,Box_lenght) )
	plt.xlabel('y [$h^{-1}$Mpc]')
	plt.ylabel('z [$h^{-1}$Mpc]')
	plt.show()
    else:
	return [datos[2][i1:i2], datos[3][i1:i2]], datos[0][i1:i2]


#..................................................................................................
#Cutting Halos in Y axe 
#..................................................................................................
def CutHaloY( Y, thick, datos, plot=True, color='black' ):
    #Initial data
    ncol = len(datos)		#Number of columns
    nrow = len(datos[0])	#Number of rows
    Box_lenght = np.max( tuple(datos[1])+tuple(datos[2])+tuple(datos[3]) )#h^-1 Mpc
  
    #Sorting in x axe
    argx = list( np.argsort( datos[2] ) )
    for i in xrange(0, ncol):
	datos[i] = datos[i][argx]
    
    if Y<=thick:
	i_star = 0
    else:
	i_star = int(Box_lenght/(Y - thick))
    
    i1 = 0
    i2 = -1
    for i in xrange(i_star,nrow):
	if datos[2][i] >= Y and i1==0:
	    i1 = i
	if datos[2][i] >= Y + thick and i2==-1:
	    i2 = i
	    break

    #Plotting results	    
    if plot == True:    
	plt.title('Cut in Y axes between %3.1f and %3.1f'%(Y, Y + thick))
	plt.plot( datos[1][i1:i2], datos[3][i1:i2], '.', color=color )
	plt.xlim( (0,Box_lenght) )
	plt.ylim( (0,Box_lenght) )
	plt.xlabel('x [$h^{-1}$Mpc]')
	plt.ylabel('z [$h^{-1}$Mpc]')
	plt.show()
    else:
	return [datos[1][i1:i2], datos[3][i1:i2]], datos[0][i1:i2]


#..................................................................................................
#Cutting Halos in Z axe
#..................................................................................................
def CutHaloZ( Z, thick, datos, plot=True, color='black' ):
    #Initial data
    ncol = len(datos)		#Number of columns
    nrow = len(datos[0])	#Number of rows
    Box_lenght = np.max( tuple(datos[1])+tuple(datos[2])+tuple(datos[3]) )#h^-1 Mpc

    #Sorting in x axe
    argx = list( np.argsort( datos[3] ) )
    for i in xrange(0, ncol):
	datos[i] = datos[i][argx]
    
    if Z<=thick:
	i_star = 0
    else:
	i_star = int(Box_lenght/(Z - thick))
    
    i1 = 0
    i2 = -1
    for i in xrange(i_star,nrow):
	if datos[3][i] >= Z and i1==0:
	    i1 = i
	if datos[3][i] >= Z + thick and i2==-1:
	    i2 = i
	    break

    #Plotting results	    
    if plot == True:    
	plt.title('Cut in Z axes between %3.1f and %3.1f'%(Y, Y + thick))
	plt.plot( datos[1][i1:i2], datos[2][i1:i2], '.', color=color )
	plt.xlim( (0,Box_lenght) )
	plt.ylim( (0,Box_lenght) )
	plt.xlabel('x [$h^{-1}$Mpc]')
	plt.ylabel('y [$h^{-1}$Mpc]')
	plt.show()
    else:
	return [datos[1][i1:i2], datos[2][i1:i2]], datos[0][i1:i2]
	
	
	
#..................................................................................................
#Cutting Density field in X/Y/Z axe
#..................................................................................................
def CutFieldZ( filename, X, res=32, Coor = 3 ):
    '''
    Coor  1 -- X      2 -- Y      3 -- Z
    '''
    os.system( "./Field_Cut%d.out %s %d temp.tmp %d"%( res, filename, X, Coor ) )
    datos = np.loadtxt( 'temp.tmp' )
    N = int(np.sqrt(len( datos )))
    datos = datos.reshape( (N, N) )
    os.system( "rm temp.tmp" )
    return datos
    
    
#..................................................................................................
#Correlation bewteen density and eigenvalues
#..................................................................................................
def Correlation( filename_eig, filename_delta, min_L, max_L, N_L ):
    os.system( "./Lambda_Correlation.out %s %s %f %f %d temp.tmp"%( 
    filename_eig, filename_delta, min_L, max_L, N_L ) )
    datos = np.transpose( np.loadtxt( 'temp.tmp' ) )
    os.system( "rm temp.tmp" )
    return datos
    
    
#..................................................................................................
#Correlation bewteen density and eigenvalues
#..................................................................................................
def Counts( filename_eig, filename_delta, min_L, max_L, N_L ):
    os.system( "./Density_Regions.out %s %s %f %f %d temp.tmp"%( 
    filename_eig, filename_delta, min_L, max_L, N_L ) )
    datos = np.transpose( np.loadtxt( 'temp.tmp' ) )
    os.system( "rm temp.tmp" )
    return datos
    
    
#..................................................................................................
#Classification Scheme
#..................................................................................................
def Scheme( eig1, eig2, eig3, Lamb ):
    N = len( eig1 )
    sch = 0*eig1
    
    for i in xrange(N):
	for j in xrange(N):
	    if eig1[i,j] > Lamb:
		sch[i,j] += 1
	    if eig2[i,j] > Lamb:
		sch[i,j] += 1
	    if eig3[i,j] > Lamb:
		sch[i,j] += 1
    return sch
    
    
#..................................................................................................
#Energy and angular mometum of pairs system
#..................................................................................................
def Energy_AngularM( M1, x1, y1, z1, vx1, vy1, vz1, M2, x2, y2, z2, vx2, vy2, vz2):
 
    #km to MPC
    KM2MPC = 3.24077929e-20
    #kg to MSUN
    KG2MSUN = 5.05e-31*0.71
    #Cavendish
    G = 6.6742e-11*(1e-3*KM2MPC)**3/KG2MSUN
 
    E = np.zeros( len(M1) )
    L = np.zeros( (len(M1),3) )
    for i in xrange( len(M1) ):
	m1 = M1[i]
	r1 = np.array( (x1[i],y1[i],z1[i]) )
	v1 = np.array( (vx1[i],vy1[i],vz1[i]) )
	m2 = M2[i]
	r2 = np.array( (x2[i],y2[i],z2[i]) )
	v2 = np.array( (vx2[i],vy2[i],vz2[i]) )
    
	#Center of mass
	Rcm = (m1*r1 + m2*r2)/(m1 + m2)
	#Mean Velocity
	Vcm = (m1*v1 + m2*v2)/(m1 + m2)
	#Center of mass coordinates
	r1p = r1 - Rcm
	r2p = r2 - Rcm
	#Peculiar velocities + Hubble flow
	v1p = v1 - Vcm + 100*r1p
	v2p = v2 - Vcm + 100*r2p
    
	L[i] = (m1*np.cross( r1p, v1p ) + m2*np.cross( r2p, v2p ))/(m1+m2)
	E[i] = (0.5*( m1*norm(v1p)**2 + m2*norm(v2p)**2 )*KM2MPC**2 - G*m1*m2/( norm(r1p - r2p) ) )/(m1+m2)
    
    return E, L
    

#..................................................................................................
#Classification Scheme 1D
#..................................................................................................
def Scheme1D( eig1, eig2, eig3, Lamb_min, Lamb_max, N_L ):
    N = len( eig1 )
    
    L_thr = np.linspace( Lamb_min, Lamb_max, N_L )
    Ncount = np.zeros( (4,N_L) )
    
    for i in xrange(N):
	for j in xrange(N_L):  
	    if eig1[i] <= L_thr[j] and eig2[i] <= L_thr[j] and eig3[i] <= L_thr[j]:
		Ncount[0,j] += 1
	    if eig1[i] > L_thr[j] and eig2[i] <= L_thr[j] and eig3[i] <= L_thr[j]:
		Ncount[1,j] += 1
	    if eig1[i] > L_thr[j] and eig2[i] > L_thr[j] and eig3[i] <= L_thr[j]:
		Ncount[2,j] += 1
	    if eig1[i] > L_thr[j] and eig2[i] > L_thr[j] and eig3[i] > L_thr[j]:
		Ncount[3,j] += 1
	      
    return L_thr, Ncount
    
    
#..................................................................................................
#Fractional Anisotropy
#..................................................................................................
def Fractional_Anisotropy( eig1, eig2, eig3 ):

    FA = 1/np.sqrt(3.)*np.sqrt( ( (eig1 - eig3)**2 + (eig2 - eig3)**2 + (eig1 - eig2)**2 )/ \
    (eig1**2 + eig2**2 + eig3**2))

    return FA
    
    
#..................................................................................................
#Loader of i,j,k element of data
#..................................................................................................
def Loader( filename, X, Y, Z, res=32 ):
    datos = np.transpose(CutFieldZ( filename, X, res=32, Coor = 1 ))
    return datos[ Y, Z ]
    

#..................................................................................................
#1D Cells Histogram
#..................................................................................................
def EigenHist1D( filename, Number, Lambda_val, N ):
    os.system( "./Lambda_Histograms.out %s 10 %d %f %d"%( filename, N, Lambda_val, Number - 1 ) )
    datos = np.transpose(np.loadtxt( 'temp.tmp' ))
    os.system( "rm temp.tmp" )
    return datos
    

#..................................................................................................
#1D Cells Histogram Variance
#..................................................................................................
def EigenHist1DVariance( filename, Number, Lambda_val, N, Ndiv ):
    os.system( "./Lambda_Histograms_Variance.out %s %d %f %d %d"%( filename, N, Lambda_val, Ndiv, Number - 1 ) )
    datos = np.transpose(np.loadtxt( 'temp.tmp' ))
    os.system( "rm temp.tmp" )
    
    #Extracting Extreme curve
    L_min = 10*np.ones( N )
    L_max = np.zeros( N )
    for l in xrange( N ):
	for i in xrange( Ndiv**3 ):
	    #Minim curve	
	    if datos[i+1,l]/(np.sum(datos[i+1,:])*2.*Lambda_val/N) <= L_min[l]:
		L_min[l] = datos[i+1,l]/(np.sum(datos[i+1,:])*2.*Lambda_val/N)
	    #Maxim curve	
	    if datos[i+1,l]/(np.sum(datos[i+1,:])*2.*Lambda_val/N) >= L_max[l]:
		L_max[l] = datos[i+1,l]/(np.sum(datos[i+1,:])*2.*Lambda_val/N)
    
    return datos[0], L_min, L_max


#..................................................................................................
#2D Cells Histogram
#..................................................................................................
def EigenHist2D( filename, Lambda_val, N, Lij ):
    if( Lij == "12" ):
	Number = 3
    if( Lij == "13" ):
	Number = 4
	
    os.system( "./Lambda_Histograms.out %s %d 10 %f %d"%( filename, N, Lambda_val, Number  ) )
    datos = np.transpose(np.loadtxt( 'temp.tmp' )[::,::-1])
    os.system( "rm temp.tmp" )
    return datos


#..................................................................................................
#Manual 1D histogram
#..................................................................................................
def Hist1D( Lambda, Lambda_val, N ):
    
    L = np.linspace( -Lambda_val, Lambda_val, N )
    Counts = np.zeros(N)
    for i in xrange( len(Lambda) ):
	if Lambda_val > Lambda[i] > -Lambda_val:
	    j = int( N*(Lambda[i] + Lambda_val)/(2*Lambda_val) )
	    Counts[j] += 1
	
    return L, Counts
    

#..................................................................................................
#Normalization of histograms
#..................................................................................................
def Norml( L1, L2 ):
    Lfunc = interp.interp1d( L1, L2 )
    Norm = integ.quad( Lfunc, np.min(L1), np.max(L1) )[0]
    return Norm

#==================================================================================================
#			MISCELLANEOUS
#==================================================================================================
    
def progress(width, percent):
    marks = math.floor(width * (percent / 100.0))
    spaces = math.floor(width - marks)
 
    loader = '[' + ('=' * int(marks)) + (' ' * int(spaces)) + ']'
 
    sys.stdout.write("%s %d%%\r" % (loader, percent))
    if percent >= 100:
        sys.stdout.write("\n")
    sys.stdout.flush()