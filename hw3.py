from discreteLog import *
from modularMath import *
from gcd import *

#modulus for problems 2.6 and 2.8
p = 1373

#2.6
bobsValue = largePowerModulo(2,871,p)
print "Bob's value: ", bobsValue

sharedValue = largePowerModulo(974,871,p)
print "Shared secret value: ", sharedValue

alicesExponent = shank(2,974,p)
print "Alice's secret exponent: ", alicesExponent

#2.8a
alicesPublicKey = largePowerModulo(2,947,p)
print "Alice's public key is ", alicesPublicKey

#b
c1 = largePowerModulo(2,877,p)
c2 = (583*largePowerModulo(177,877,p)) % p
print("Alice sends the ciphertext (%d,%d)" %(c1,c2))

#c
c1a = largePowerModulo(661,299,p)
c1aInv = inverse(c1a,p)
m = c1aInv*1325 % p
print "Bob's message, decrypted, is ", m

#d
bobsPrivateKey = discreteLog_bruteForce(2,893,p)
print "Bob's private key is ",bobsPrivateKey
c1aAlice = largePowerModulo(693,219,p)
c1aInvAlice = inverse(c1aAlice,p)
mAlice = c1aInvAlice*793 % p
print "Alice's message, decrypted by Eve, is ", mAlice



#2.17a
print("The discrete log base 11 of 21 is %d mod 71." % shank(11,21,71) )

#2.18c
print "GCD of moduli: ", euclidean_gcd(451,697)
invVal = inverse(451,697)
print("The inverse of 451 is %d mod 697" % invVal)
b = (invVal*104)%697
print("b = %d" % b)
solution = 451*b + 133
print("An alleged solution to the congruence is %d" % solution)
print ("Testing the solution: ")
print (solution % 451) == 133
print (solution % 697) == 237