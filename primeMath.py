import math

#simple primality test		
def isPrime(num):
	if num <= 3:
		return num >= 2 #the only prime numbers less than or equal to 3 are 2 and 3
	#only need to check up to (but including) the square root of the number
	#after that, the divisors just reverse order (e.g. 2*5 = 5*2)
	for possFactor in range(2,int(math.floor(num**0.5)) + 1 ):
		if num % possFactor == 0:
			return False
	return True