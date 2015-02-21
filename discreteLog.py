import math

from modularMath import *


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

#testing	
print discreteLog_bruteForce(2,6,10)
print shank(2,6,10)
print discreteLog_bruteForce(9704,13896,17389)
print shank(9704,13896,17389)