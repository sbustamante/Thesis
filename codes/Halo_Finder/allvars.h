/**************************************************************************************************
			      MACROS
**************************************************************************************************/
//General Macros
#define MAXHALOS	500000
#define MAXPAIRS	50000
#define MAXIPAIR	5000
#define HALOSPR		2000

#define NMAX1		1000
#define NMAX2		10

//Macros for Parameters
#define NAXE		0
#define LBOX		1
#define MMIN		2
#define MMAX		3
#define RREL		4
#define VMAX		5
#define RPMAS		6
#define MMMAX		7
#define RMMAX		8

#define NDAT		9
#define PAIR		10
#define ISOPAIR		11
#define HRMAS		12

//Other parameters
#define X		0
#define Y		1
#define Z		2

//Constants
#define C_H0		100

/**************************************************************************************************
			      ESTRUCTURAS
**************************************************************************************************/
struct halo{
    //Positions
    float r[3];
    //Velocities
    float v[3];
    //Mass
    float Mass;
    //Id
    int id;
    //Id of original file
    int id_or;

    //Region (sub-octant)
    int oct;
    //Id of closest halo in restringed range mass;
    int idclos;
    //Distance to closest halo in restringed range mass;
    float Rclos;
    //Conditions of region of companion halo (periodic boundary conditions);
    int cond_comp[3];
    
    //Id of two closest halo with more mass that current halo;
    int idpmas[2];
    //Distance to two closest halo with more mass that current halo;
    float Rpmas[2];
    
    //Id of closest halo with maximim mass limit;
    int idmmas;
    //Distance to closest halo with maximim mass limit;
    float Rmmas;
    
    //Id of closest halo with upper mass limit;
    int idumas;
    //Distance to closest halo with upper mass limit;
    float Rumas;
    
    //Id of asociated pair
    signed int idpair;
    };
    
struct pair{
    //Mass of halo 1
    float M1;
    //id of halo 1
    int id1;
    //Region of halo 1 (sub-octant)
    int oct1;
    
    //Mass of halo 2
    float M2;
    //id of halo 2
    int id2;
    //Region of halo 2 (sub-octant)
    int oct2;
    
    //Relative distances
    float Rdis;
    //Radial relative velocities
    float Vrad;
    //Pair id
    int idpair;
    };
    
struct region{
    //lower right corner position(xy)
    float Rcor[3];
    //Neighbors
    int neigh[27];
    int cond_neigh[27][3];
    //number Neighbors
    int Nneigh;
    //Number of pairs in region
    int Npair;
    //ide of region
    int id;
    
    //Number of halos in region
    int Nhalos;
    //Halos in region;
    int HalosId[HALOSPR];
    };
    
/**************************************************************************************************
			      HEADERS
**************************************************************************************************/
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#include <proto.h>