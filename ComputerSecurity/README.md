# Computer Security

A collection of labs and lab reports created during Computer Security at the University of Manitoba

##  Lab 1 - Encryption and Decryption

### CBC vs ECB Encryption
Given the original image, I compared the security of CBC and ECB encryption.
![](img/orig_rsaImg.JPG)

Using the command line and the same key (123456789) to encrypt the image, I obtained the following encrypted images:

![](img/rsa_CBC_encrypt.JPG)
In the image encrypted with CBC, there are no clear patterns to see, only noise. 

![](img/rsa_ECB_encrypt.JPG)
In the image encrypted with ECB, there are clear patterns that show the shapes and similar colors to the original image. Typically, images are not suitable for ECB encryption because patterns are repeated with ECB encryption.

Compared to CBC, ECB encryption is less secure because clear patterns are visible.

### RSA
RSA encryption uses the following formula:
- `n = p*q`
- calculate `phin = (p-1)*(q-1)

## Lab 2 - Buffer Overflow Exploit & Address Randomization

## Lab 3 - Environment Variable Manipulation



## Lab 4 -  SQL Injection

## Lab 5 -  SYN-Flooding & SYN-Cookie Countermeasure
