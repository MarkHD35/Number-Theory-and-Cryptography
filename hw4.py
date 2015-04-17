from modularMath import *
from discreteLog import *
from primeMath import *

#note: will hopefully refactor this code soon (I claim the thesis-is-due defense...)

#takes in a number and factors it
def factor(value):
	return getFactorList(value, [])

#direct factoring into primes
def getFactorList(value, factor_list):
	for possFactor in range(2,value):
		if value % possFactor == 0:
			factor_list.append(possFactor)
			return getFactorList(value / possFactor,factor_list)
	factor_list.append(value)
	#should be sorted since factors are checked in order
	return groupFactors(factor_list)
	
#takes in a list of numbers (e.g. prime factors)
#specifies the exponents of each unique factor
#e.g. 2,2,2,3,5,5 becomes {2: 3, 3: 1, 5: 2}
def groupFactors(factorList):
	factorDict = dict()
	
	for element in factorList:
		#element is already in dictionary
		if element in factorDict:
			factorDict[element] += 1
		else: #add to dictionary
			factorDict[element] = 1
	return factorDict
	
def pi4(X,remainder):
	count = 0
	for number in range(2,X+1):
		if isPrime(number) and number % 4 == remainder:
			count += 1
	return count

#test for b-smoothness	
def bSmooth(number, smoothness):
	factors = factor(number)
	allFactors = factors.keys()
	largestFactor = allFactors[-1]
	return largestFactor <= smoothness
	
#test for b-power-smoothness
def bPowerSmooth(number,smoothness):
	factors = factor(number)
	allFactors = factors.keys()
	maxPower = 0
	for fac in allFactors:
		if fac**factors[fac] > maxPower:
			maxPower = fac**factors[fac]
	return maxPower <= smoothness

'''
factors = factor(12191)
print factors

print "The inverse of 37 modulo (p-1)(q-1) is ", inverse(37,72*166)
print "c^d % N = ", largePowerModulo(587,10153,12191)
print "\pi_1(10) = ", pi4(10,1)
print "\pi_3(10) = ", pi4(10,3)
print "\pi_1(25) = ", pi4(25,1)
print "\pi_3(25) = ", pi4(25,3)
print "\pi_1(100) = ", pi4(100,1)
print "\pi_3(100) = ", pi4(100,3)
print "\pi_1(10^6) = ", pi4(10**6,1)
print "\pi_3(10^6) = ", pi4(10**6,3)
print isPrime(39175)
'''
'''
#list of numbers for Exercise 3.27
numbers327 = [84,141,171,208,224,318,325,366,378,390,420,440,504,530,707,726,758,765,792,817]
smoothness = 10
for number in numbers327:
	print("%d is " % number),
	if bSmooth(number,smoothness):
		print "10-smooth; ",
	else:
		print "not 10-smooth; ",
	
	if bPowerSmooth(number,smoothness):
		print "10-power-smooth."
	else:
		print "not 10-power-smooth."
'''	