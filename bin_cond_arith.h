/************************************************************************
 *
 *	arithmetic_coding.h
 *
 ************************************************************************/


/* DECLARATIONS USED FOR ARITHMETIC ENCODING AND DEODING */

#include <stdio.h>

/* SIZE OF ARITHMETIC CODE VALUE */

#define Code_value_bits 16          /* Number of bits in a code value   */
typedef long code_value;            /* Type of an arithmetic code value */

#define Top_value (((long)1<<Code_value_bits)-1)  /* Largest code value */


/* HALF AND QUARTER POINTS IN THE CODE VALUE RANGE */

#define First_qtr (Top_value/4+1)   /* Point after first quarter        */
#define Half      (2*First_qtr)     /* Point after first half           */
#define Third_qtr (3*First_qtr)     /* Point after third quarter        */


/* INPUT AND OUTPUT FILE */

FILE *fin;                        /* Pointer of input file */
FILE *fout;                       /* Pointer of output file */

