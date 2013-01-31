#include <stdio.h>
#include <stdlib.h>
#define FLOAT float

int main(int argc, char **argv)
{    
    FILE *in, *out_env, *out_vol;
    FLOAT *eigen1, *eigen2, *eigen3;
    int *environment;
    char filename[100];
    
    FLOAT Lambda_min, Lambda_max, Lambda;
    int j, k, N_thr, eig, i_c;
    
    int volume[4];
    
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
    N_thr = 20;     
    //Minim Lambda_th
    Lambda_min = 0.0;
    //Maxim Lambda_th
    Lambda_max = 1.0;
    //=============================================================================================
        
        
    //LOADING OF EIGENVALUES=======================================================================
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
	    if(!(eigen1=malloc(n_nodes * sizeof(FLOAT)))){
		fprintf(stderr, "problem with array allocation\n");
		exit(1);}
	    fread(&dumb,sizeof(int),1,in);
	    fread(&(eigen1[0]),sizeof(FLOAT), n_total, in);
	    fread(&dumb,sizeof(int),1,in);}
	//Second Eigenvalue
	if(eig == 1){
	    if(!(eigen2=malloc(n_nodes * sizeof(FLOAT)))){
		fprintf(stderr, "problem with array allocation\n");
		exit(1);}
	    fread(&dumb,sizeof(int),1,in);
	    fread(&(eigen2[0]),sizeof(FLOAT), n_total, in);
	    fread(&dumb,sizeof(int),1,in);}
	//Third Eigenvalue
	if(eig == 2){
	    if(!(eigen3=malloc(n_nodes * sizeof(FLOAT)))){
		fprintf(stderr, "problem with array allocation\n");
		exit(1);}
	    fread(&dumb,sizeof(int),1,in);
	    fread(&(eigen3[0]),sizeof(FLOAT), n_total, in);
	    fread(&dumb,sizeof(int),1,in);}
	fclose(in);}

	    
    //LAMBDA THRESHOLD VALUES (ENVIRONMENT)========================================================
    //To alloc memory for environment array
    if(!(environment=malloc(n_nodes * sizeof(int)))){
	fprintf(stderr, "problem with array allocation\n");
	exit(1);}
	
    //Volumen File
    sprintf(filename, "Volume.dat");
    out_vol=fopen(filename, "w");
	
    //Calculating the environment matrix for each Lambda_th Value
    for( j=0; j<=N_thr; j++ ){
	//Current Lambda
	Lambda = Lambda_min + (Lambda_max - Lambda_min)*j/N_thr;
	
	//New file for current Lambda value
	sprintf(filename, "enviroment_Lamb_%1.2f.dat", Lambda);
	out_env=fopen(filename, "w");
	volume[0] = 0; volume[1] = 0; volume[2] = 0; volume[3] = 0;
	
	for( i_c=0; i_c<n_total; i_c++ ){
	    environment[i_c] = 0;
	    if( eigen1[i_c] >= Lambda )
		environment[i_c] += 1;
	    if( eigen2[i_c] >= Lambda )
		environment[i_c] += 1;
	    if( eigen3[i_c] >= Lambda )
		environment[i_c] += 1;
	    fprintf( out_env, "%d\n", environment[i_c] );

	    //Volumen Control
	    for( k=0; k<4; k++)
		if( environment[i_c] == k )
		    volume[k] += 1;}
    	fclose(out_env);

	//Saving volumen fraction of each environment
	fprintf( out_vol, "%f\t", Lambda );
	for( k=0; k<4; k++)
	    fprintf( out_vol, "%d\t", volume[k] );
	fprintf( out_vol, "%d\n", volume[0]+volume[1]+volume[2]+volume[3]);
    }
    fclose(out_vol);
    //=============================================================================================
    return 0;
}