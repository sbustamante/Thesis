#include <allvars.h>

/**************************************************************************************************
 NAME:	     conf2dump
 FUNCTION:   To convert a data file text in plain text 
 INPUTS:     name of configuration file
 RETURN:     0
**************************************************************************************************/
int conf2dump( char filename[] )
{
    char cmd[100];
    sprintf( cmd, "grep -v \"#\" %s | grep -v \"^$\" | gawk -F\"=\" '{print $2}' > %s.dump", 
	     filename, filename );
    system( cmd );

    return 0;
}


/**************************************************************************************************
 NAME:       in2dump
 FUNCTION:   To convert a data file text in plain text 
 INPUTS:     name of configuration file
 RETURN:     0
**************************************************************************************************/
int in2dump( char filename[] )
{
    char cmd[100];
    sprintf( cmd, "grep -v \"#\" %s > %s.dump", 
	     filename, filename );
    system( cmd );

    return 0;
}


/**************************************************************************************************
 NAME:       read_parameters
 FUNCTION:   read the file with given name and load information of array given
 INPUTS:     array where it returns reading data and file name 
	     with configuration file
 RETURN:     0 if file read ok
	     1 if file dont exist
**************************************************************************************************/
int read_parameters( float parameters[],
		     char filename[] )
{
    char cmd[100], filenamedump[100];
    int i=0;
    FILE *file;

    //Load of File
    file = fopen( filename, "r" );
    if( file==NULL ){
	printf( "  * The file '%s' don't exist!\n", filename );
	return 1;}
    fclose(file);
    
    //Converting to plain text
    conf2dump( filename );
    sprintf( filenamedump, "%s.dump", filename );
    file = fopen( filenamedump, "r" );
    
    //Reading
    while( getc( file ) != EOF ){
	fscanf( file, "%f", &parameters[i] );
	i++;}
    
    fclose( file );
    
    printf( "  * The file '%s' has been loaded!\n", filename );

    sprintf( cmd, "rm -rf %s.dump", filename );
    system( cmd );
    
    return 0;
}


/**************************************************************************************************
 NAME:       data_in
 FUNCTION:   read input file with masses, positions, velocities, id, ...
 INPUTS:     'halo' structure, input file name, and number of octant
 RETURN:     Number of data (rows)
**************************************************************************************************/
int data_in( struct halo halos[],
	     char filename[],
	     int Noct)
{
    int i=0, j=0, Ndats;
    char cmd[100], filenamedump[100];
    FILE *file;
    float tmp;
    

    //File Detection
    file = fopen( filename, "r" );
    if( file==NULL ){
	printf( "  * The file '%s' don't exist!\n", filename );}
    fclose(file);

    //Conversed to plain text
    in2dump( filename );
    sprintf( filenamedump, "%s.dump", filename );
    file = fopen( filenamedump, "r" );
    
    //Read data
    while( getc( file ) != EOF ){
	fscanf( file,"%d %f %f %f %f %f %f %f %f %f %f %f %f %f", 
		&halos[i].id_or, 
		&halos[i].r[X], &halos[i].r[Y], &halos[i].r[Z],
		&halos[i].v[X], &halos[i].v[Y], &halos[i].v[Z],
		&tmp, 	&halos[i].Mass, &tmp, &tmp, &tmp, &tmp, &tmp );
	halos[i].id = i;
	i++;}

    //Number of rows in datafile
    Ndats = i-1;
    j = 0;
    //Octant asignation for halo
    for( i=0; i<Ndats; i++ ){
	if( i == (int)( Ndats*(j+1)/pow(2,3*Noct) ) )
	  j += 1;
	halos[i].oct = j;
    }
	  
    fclose( file );

    printf( "  * The file '%s' has been loaded!\n", filename );
    
    sprintf( cmd, "rm -rf %s.dump", filename );
    system( cmd );

    return Ndats;
}

/**************************************************************************************************
 NAME:       data_pair_out
 FUNCTION:   write a file with masses, positions and velocities of
	     all particles
 INPUTS:     'pair' structure with halo pairs data, halos data, string with out file name, 
	     Number of pairs 
 RETURN:     0
**************************************************************************************************/
int data_pair_out( struct pair pairs[],
		   struct halo halos[],
		   char filename[],
		   int Npair)
{
    int i=0;
    int h1, h2;
    FILE *file;
    
    //GENERAL FILE
    file = fopen( filename, "w" );
    fprintf( file, "#HALO PAIR SAMPLES\t\tNumber of Pairs found: %d\n", Npair ); 
    fprintf( file, "#IdPair\tId1\tM1\t\tRg1\tId2\tM2\t\tRg2\tRdis\t\tVrad\t\tId11pm\tR11pm\tId12pm\tR12pm\tId1Mm\tR1Mm\tId1um\tR1um\t\tId21pm\tR21pm\tId22pm\tR22pm\tId2Mm\tR2Mm\tId2um\tR2um\t\ti\tj\tk\n" );
    //Writing
    for( i=0; i<Npair; i++ ){
	h1 = pairs[i].id1;
	h2 = pairs[i].id2;
	fprintf( file, "%d\t%d\t%1.4e\t%d\t%d\t%1.4e\t%d\t%4.3f\t\t%+4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t\t%d\t%d\t%d\n", 
		 pairs[i].idpair, 
		 halos[h1].id_or, pairs[i].M1, pairs[i].oct1,
		 halos[h2].id_or, pairs[i].M2, pairs[i].oct2,
		 pairs[i].Rdis, pairs[i].Vrad,
		 halos[h1].idpmas[0], halos[h1].Rpmas[0],
		 halos[h1].idpmas[1], halos[h1].Rpmas[1],
		 halos[h1].idmmas,    halos[h1].Rmmas,
		 halos[h1].idumas,    halos[h1].Rumas,
		 
		 halos[h2].idpmas[0], halos[h2].Rpmas[0],
		 halos[h2].idpmas[1], halos[h2].Rpmas[1],
		 halos[h2].idmmas,    halos[h2].Rmmas,
		 halos[h2].idumas,    halos[h2].Rumas,
		 halos[h1].cond_comp[0],
		 halos[h1].cond_comp[1],
		 halos[h1].cond_comp[2]);}

    return 0;
}