#For Math 4351, Number Theory and Cryptography, at Washington University in St. Louis in Spring 2015
#This file is where I did my computer-assisted scratch work for HW 2
#For instructor verification if desired

from code_Math4351 import *

#1.32a
print "1.32a: "
if primitivity_test(2,7): print ("2 is a primitive root of %d" % 7)
if primitivity_test(2,13): print ("2 is a primitive root of %d" % 13)
if primitivity_test(2,19): print ("2 is a primitive root of %d" % 19)
if primitivity_test(2,23): print ("2 is a primitive root of %d" % 23)

#1.32c
print "1.32c: "
print ("%d is a primitive root of %d" %(find_primitive_roots(23)[0],23))
print ("%d is a primitive root of %d" %(find_primitive_roots(29)[0],29))
print ("%d is a primitive root of %d" %(find_primitive_roots(41)[0],41))
print ("%d is a primitive root of %d" %(find_primitive_roots(43)[0],43))

#for 1.34b
print "1.34b: "
sqrt_mod(7,2)
sqrt_mod(11,5)
sqrt_mod(11,7)
sqrt_mod(37,3)

#for 1.34c
print "1.34c: "
sqrt_mod(35,29)

#for 1.36
print "1.36: "
for p in range(3,100):
	if isPrime(p):
		print("2^((%d-1)/2) mod %d = %d mod %d = %d" % (p, p, 2**((p-1)/2), p, (2**((p-1)/2)) % p))
	
#for 1.40
print "1.40: "
to_ascii("Bad day, Dad.")

#for 1.41a
print "1.41a: "
print "Encryption of message 204: ", affine_encrypt(204, 34,71, 541)
print "Decryption of ciphertext 431: ", affine_decrypt(431, 34,71, 541)

#for 1.41c
print "1.41c: "
p = 601
key1, key2 = crack_affine(387,491,324,381,p)
print("The private key is (%d, %d)" % (key1, key2))

new_message = 173
print("Encrypting new message %d with the key we figured out: %d"\
 % ( new_message, affine_encrypt(new_message,key1, key2, p) ))
		
	