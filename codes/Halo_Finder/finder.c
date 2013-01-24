#include <allvars.h>

/**************************************************************************************************
 NAME:       distance
 FUNCTION:   calculate distance between two vectors
 INPUTS:     two 3D arrays, 3 type int with boundary conditions, Box length
 RETURN:     0
**************************************************************************************************/
float distance( float r1[3],
	        float r2[3],
		int ic, int jc, int kc,
		float Lbox)
{    
    return pow( pow( ic*Lbox - fabs(r1[X]-r2[X]), 2. ) +
		pow( jc*Lbox - fabs(r1[Y]-r2[Y]), 2. ) +
		pow( kc*Lbox - fabs(r1[Z]-r2[Z]), 2. ) , 0.5 );
}


/**************************************************************************************************
 NAME:       radial_vel
 FUNCTION:   calculate radial velocity between two halos
 INPUTS:     four 3D arrays (v1, v2, r1, r2), 3 type int with boundary conditions, Box length
 RETURN:     0
**************************************************************************************************/
float radial_vel( float v1[3],
		  float v2[3],
		  float r1[3],
		  float r2[3],
		  int ic, int jc, int kc,
		  float Lbox)
{   
    float magr, Vrad;
    magr = distance( r1, r2, ic, jc, kc, Lbox);
  
    Vrad = 0;
    if(ic == 0)	Vrad += (v1[X]-v2[X])*(r1[X]-r2[X]);
    if(ic == 1)	Vrad += (v1[X]-v2[X])*(r1[X]-r2[X])*( fabs(r1[X]-r2[X]) - Lbox )/fabs(r1[X]-r2[X]);
    
    if(jc == 0)	Vrad += (v1[Y]-v2[Y])*(r1[Y]-r2[Y]);
    if(jc == 1)	Vrad += (v1[Y]-v2[Y])*(r1[Y]-r2[Y])*( fabs(r1[Y]-r2[Y]) - Lbox )/fabs(r1[Y]-r2[Y]);
    
    if(kc == 0)	Vrad += (v1[Z]-v2[Z])*(r1[Z]-r2[Z]);
    if(kc == 1)	Vrad += (v1[Z]-v2[Z])*(r1[Z]-r2[Z])*( fabs(r1[Z]-r2[Z]) - Lbox )/fabs(r1[Z]-r2[Z]);
    	   
    return Vrad/magr;
}


/**************************************************************************************************
 NAME:	     make_regions
 FUNCTION:   Construct octant regions of box
 INPUTS:     Matrix of region struct, Halo Structure with halos, number of halos, 
	     number of division in each axe, length of box
 RETURN:     0
**************************************************************************************************/
int make_regions( struct region regions[NMAX2][NMAX2][NMAX2], 
		  struct halo halos[], 
		  int Nhalos, int Naxe, float Lbox, 
		  int index[NMAX1][3] )
{
    int i,j,k;
    int l, m, n;
    int ic, jc, kc;
    int it, jt, kt;
    int Nreg = (int)pow(Naxe,3);
    
    l=0;
    for( i=0; i<Naxe; i++ )
    for( j=0; j<Naxe; j++ )
    for( k=0; k<Naxe; k++ )      
    {
	regions[i][j][k].Rcor[X] = i*Lbox/Naxe;
	regions[i][j][k].Rcor[X] = j*Lbox/Naxe;
	regions[i][j][k].Rcor[Z] = k*Lbox/Naxe;
	regions[i][j][k].id = l;
	
	//Reset the region halos counter
	n = 0;
	regions[i][j][k].Nhalos = 0;
	for( m=0; m<Nhalos; m++ ){
	    if( halos[m].r[X] >= i*Lbox/Naxe && halos[m].r[X] < (i+1)*Lbox/Naxe )
	    if( halos[m].r[Y] >= j*Lbox/Naxe && halos[m].r[Y] < (j+1)*Lbox/Naxe )
	    if( halos[m].r[Z] >= k*Lbox/Naxe && halos[m].r[Z] < (k+1)*Lbox/Naxe ){
		regions[i][j][k].HalosId[n] = m;
		regions[i][j][k].Nhalos++;
		halos[m].oct = l;
		n++;}}
	
	//Index regions construction
	index[l][0] = i; index[l][1] = j; index[l][2] = k;
	regions[i][j][k].Nneigh = 0;
	l += 1;
    }
    
    //Setting the Neighborhood
    for( i=0; i<Naxe; i++ )
    for( j=0; j<Naxe; j++ )
    for( k=0; k<Naxe; k++ )      
    {
	l = regions[i][j][k].id;
	
	for( ic=-1; ic<=1; ic++ )
	for( jc=-1; jc<=1; jc++ )
	for( kc=-1; kc<=1; kc++ ){  	
	  
	    it = i + ic; jt = j + jc; kt = k + kc;
	    //Neighbor out of limits (Periodic boundary conditions) (X direction)
	    if( i+ic>=Naxe )		it = 0;
	    if( i+ic<0 )		it = Naxe -1;
	    //Neighbor out of limits (Periodic boundary conditions) (Y direction)
	    if( j+jc>=Naxe )		jt = 0;
	    if( j+jc<0 )		jt = Naxe -1;
	    //Neighbor out of limits (Periodic boundary conditions) (Z direction)
	    if( k+kc>=Naxe )		kt = 0;
	    if( k+kc<0 )		kt = Naxe -1;
	    
	    m = regions[it][jt][kt].Nneigh;
	    //Id of neighbors
	    regions[it][jt][kt].neigh[m] = l;
	    //Augment number of neighbors
	    regions[it][jt][kt].Nneigh += 1;
	    
	    regions[it][jt][kt].cond_neigh[m][0] = 0;
	    regions[it][jt][kt].cond_neigh[m][1] = 0;
	    regions[it][jt][kt].cond_neigh[m][2] = 0;

	    if( i+ic<0 || i+ic>=Naxe )
		regions[it][jt][kt].cond_neigh[m][0] = 1;
	    if( j+jc<0 || j+jc>=Naxe )
		regions[it][jt][kt].cond_neigh[m][1] = 1;
	    if( k+kc<0 || k+kc>=Naxe )
		regions[it][jt][kt].cond_neigh[m][2] = 1;
	    }}
    return 0;
}


/**************************************************************************************************
 NAME:	     pair_finder
 FUNCTION:   Construct octant regions of box
 INPUTS:     Halo struct with halos, Pair struct with empty general pairs sample, 
	     Pair struct with empty isolated pair sample, Matrix of region struct, number of 
	     octants, length of box
 RETURN:     0
**************************************************************************************************/
int pair_finder( struct halo halos[], 
		 struct pair pairs[], 
		 struct pair isopair[],
		 struct region regions[NMAX2][NMAX2][NMAX2],
		 int index[NMAX1][3],
		 float p[NMAX1] )
{
    int i, j, k;
    int ch1, ch2;
    int h1, h2;
    int r1, r2;
    int c1, c2, c3;
    
    float rclos1_n, rclos2_n;
    float rclos1_m, rclos2_m;
    float rclos1_M, rclos2_M;
    float rclos1_u, rclos2_u;
    
    float Rpmass1, Rpmass2;

    //Counter of Halos in mass range
    c3 = 0;
    //Sweeping each region
    for( r1=0; r1<pow(p[NAXE],3); r1++ )
    {
	//Index of current region
	i = index[r1][0]; j = index[r1][1]; k = index[r1][2];
  	printf( "\tActually in Region #%d\n", r1 );

	//Sweeping each halo in current region
	for( ch1=0; ch1<regions[i][j][k].Nhalos; ch1++ )
	{
	    //Id of halos in current region r1
	    h1 = regions[i][j][k].HalosId[ch1];
	    
	    //Halo 1 mass in range Mmin<M<Mmax
	    if( halos[h1].Mass>=p[MMIN] && halos[h1].Mass<=p[MMAX] ){
		c3 += 1;
		//Initializing some closest distances for current halo
		rclos1_n = 2*p[LBOX];	 rclos2_n = 2*p[LBOX];
		rclos1_m = 2*p[LBOX];	 rclos2_m = 2*p[LBOX];
		rclos1_M = 2*p[LBOX];	 rclos2_M = 2*p[LBOX];
		rclos1_u = 2*p[LBOX];	 rclos2_u = 2*p[LBOX];
		halos[h1].idpmas[0] = 0; halos[h1].idpmas[1] = 0;
		
		//Reset of pair index of current halo
		halos[h1].idpair = -1;
		
		//Sweeping each neighbor region
		for( c1=0; c1<regions[i][j][k].Nneigh; c1++ ){
		    //Id of current neighbor region
		    r2 = regions[i][j][k].neigh[c1];

		    //Sweeping each halo in neighbor region
		    for( ch2=0; ch2<regions[ index[r2][0] ][ index[r2][1] ][ index[r2][2] ].Nhalos; ch2++ ){
		      
		      	//Id of halos in current region r2
			h2 = regions[ index[r2][0] ][ index[r2][1] ][ index[r2][2] ].HalosId[ch2];
	
			//Halo With more mass of current halo--------------------------------------
  			if( halos[h2].Mass>halos[h1].Mass ){
			    rclos1_m = distance( halos[h1].r, halos[h2].r, 
						 regions[i][j][k].cond_neigh[c1][0],
						 regions[i][j][k].cond_neigh[c1][1],
						 regions[i][j][k].cond_neigh[c1][2],
						 p[LBOX] );
			    if( rclos1_m <= rclos2_m ){
				//First Closest halo
				halos[h1].Rpmas[0] = rclos1_m;
				halos[h1].idpmas[1] = halos[h1].idpmas[0];
				//Second Closest halo
				halos[h1].Rpmas[1] = rclos2_m;
				halos[h1].idpmas[0] = halos[h2].id_or;
				rclos2_m = rclos1_m;}}
			//-------------------------------------------------------------------------
			
			//Halo With Maxim Mass limit for isolated pairs----------------------------
  			if( halos[h2].Mass>p[MMMAX] && h1!=h2 ){
			    rclos1_M = distance( halos[h1].r, halos[h2].r, 
						 regions[i][j][k].cond_neigh[c1][0],
						 regions[i][j][k].cond_neigh[c1][1],
						 regions[i][j][k].cond_neigh[c1][2],
						 p[LBOX] );
			    if( rclos1_M <= rclos2_M ){
				halos[h1].Rmmas = rclos1_M;
				halos[h1].idmmas = halos[h2].id_or;
				rclos2_M = rclos1_M;}}
			//-------------------------------------------------------------------------
			
			//Halo 2 mass in range Mmin<M<Mmax-----------------------------------------
  			if( halos[h2].Mass>=p[MMIN] && halos[h2].Mass<=p[MMAX] && h1!=h2 ){
			    rclos1_n = distance( halos[h1].r, halos[h2].r, 
						 regions[i][j][k].cond_neigh[c1][0],
						 regions[i][j][k].cond_neigh[c1][1],
						 regions[i][j][k].cond_neigh[c1][2],
						 p[LBOX] );
			    if( rclos1_n <= rclos2_n ){
				halos[h1].Rclos = rclos1_n;
				halos[h1].idclos = h2;
				rclos2_n = rclos1_n;
				
				//Conditions of region of companion halo 1
				halos[h1].cond_comp[0] = regions[i][j][k].cond_neigh[c1][0];
				halos[h1].cond_comp[1] = regions[i][j][k].cond_neigh[c1][1];
				halos[h1].cond_comp[2] = regions[i][j][k].cond_neigh[c1][2];}}
			//-------------------------------------------------------------------------
			
			//Halo 2 mass M>Mmax-------------------------------------------------------
  			if( halos[h2].Mass>p[MMAX] ){
			    rclos1_u = distance( halos[h1].r, halos[h2].r, 
						 regions[i][j][k].cond_neigh[c1][0],
						 regions[i][j][k].cond_neigh[c1][1],
						 regions[i][j][k].cond_neigh[c1][2],
						 p[LBOX] );
			    if( rclos1_u <= rclos2_u ){
				halos[h1].Rumas = rclos1_u;
				halos[h1].idumas = halos[h2].id_or;
				rclos2_u = rclos1_u;}}
			//-------------------------------------------------------------------------
			
			}}}

	}}

      //Halo Pair assignation
      c1 = 0;	//counter of general pair sample
      c2 = 0;	//counter of isolated pair sample
      for( h1=0; h1<p[NDAT]; h1++ ){
	  //Halo 1 mass in range Mmin<M<Mmax
	  if( halos[h1].Mass>=p[MMIN] && halos[h1].Mass<=p[MMAX] ){
	      //Condition for a halo is not in a pair
	      if( halos[h1].idpair == -1 ){
		  h2 = halos[h1].idclos;
		  //Halo 2 mass in range Mmin<M<Mmax
		  if( halos[h2].Mass>=p[MMIN] && halos[h2].Mass<=p[MMAX] )
		      //If each halo is the closest to other,
 		      if( halos[h1].idclos == halos[h2].id && halos[h2].idclos == halos[h1].id &&
		      //and any halo with upper mass limit isn't closer that its companion, they form a pair
			  halos[h1].Rumas>halos[h1].Rclos && halos[h2].Rumas>halos[h2].Rclos ){
			  //GENERAL HALO PAIRS SAMPLES --------------------------------------------
			  //Mass of halo 1
			  pairs[c1].M1 = halos[h1].Mass;
			  //Id of halo 1
			  pairs[c1].id1 = halos[h1].id;
			  //Region of halo 1
			  pairs[c1].oct1 = halos[h1].oct;
			  
			  //Mass of halo 2
			  pairs[c1].M2 = halos[h2].Mass;
			  //Id of halo 2
			  pairs[c1].id2 = halos[h2].id;
			  //Region of halo 2
			  pairs[c1].oct2 = halos[h2].oct;
			  
			  //Distance between halos
			  pairs[c1].Rdis = halos[h1].Rclos;
			  //Relative velocity between halos
			  pairs[c1].Vrad = radial_vel( halos[h1].v, halos[h2].v,
						       halos[h1].r, halos[h2].r,
						       halos[h1].cond_comp[0],
						       halos[h1].cond_comp[1],
						       halos[h1].cond_comp[2],
						       p[LBOX]) + C_H0*pairs[c1].Rdis;
			  //Id of pair
			  pairs[c1].idpair = c1;
			  halos[h1].idpair = c1;
			  halos[h2].idpair = c1;
			  //-----------------------------------------------------------------------

			  //ISOLATED HALO PAIRS SAMPLES -------------------------------------------
			  //In case that M1>M2, the closest more massive halo to halo1 is Rpmas[0] and
			  //for halo2 is Rpmas[1] (The first is its companion!)
			  if( halos[h1].Mass > halos[h2].Mass ){
			      Rpmass1 = halos[h1].Rpmas[0];
			      Rpmass2 = halos[h2].Rpmas[1];}
			  //In case that M2>M1, the closest more massive halo to halo2 is Rpmas[0] and
			  //for halo1 is Rpmas[1] (The first is its companion!)
			  else{
			      Rpmass1 = halos[h1].Rpmas[1];
			      Rpmass2 = halos[h2].Rpmas[0];}
			      
			  //Conditions for closest halo with more mass that halo1 and halo2 respectively
			  if( Rpmass1 > p[RPMAS] &&
			      Rpmass2 > p[RPMAS] &&
			  //Condition for closest halo (with maximum mass limit) to halo1 and halo2 respectively
			      halos[h1].Rmmas > p[RMMAX] &&
			      halos[h2].Rmmas > p[RMMAX] &&
			  //Negative relative radial velocity
 			      pairs[c1].Vrad <= p[VMAX] &&
			  //Its relative distance is smaller that limit valor
 			      pairs[c1].Rdis <= p[RREL] ){
			    
			      //Mass of halo 1
			      isopair[c2].M1 = halos[h1].Mass;
			      //Id of halo 1
			      isopair[c2].id1 = halos[h1].id;
			      //Region of halo 1
			      isopair[c2].oct1 = halos[h1].oct;
			      
			      //Mass of halo 2
			      isopair[c2].M2 = halos[h2].Mass;
			      //Id of halo 2
			      isopair[c2].id2 = halos[h2].id;
			      //Region of halo 2
			      isopair[c2].oct2 = halos[h2].oct;
			      
			      //Distance between halos
			      isopair[c2].Rdis = pairs[c1].Rdis;
			      //Relative velocity between halos
			      isopair[c2].Vrad = pairs[c1].Vrad;
			      //Id of pair
			      isopair[c2].idpair = c1;
			      c2 += 1;
			  }
			  c1 += 1;
			  //-----------------------------------------------------------------------
		      }}}}

      //Number of General Halo Pairs
      p[PAIR]    = c1;
      //Number of Isolated Halo Pairs
      p[ISOPAIR] = c2;
      //Number of Halos in mass range
      p[HRMAS] 	 = c3;
      return 0;
}