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
         printf("Usage:  decode decoded_file encoded_file \n");
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

    start_model();            /* Set up other modules     */
    start_inputing_bits();
    start_decoding();

    for(;;)  {
        symbol = decode_symbol(cum_freq);  
        if (symbol==EOF_symbol) break;      /* Exit loop if EOF symbol  */
        ch = index_to_char[symbol];  /* Translate to a char.     */
        putc(ch,fout);                    /* White that character.    */
        update_model(symbol);
    }
    fclose(fin);
    fclose(fout);
    exit(0);
}


start_inputing_bits()
{
    bits_to_go = 0;                       /* Buffer starts out with     */
    garbage_bits = 0;                     /* no bits in it.             */
}


/*  INPUT A BIT */

input_bit()
{
    int t;
    if (bits_to_go == 0) {                /* Read the next byte if no  */
        buffer = getc(fin);             /* bits are left in buffer.  */
            if (buffer == EOF) {
               garbage_bits += 1;
               if(garbage_bits>Code_value_bits-2) {
                  printf("Bad input file\n");
                  exit(-1);
               }
            }
    bits_to_go = 8;
    }
    t = buffer&1;                        /* Return the next bit from  */
    buffer >>= 1;                        /* the bottom of the byte.   */
    bits_to_go -= 1;
    return t;
}

start_decoding()
{
    int i;
    value = 0;                            /* Input bits to fill the     */
    for (i = 1; i<=Code_value_bits; i++) {/* code value.                */
        value = 2*value+input_bit();
    }
   low = 0;                     /* Full code range.                 */
   high = Top_value;
}


/* DECODE THE NEXT SYMBOL. */

decode_symbol(cum_freq)
    int cum_freq[];               /* Cumulative symbol frequencies     */
{
    long range;                   /* Size of current code region       */
    int cum;                      /* Cumulative frequency calculated   */
    int symbol;                   /* Symbol decoded                    */
    range = (long)(high-low)+1;
    cum =                         /* Find cum freq for value           */
      (((long)(value-low)+1)*cum_freq[0]-1)/range;
    for (symbol = 1; cum_freq[symbol]>cum; symbol++);/* Then find symbol. */
    high = low +                  /* narrow the code region            */
      (range*cum_freq[symbol-1])/cum_freq[0]-1;  /* to that allocated  */
    low = low +                                  /* to this symbol.    */
      (range*cum_freq[symbol])/cum_freq[0];
    for (; ;) {                   /* Loop to get rid of bits.          */
        if (high< Half) {
            /* nothing */         /* Expand low half                   */
        }
        else if (low>=Half) {     /* Expand high half                  */
           value -= Half;
           low -= Half;           /* Subtract offset to top.           */
           high -= Half;
        }
        else if (low>=First_qtr   /* Expand middle half                */
             && high<Third_qtr) {
           value -= First_qtr;
           low -= First_qtr;      /* Subtract offset to middle         */
           high -= First_qtr;
        }
        else break;               /* Otherwise exit loop.              */
        low = 2*low;
        high = 2*high+1;          /* Scale up code range.              */
        value = 2*value+input_bit();   /* Move in next input bit.      */
    }
    return symbol;
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
}                                         /* same as freq[1].           */

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

