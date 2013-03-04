#include <stdio.h>
#include <stdlib.h>
#define FLOAT1 float
#define FLOAT2 double
#define NMAX 1000

//USAGE  Lambda_Correlation.out <EIG_Filename> <DELTA_Filename> <Min_Lambda> <Max_Lambda> <N_Lambda> <Out_Filename> <N_div>

int main(int argc, char **argv)
{    
    FILE *in, *out_corr;
    FLOAT1 *eigen1, *eigen2, *eigen3;
    FLOAT2 *delta;
    int *environment;
    char filename[100];
    float Ndiv[NMAX], Ncon[NMAX], Nsub[NMAX], Nover[NMAX];
    
    FLOAT1 Lambda_min, Lambda_max, Lambda;
    int octx, octy, octz, oct_id, j, N_thr, eig, ii, jj, kk, Noct = atoi(argv[7]);
    float corr[NMAX][4];
    
    //Grid variables===============================================================================
    int dumb;
    char line[30];
    long long i;
    int n_x, n_y, n_z;
    int n_nodes;
    long long n_total;
    float dx, dy, dz, x_0, y_0, z_0;
    //=============================================================================================
    
   
    //PARAMETERS===================================================================================
    //Number of divisions in Lambda_th array
    N_thr = atoi( argv[5] );     
    //Minim Lambda_th
    Lambda_min = atof( argv[3] );
    //Maxim Lambda_th
    Lambda_max = atof( argv[4] );
    //=============================================================================================
        
        
    //LOADING EIGENVALUES==========================================================================
    for( eig=0; eig<3; eig++ ){
        //filename of current eigenvalue
 	sprintf(filename, "%s_%d", argv[1], eig + 1);
	if(!(in=fopen(filename, "r"))){
	    fprintf(stderr, "Problem opening file %s\n", filename);
	    exit(1);}
	fread(&dumb,sizeof(int),1,in);
	fread(line,sizeof(char)*30,1,in);
	fread(&dumb,sizeof(int),1,in);
	fread(&dumb,sizeof(int),1,in);
	fread(&n_x,sizeof(int),1,in);    
	fread(&n_y,sizeof(int),1,in);    
	fread(&n_z,sizeof(int),1,in);    
	fread(&n_nodes,sizeof(int),1,in);    
	fread(&x_0,sizeof(float),1,in);    
	fread(&y_0,sizeof(float),1,in);    
	fread(&z_0,sizeof(float),1,in);    
	fread(&dx,sizeof(float),1,in);    
	fread(&dy,sizeof(float),1,in);    
	fread(&dz,sizeof(float),1,in);    
	fread(&dumb,sizeof(int),1,in);
	n_total = n_x * n_y * n_z;
	fprintf(stderr, "Nx Ny Nz : %d %d %d %lld\n", n_x, n_y, n_z, n_total);
	fprintf(stderr, "x_0 y_0 z_0 : %g %g %g\n", x_0, y_0, z_0);
	fprintf(stderr, "dx dy dz : %g %g %g\n", dx, dy, dz);    
	
	//First Eigenvalue
	if(eig == 0){
	    if(!(eigen1=malloc(n_nodes * sizeof(FLOAT1)))){
		fprintf(stderr, "problem with array allocation\n");
		exit(1);}
	    fread(&dumb,sizeof(int),1,in);
	    fread(&(eigen1[0]),sizeof(FLOAT1), n_total, in);
	    fread(&dumb,sizeof(int),1,in);}
	//Second Eigenvalue
	if(eig == 1){
	    if(!(eigen2=malloc(n_nodes * sizeof(FLOAT1)))){
		fprintf(stderr, "problem with array allocation\n");
		exit(1);}
	    fread(&dumb,sizeof(int),1,in);
	    fread(&(eigen2[0]),sizeof(FLOAT1), n_total, in);
	    fread(&dumb,sizeof(int),1,in);}
	//Third Eigenvalue
	if(eig == 2){
	    if(!(eigen3=malloc(n_nodes * sizeof(FLOAT1)))){
		fprintf(stderr, "problem with array allocation\n");
		exit(1);}
	    fread(&dumb,sizeof(int),1,in);
	    fread(&(eigen3[0]),sizeof(FLOAT1), n_total, in);
	    fread(&dumb,sizeof(int),1,in);}
	fclose(in);}
	
    //LOADING DENSITY FIELD========================================================================
    sprintf(filename, "%s", argv[2]);
    if(!(in=fopen(filename, "r"))){
	fprintf(stderr, "Problem opening file %s\n", filename);
	exit(1);}
    fread(&dumb,sizeof(int),1,in);
    fread(line,sizeof(char)*30,1,in);
    fread(&dumb,sizeof(int),1,in);
    fread(&dumb,sizeof(int),1,in);
    fread(&n_x,sizeof(int),1,in);    
    fread(&n_y,sizeof(int),1,in);    
    fread(&n_z,sizeof(int),1,in);    
    fread(&n_nodes,sizeof(int),1,in);    
    fread(&x_0,sizeof(float),1,in);    
    fread(&y_0,sizeof(float),1,in);    
    fread(&z_0,sizeof(float),1,in);    
    fread(&dx,sizeof(float),1,in);    
    fread(&dy,sizeof(float),1,in);    
    fread(&dz,sizeof(float),1,in);    
    fread(&dumb,sizeof(int),1,in);
    n_total = n_x * n_y * n_z;
    fprintf(stderr, "Nx Ny Nz : %d %d %d %lld\n", n_x, n_y, n_z, n_total);
    fprintf(stderr, "x_0 y_0 z_0 : %g %g %g\n", x_0, y_0, z_0);
    fprintf(stderr, "dx dy dz : %g %g %g\n", dx, dy, dz);    
    
    if(!(delta=malloc(n_nodes * sizeof(FLOAT2)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
    fread(&dumb,sizeof(int),1,in);
    fread(&(delta[0]),sizeof(FLOAT2), n_total, in);
    fread(&dumb,sizeof(int),1,in);
    
    fclose(in);

    //CORRELATIONS=================================================================================
    
    //Divisions
    oct_id = 0;
    for( octx=0; octx<Noct; octx++ )
	for( octy=0; octy<Noct; octy++ )
	    for( octz=0; octz<Noct; octz++ ){
    
		//Correlation File
		sprintf(filename, "%s_%02d.dat", argv[6],oct_id);
		out_corr=fopen(filename, "w");

		//Initializing histograms
		for( j=0; j<N_thr; j++ )
		    for( i=0; i<4; i++ )
			corr[j][i] = 0;
		
		for( j=0; j<N_thr; j++ ){
		    Ncon[j] = 0;	Ndiv[j] = 0;
		    Nsub[j] = 0;	Nover[j] = 0;

		    for( ii=(int)(n_x*octx/Noct); ii<(int)(n_x*(octx+1)/Noct); ii++ )
		    for( jj=(int)(n_y*octy/Noct); jj<(int)(n_y*(octy+1)/Noct); jj++ )
		    for( kk=(int)(n_z*octz/Noct); kk<(int)(n_z*(octz+1)/Noct); kk++ ){
			i = ii + n_x * (jj + n_y * kk );

			//Current Lambda
			Lambda = Lambda_min + (Lambda_max - Lambda_min)*j/N_thr;
			
			//Convergent and Divergent regions
			if( eigen1[i] + eigen2[i] + eigen3[i] - 3*Lambda < 0 )
			    Ndiv[j] ++;
			else
			    Ncon[j] ++;
			
			//Sub and Over density 
			if( delta[i]<=0 )
			    Nsub[j] ++;
			else
			    Nover[j] ++;		

			
			//Histogram
			if( delta[i]<=0 && eigen1[i] + eigen2[i] + eigen3[i] - 3*Lambda < 0 )
			    corr[j][0] ++;
			if( delta[i]<=0 && eigen1[i] + eigen2[i] + eigen3[i] - 3*Lambda > 0 )
			    corr[j][1] ++;
			if( delta[i]>0 && eigen1[i] + eigen2[i] + eigen3[i] - 3*Lambda > 0 )
			    corr[j][2] ++;
			if( delta[i]>0 && eigen1[i] + eigen2[i] + eigen3[i] - 3*Lambda < 0 )
			    corr[j][3] ++;
		    }}
		    
		//File Head
		fprintf( out_corr, "#Lamb  rg1  rg2  rg3  rg4  Ntot  Nsub  Nover  Ndiv  Ncon\n");
		for( j=0; j<N_thr; j++ ){
		    //Current Lambda
		    Lambda = Lambda_min + (Lambda_max - Lambda_min)*j/N_thr;
		    
		    fprintf( out_corr, "%1.2f  %1.3f %1.3f %1.3f %1.3f %8f  %8f %8f %8f %8f\n", Lambda, \
		    corr[j][0], corr[j][1], corr[j][2], corr[j][3],
		    corr[j][0] + corr[j][1] + corr[j][2] + corr[j][3],
		    Nsub[j], Nover[j], Ndiv[j], Ncon[j]);}
		    
		fclose(out_corr);
		oct_id ++;}
    
    //=============================================================================================
    return 0;
}
