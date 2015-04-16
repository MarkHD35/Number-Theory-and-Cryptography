#find all square roots of b mod whatever the modulus is
def sqrt_mod(modulus,b):
	sqrts = list()
	
	#check every number in the field of integers modulo the modulus
	for sqrt in range(0,modulus):
		if sqrt**2 % modulus == b % modulus:
#			print ("%d^2 mod %d = %d mod %d = %d = %d mod %d" % \
#			(sqrt,modulus,sqrt**2,modulus,sqrt**2 % modulus,b,modulus))
			sqrts.append(sqrt)
#	if len(sqrts) == 0:
#		print ("There are no square roots of %d modulo %d." % (b,modulus))
#	else:
#		print ("Square roots of %d modulo %d: " % (b,modulus)),
#		print sqrts
	return sqrts
	
#compute the inverse modulo p
def inverse(number, p):
	#since by Fermat's Little Theorem, a^0 == 1 == a^(p-1) mod p
	#then a^-1 = a^(p-2) mod p
	return (number**(p-2)) % p