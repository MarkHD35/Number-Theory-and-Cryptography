#For Math 4351, Number Theory and Cryptography, at Washington University in St. Louis in Spring 2015
#This file is where I implemented algorithms 
#referred to in chapter 1 of "Mathematical Cryptography" by Silverman and Hoffstein
#Some of these were for use in HW 1, others just because

import re
import sys
import math

alphabetSize = 26

def shift(code, shift_factor):
	startingChar = 'a' #this is the start of the alphabet
	# and ASCII representations of alphabet characters are consecutive
	# so start here to only work with ASCII representations of alphabet characters
	
	code = code.lower() #for consistency
	shifted = "" #will represent the shifted code, when shifted letters are appended to it
	
	#for each letter in the code
	for letter in range(0, len(code)):
		#get ASCII value of the new shifted character
		new_ascii = (ord(code[letter]) + shift_factor - ord(startingChar))%alphabetSize + ord(startingChar) 
		
		#get letter corresponding to ASCII value of new shifted character...
		new_letter = unichr(new_ascii)
		shifted += str(new_letter) #...and append it to the string of shifted code
	return shifted

#This method decodes a Caesar cipher
#takes in a string and shifts each letter each possible number of letters to the right
def decode_caesar(code):
	#try each possible shift
	for alph_shift in range(1,alphabetSize):
		#visually inspect to see which makes sense
		#ideally try to devise an algorithm for splitting a sequence of characters into words
		#for the purposes of this problem that's probably more complicated than necessary,
		#since this is a small alphabet
		print shift(code,alph_shift),
		print(" (shift of %d right/%d left)" % (alph_shift, alphabetSize - alph_shift))
		
#For usage in decoding arbitrary substitution ciphers
#Takes in a string of code and allows for replacement of one letter with another
#That way, a human can decode manually
#Ideally, would have the computer decode using statistical analysis
#For the sake of the scope of this exercise, this was not done
def decode_substitution_manually(code, codeLetter, decodedLetter):
	#could make more efficient by stripping whitespace
	code = re.sub(codeLetter, decodedLetter, code)
	return code

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

#find all square roots of b mod whatever the modulus is
def sqrt_mod(modulus,b):
	sqrts = list()
	
	#check every number in the field of integers modulo the modulus
	for sqrt in range(0,modulus):
		if sqrt**2 % modulus == b % modulus:
			print ("%d^2 mod %d = %d mod %d = %d = %d mod %d" % \
			(sqrt,modulus,sqrt**2,modulus,sqrt**2 % modulus,b,modulus))
			sqrts.append(sqrt)
	if len(sqrts) == 0:
		print ("There are no square roots of %d modulo %d." % (b,modulus))
	else:
		print ("Square roots of %d modulo %d: " % (b,modulus)),
		print sqrts
	return sqrts

#convert a string to ascii:
def to_ascii(string):
	print "\""+ string + "\" in ASCII is: ",
	for char in string:
		print str(ord(char)) + " ",
	print

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
	
#compute the inverse modulo p
def inverse(number, p):
	#since by Fermat's Little Theorem, a^0 == 1 == a^(p-1) mod p
	#then a^-1 = a^(p-2) mod p
	return number**(p-2)

#affine encryption: combination of shift cipher and multiplication cipher	
def affine_encrypt(message, key1, key2, p):
	encoding = (key1*message + key2) % p
	return encoding

#affine decryption	
def affine_decrypt(ciphertext, key1, key2, p):
	key1Inv = inverse(key1, p)
	decoding = (key1Inv * (ciphertext - key2)) % p
	return decoding
	
#crack affine cipher given two ciphertexts and corresponding plaintexts
#p is public knowledge
def crack_affine(message1, message2, ciphertext1, ciphertext2, p):
	if message1 > message2:
		mtemp = message1
		message1 = message2
		message2 = mtemp
		ctemp = ciphertext1
		ciphertext1 = ciphertext2
		ciphertext2 = ctemp
		
	#derivations in written part of homework
	key1 = (ciphertext2 - ciphertext1)*inverse((message2 - message1),p)
	key1 = key1 % p
	key2 = (ciphertext1 - key1*message1) % p
	return key1, key2