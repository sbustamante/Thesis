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
	float p[NMAX1];
	
	struct region regions[NMAX2][NMAX2][NMAX2];
	int index[NMAX1][3];
	
	FILE *script;
	
	
	printf( "\n\n************************ HALO PAIR FINDER ***********************\n" );
	//Load Configuration-----------------------------------------------------------------------
	read_parameters( p, "parameters.conf" );
	
	//Load Processed input datafile------------------------------------------------------------
	  //Input Filename
// 	sprintf( filename, "%s", "../Data/CLUES/16953/halos_catalog.dat" );
	sprintf( filename, "%s", "./Halos_catalog.dat" );
	p[NDAT] = data_in( halos, filename, p[NAXE] );

	//Neighborhood Construction----------------------------------------------------------------
 	make_regions( regions, halos, p[NDAT], p[NAXE], p[LBOX], index );
	printf( "  * Datafile of halos has been sorted in octant regions!\n" );
	printf( "  * Neighborhood construction done!\n" );
	
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