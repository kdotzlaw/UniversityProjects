#include <stdio.h>
//use BIGNUM library from lab questions
//now we can compute a^b 
#include <openssl/bn.h>

#define NBITS 128

//print
void printBN(char *msg, BIGNUM * a)
{
    /* Use BN_bn2hex(a) for hex string
    * Use BN_bn2dec(a) for decimal string */
   char * number_str = BN_bn2hex(a);
   printf("%s %s\n", msg, number_str);
   OPENSSL_free(number_str);
}

//Main
int main()
{
  //init BIGNUM
  BN_CTX *ctx = BN_CTX_new();
  BIGNUM *p = BN_new();
  BIGNUM *q = BN_new();
  BIGNUM *e = BN_new();
  BIGNUM *n = BN_new();
  BIGNUM *d = BN_new();
  BIGNUM *phin = BN_new();
  BIGNUM *pone = BN_new();
  BIGNUM *qone = BN_new();
  
  BN_hex2bn(&p,"F7E75FDC469067FFDC4E847C51F452DF");
  BN_hex2bn(&q,"E85CED54AF57E53E092113E62F436F4F");
  BN_hex2bn(&e,"0D88C3");
  BN_hex2bn(&pone,"F7E75FDC469067FFDC4E847C51F452DE");
  BN_hex2bn(&qone,"E85CED54AF57E53E092113E62F436F4E");
  //Task 1: Derive Private Key
  //n = p*q
	BN_mul(n,p,q,ctx);
	//calcualte phin -- phin = (p-1)*(q-1)
	BN_mul(phin,pone,qone,ctx);
	//private key d: unique st ed is identical to 1%phin
	//d is multiplicative modular inverse of e & phin so 
	BN_mod_inverse(d,e,phin,ctx);
	printBN("Private key=",d);
  
  //test
  BIGNUM *res = BN_new();
  BIGNUM *a = BN_new();
  BN_hex2bn(&a,"4120746f702073656372657421");
  BN_mod_exp(res,a,e,n,ctx);
  printBN("Encrypt=",res);
  
  BN_mod_exp(res,res,d,n,ctx);
  printBN("decrypt w d=",res);
  
  //Task 2: Encrypt Msg -- python to convert to hex
  BIGNUM *n2 = BN_new();
  BIGNUM *e2 = BN_new();
  BIGNUM *d2 = BN_new();
  BN_hex2bn(&n2,"DCBFFE3E51F62E09CE7032E2677A78946A849DC4CDDE3A4D0CB81629242FB1A5");
BN_hex2bn(&e2, "010001");
BN_hex2bn(&d2,"74D806F9F3A62BAE331FFE3F0A68AFE35B3D2E4794148AACBC26AA381CD7D30D");
  
  BIGNUM *msg = BN_new();
  BN_hex2bn(&msg,"4120746f702073656372657421");
  //encrypt
  BN_mod_exp(res,msg,e2,n2,ctx);
  printBN("Encrypted msg= ",res);
  //verify
BN_mod_exp(res,res,d2,n2,ctx);
  printBN("Decrypted msg=",res);
  
  //Task 3: Decrypt Msg
  BIGNUM *c = BN_new(); //cipher
  //use same n2,e2,d2 as task 2
 BN_hex2bn(&c,"8C0F971DF2F3672B28811407E2DABBE1DA0FEBBBDFC7DCB67396567EA1E2493F");
  BN_mod_exp(res,c,d2,n2,ctx);
  printBN("Decrypted msg=",res);
	return 0;
}
