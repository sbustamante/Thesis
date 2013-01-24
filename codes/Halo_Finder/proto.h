// Data Module
int conf2dump( char * );
int in2dump( char * );
int read_parameters( float *, char * );
int data_in( struct halo *, char *, int );
int data_pair_out( struct pair *,struct halo *, char *, int );

//Finder Module
int make_regions( struct region regions[NMAX2][NMAX2][NMAX2], struct halo halos[], int Nhalos, int Naxe, float Lbox, int index[NMAX1][3] );
int pair_finder( struct halo halos[], struct pair pairs[], struct pair isopair[], 
		 struct region regions[NMAX2][NMAX2][NMAX2], int index[NMAX1][3], float p[NMAX1] );
float distance( float *, float *, int, int, int, float );
float radial_vel( float *, float *, float *, float *, int, int, int, float );