# -*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import sys

if len(sys.argv) == 1:
    print "Number of octants and filename is required!"


n = int(sys.argv[1])		#Number of octants in space
N = (2**n)			#Number of partitions for data file
filename = sys.argv[2]		#Filename of external data file


datos = np.transpose( np.loadtxt( filename ) )
ncol = len(datos)		#Number of columns
nrow = len(datos[0])		#Number of rows

#Sort in x coordinate
argx = list( np.argsort( datos[1] ) )
for i in xrange(0, ncol):
    datos[i] = datos[i][argx]

#Sort in y coordinate
Nx = nrow/N
for j in xrange(0,N):
    argy = list( np.argsort( datos[2][j*Nx:(j+1)*Nx-1] ) )
    for i in xrange(0, ncol):
	datos[i][j*Nx:(j+1)*Nx-1] = datos[i][j*Nx:(j+1)*Nx-1][argy]
    
#Sort in y coordinate
Ny = nrow/(N**2)
for j in xrange(0,N):
      for k in xrange(0,N):
	  argz = list( np.argsort( datos[3][j*Nx:(j+1)*Nx-1][k*Ny:(k+1)*Ny-1] ) )
	  for i in xrange(0, ncol):
	      datos[i][j*Nx:(j+1)*Nx-1][k*Ny:(k+1)*Ny-1] = datos[i][j*Nx:(j+1)*Nx-1][k*Ny:(k+1)*Ny-1][argz]
Nz = nrow/(N**3)

#Saving sorted datas
np.savetxt( "P%s"%(filename), np.transpose(datos),\
fmt='%d\t%3.3f\t%3.3f\t%3.3f\t%3.1f\t%3.1f\t%3.1f\t%d\t%0.4e\t%1.4e\t%4.2f\t%1.4e\t%3.1f\t%0.4e' )