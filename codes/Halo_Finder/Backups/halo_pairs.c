#include <allvars.h>

int main( int argc, char *argv[] )
{   
	//Individual halos
	struct halo *halos;
	halos = (struct halo *)calloc( MAXHALOS, sizeof( struct halo ) );
	//Halo pairs
	struct pair *pairs;
	pairs = (struct pair *)calloc( MAXPAIRS, sizeof( struct pair ) );
	//Isolated halo pairs
	struct pair *isopair;
	isopair = (struct pair *)calloc( MAXIPAIR, sizeof( struct pair ) );
	
	int i,j;
	
	int k, l;
	
	char filename[NMAX1];
	char filenameP[NMAX1];
	char cmd[NMAX1];
	float p[NMAX1];
	
	struct region regions[NMAX2][NMAX2][NMAX2];
	int index[NMAX1][3];
	
	FILE *script;
	
	
	printf( "\n\n************************ HALO PAIR FINDER ***********************\n" );
	//Load Configuration-----------------------------------------------------------------------
	read_parameters( p, "parameters.conf" );
	//Construction of octant regions (PYHTON CODE CALL) [Processed input data file] P<filename>
	  //Input Filename
	sprintf( filename, "%s", "halos.dat" );
  	sprintf( cmd, "python octant.py %d %s", (int)p[NAXE], filename );
     	system( cmd );
	printf( "  * Datafile of halos has been sorted in octant regions!\n" );
	
	//Load Processed input datafile------------------------------------------------------------
 	sprintf( filenameP, "P%s", filename );
	p[NDAT] = data_in( halos, filenameP, p[NAXE] );
	
	//Neighborhood Construction----------------------------------------------------------------
 	make_regions( regions, halos, p[NDAT], p[NAXE], p[LBOX], index );
	printf( "  * Neighborhood construction done!\n" );
 	for( i=0; i<pow(p[NAXE],3); i++ ){
 	    printf( "%d\t%d\t%d\t%d\t%d\n", regions[ index[i][0] ][ index[i][1] ][ index[i][2] ].id,regions[ index[i][0] ][ index[i][1] ][ index[i][2] ].Nhalos, index[i][0], index[i][1], index[i][2] );}
	
	//Halo Pair construction-------------------------------------------------------------------
 	pair_finder( halos, pairs, isopair, regions, index, p );
	printf( "  * Halo pairs have been found!\n" );
	printf( "  * %d Halos in Mass Range Found!\n", (int)p[HRMAS] );
	
	//Saving Halo Pairs General Sample --------------------------------------------------------
	data_pair_out( pairs, halos, "Pairs.dat", p[PAIR] );
	printf( "  * %d General Halo Pairs Found!\tData in 'Pairs.dat'\n", (int)p[PAIR] );
	
	//Saving Halo Pairs Isolated Sample --------------------------------------------------------
	data_pair_out( isopair, halos, "IsoPairs.dat", p[ISOPAIR] );
	printf( "  * %d Isolated Halo Pairs Found!\tData in 'IsoPairs.dat'\n", (int)p[ISOPAIR] );
	
    return 0;
}