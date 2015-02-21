import re

from modularMath import *

alphabetSize = 26

#convert a string to ascii:
def to_ascii(string):
	print "\""+ string + "\" in ASCII is: ",
	for char in string:
		print str(ord(char)) + " ",
	print
	
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