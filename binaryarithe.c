#include <stdio.h>
#include "model.h"
#include "arith.h"


main(argc, argv)
    int argc;
    char *argv[];
{
    int i,j;
    int ch; int symbol;
    if (argc < 3) {
         printf("Usage: encode in_file out_file \n");
         exit(-1);
    }
    if ((fin = fopen(argv[1], "rb")) == NULL) {   /* Open input file  */
         printf("Can't find file <%s>\n", argv[1]);
         exit(-1);
    }
    if ((fout = fopen(argv[2], "wb")) == NULL) {   /* Open input file  */
         printf("Can't find file <%s>\n", argv[2]);
         exit(-1);
    }

    start_model();
    start_outputing_bits();
    start_encoding();

    for(;;) {
        ch = getc(fin);
        if(ch==EOF) break;
        symbol = char_to_index[ch]; 
        encode_symbol(symbol,cum_freq);
        update_model(symbol); 
    }
    encode_symbol(EOF_symbol, cum_freq);     
    done_encoding();            /* Send the last few bits.  */
    done_outputing_bits();
    fclose(fin);
    fclose(fout);
    exit(0);
}

/* INITIALIZE THE MODEL */

start_model()
{
    int i;
    for (i = 0; i < No_of_chars; i++) {   /* Set up tables that         */
        char_to_index[i] = i+1;           /* translate between symbol   */
        index_to_char[i+1] = i;           /* indices and characters.    */
    }
   for (i =0; i<= No_of_symbols; i++) {
       freq[i]=1; 
       cum_freq[i]=No_of_symbols-i;
    }
    freq[0]=0;
}            

/* UPDATE THE MODEL TO ACCOUNT FOR A M|NEW SYMBOL. */

update_model(symbol)
int symbol;            /* Index of new symbol        */
{
int i,cum,ch_i,ch_symbol;
   if (cum_freq[0] > Max_frequency)
      {
      cum=0;

      for(i=No_of_symbols;i>=0;i--)
         {
         freq[i]=(freq[i]+1)/2;
         cum_freq[i]=cum;
         cum+=freq[i];
         }
      }
      for(i=symbol; freq[i]==freq[i-1];i--);
      if(i<symbol)
        {
        ch_i=index_to_char[i];
        ch_symbol=index_to_char[symbol];
        index_to_char[i]=ch_symbol;
        index_to_char[symbol]=ch_i;
        char_to_index[ch_i]=symbol;
        char_to_index[ch_symbol]=i;
        }
      freq[i]++;
      while(i>0)
         {
         i--;
         cum_freq[i]++;
         }
}



/* INITIALIZE FOR BIT OUTPUT. */

start_outputing_bits()
{
    buffer = 0;                           /* Buffer is empty to start   */
    bits_to_go = 8;                       /* with.                      */
}


/*  OUTPUT A BIT */

int output_bit(bit)
    int bit;
{
    buffer >>= 1;                         /* Put bit in top of buffer   */
    if (bit) buffer |= 0x80;
    bits_to_go -= 1;
    if (bits_to_go == 0) {                /* Output buffer if it is     */
       putc(buffer, fout);              /* now full.                  */
       bits_to_go = 8;
    }
}


/* FLUSH OUT THE LAST BITS. */

done_outputing_bits()
{
    putc(buffer>>bits_to_go, fout);
}





/* START ENCODING A STREAM OF SYMBOLS. */

start_encoding()
{
   low = 0;                     /* Full code range.                 */
   high = Top_value;
   bits_to_follow = 0;              /* No bits to follow next.          */
}


/* ENCODE A SYMBOL. */


encode_symbol(symbol,cum_freq)
    int symbol ;                    /* Symbol to encode                 */
    int cum_freq[];                 /* Cumulative symbol frequencies    */
{
    long range;                     /* Size of the current code region  */
    range = (long)(high-low)+1;
    high = low +                    /* narrow the code region */
      (range*cum_freq[symbol-1])/cum_freq[0]-1;/* to that allocted to  */
    low = low +                                 /* this symbol.         */
      (range*cum_freq[symbol])/cum_freq[0];
    for (; ;) {                     /* Loop to output bits.             */
        if (high < Half) {
           bit_plus_follow(0);      /* Output 0 if in low half.         */
        }
        else if (low >= Half) {     /* Output 1 if in high half.        */
           bit_plus_follow(1);
           low -= Half;
           high -= Half;            /* Subtract offset to top.          */
        }
        else if (low >= First_qtr   /* Output an opposite bit           */
            && high < Third_qtr) {  /* later if in middle half.         */
           bits_to_follow += 1;
           low -= First_qtr;        /* Subtract offset to middle.       */
           high -= First_qtr;
        }
        else break;                 /* Otherwise exit loop.             */
        low = 2*low;
        high = 2*high+1;            /* Scale up code range.             */
    }
}


/* FINISH ENCODING THE STREAM */

done_encoding()
{
    bits_to_follow += 1;                      /* Out two bits that       */
    if (low < First_qtr) bit_plus_follow(0);
    else bit_plus_follow(1);                 /* the current code range  */
}                                            /* contains.               */


/* OUTPUT BITS PLUS FOLLOWING OPPOSITE BITS */

bit_plus_follow(bit)
    int bit;
{
    output_bit(bit);                /* Output the bit.                  */
    while (bits_to_follow > 0) {
        output_bit(!bit);               /* Output bits_to_follow            */
        bits_to_follow -= 1;        /* opposite bits. Set               */
    }                               /* bits_to_follow to zero.          */
}
