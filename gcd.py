#Implementation of the Euclidean algorithm for computing the gcd of two positive integers a,b
def euclidean_gcd(divisor,dividend):
	#make sure input is valid and in a form we want it
	divisor,b = formatInput_Euclidean(divisor,dividend)
	
	#base case: dividend divides divisor
	if dividend % divisor == 0:
		return divisor
	else:
		#recursively replace the larger number with its remainder modulo the smaller number
		#get remainder by taking advantage of the fact that integer division is a floor in Python
		return euclidean_gcd(dividend - (dividend/divisor)*divisor,divisor)

#Implementation of extended Euclidean algorithm for finding u,v such that ua + vb = gcd(a,b)
def extended_Euclidean(divisor,dividend):
	#make sure input is valid and in a form we want it
	divisor,b = formatInput_Euclidean(divisor,dividend)
	return extended_Euclidean_rec(1,divisor,0,dividend,divisor,dividend)

#Solves not only for the gcd of two positive integers a and b
# but also for u,v such that au+bv = gcd(a,b)
#From "Mathematical Cryptography"" by Silverman and Hoffstein
def extended_Euclidean_rec(u,g,x,y,a,b):
	if y == 0:
		v = (g - a*u)/b
		print ("%d*%d + %d*%d = %d" % (a,u,b,v,a*u + v*b))
		return (g,u,v)
	else:
		q = g/y #divisor of g
		t = g - q*y #remainder
		s = u - q*x
		u = x
		g = y
		x = s
		y = t
		return extended_Euclidean_rec(u,g,x,y,a,b)

#Formats input for Euclidean and extended Euclidean algorithms
def formatInput_Euclidean(a,b):
	#check for bad input
	if a <= 0 or b <= 0:
		raise ValueError("Both numbers must be positive")
	if type(a) != int or type(b) != int:
		raise TypeError("Both numbers must be integers")
	
	#for consistency and without loss of generality, make a the smaller number
	if a > b: 
		temp = a
		a = b
		b = temp
		
	return a,b