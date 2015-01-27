#For Math 4351, Number Theory and Cryptography, at Washington University in St. Louis in Spring 2015
#This file is where I implemented algorithms 
#referred to in chapter 1 of "Mathematical Cryptography" by Silverman and Hoffstein
#Some of these were for use in HW 1, others just because

import re
import sys

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
	divisor,b = format_input(divisor,dividend)
	
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
	divisor,b = format_input(divisor,dividend)
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
def format_input(a,b):
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