#see if testRoot is a primitive root of b
#see if testRoot^k = any nonnegative integer less than b for some k
def primitivity_test(testRoot,modulus):
	if testRoot > modulus: 
		temp = testRoot
		testRoot = modulus
		modulus = temp
	if modulus <= 1:
		raise ValueError("You must take roots of an integer greater than 1")
	if type(testRoot) != int or type(modulus) != int:
		raise TypeError("You must pass in integers")
		
	roots = list() #hold roots
	#note: since a^(b-1) = 1 = a^0 mod b by Fermat's Little Theorem, only need to check through 1 to b - 1
	#note: no repeats since there are the same number of integers modulo b and numbers between 1 and b-1
	#where b is the modulus
	for i in range(1,modulus):
		roots.append(testRoot**i % modulus)
	roots = sorted(roots)
	return roots == [i for i in range(1,modulus)]
	
#finds all primitive roots of an integer modulus
#basically performs a primitivity test for every number less than the inputted integer
def find_primitive_roots(modulus):
	roots = []
	if modulus <= 1:
		raise ValueError("You must pass in an integer greater than 1")
	if type(modulus) != int:
		raise TypeError("You must pass in an integer")
	for i in range(2,modulus):
		if primitivity_test(i,modulus):
			roots.append(i)
	return roots