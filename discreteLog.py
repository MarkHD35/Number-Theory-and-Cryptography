import math

from modularMath import *
from gcd import *


#TODO: find order of base within group, use that as "N" instead of modulus

#solves the discrete logarithm problem: 
#find x such that (base)^x = (value) mod (modulus)
#does so by brute force: checking evey number up to the modulus
def discreteLog_bruteForce(base,value,modulus):
	exponent = 0
	powerValue = 1
	while exponent < modulus:
		if powerValue % modulus == value:
			break #return exponent
		else:
			powerValue *= base
			exponent += 1
	return exponent
	
#Shank's algorithm for solving the discrete logarithm problem
#find x such that (base)^x = (value) mod (modulus)
def shank(base, value, modulus):
	n = int(1 + math.ceil(math.sqrt(modulus)) ) #n > sqrt(modulus)
	list1 = list()
	
	list1Base = 1
	for i in range(0,n+1):
		list1.append(list1Base%modulus)
		list1Base *= base
		
	list2Base = 1
	list2Change = inverse(base,modulus) ** n
	for j in range(0,n+1):
		list2elt = value * list2Base 
		list2elt = list2elt % modulus
		for i in range(0,len(list1)):
			if list1[i] == list2elt:
				return i + j*n #solution to discrete log problem
		list2Base *= list2Change
	return 0 #if failure
	
#Chinese Remainder Theorem
#takes in a dictionary of values and moduli and solves simultaneous congruence
#solve for x such that x = a mod modulus(a), x = b mod modulus(b), etc.
#where m, n are relatively prime
def chineseRemainder(congruences):
	#TODO: check if all moduli are relatively prime
	#TODO: check if there are at least two congruences
	
	pass
	
def crt(mod1, val1, mod2, val2):
	print mod1, val1, mod2, val2
	#wlog make val1 be bigger than val2
	if val1 < val2:
		return crt(mod2,val2,mod1,val1)
	else:
		#x = mod1 * y + val1
		#y * mod1 = (val1 - val2) % mod2
		y = (inverse(mod1, mod2) * (val1 - val2)) % mod2
		print inverse(mod1, mod2)
		print y
		return y*mod1 + val1

#returns base^exponent % modulus
#useful when base^exponent is such a large number that you'd have overflow error normally
def largePowerModulo(base, exponent, modulus):
	value = 1
	for i in range(0,exponent):
		value *= base
		value = value % modulus
	return value
	
#testing
if __name__ == "__main__":	
	print discreteLog_bruteForce(2,6,10)
	print shank(2,6,10)
	print discreteLog_bruteForce(9704,13896,17389)
	print shank(9704,13896,17389)

	testCongruences = dict()
	testCongruences[5] = 1
	testCongruences[11] = 9
	print testCongruences

	#5y + 1 = 9 mod 11
	#5y = 8 mod 11

	#print crt(5,1,11,9)
	print inverse(11,9)
	print inverse(27,7)

