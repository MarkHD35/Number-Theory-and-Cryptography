#For Math 4351, Number Theory and Cryptography, at Washington University in St. Louis in Spring 2015
#This file is where I did my computer-assisted scratch work for HW 1
#For instructor verification if desired

from code_Math4351 import *

#problem 1.2a
code1 = "LWKLQNWKDWLVKDOOQHYHUVHHDELOOERDUGORYHOBDVDWUHH"

#problem 1.4a
code2 = "JNRZR BNIGI BJRGZ IZLQR OTDNJ GRIHT USDKR ZZWLG OIBTM NRGJN IJTZJ LZISJ NRSBL QVRSI ORIQT QDEKJ JNRQW GLOFN IJTZX QLFQLWBIMJ ITQXT HHTBL KUHQL JZKMM LZRNT OBIMI EURLW BLQZJ GKBJTQDIQS LWJNR OLGRI EZJGK ZRBGS MJLDG IMNZT OIHRK MOSOT QHIJLQBRJN IJJNT ZFIZL WIZTO MURZM RBTRZ ZKBNN LFRVR GIZFL KUHIMMRIGJ LJNRB GKHRT QJRUU RBJLW JNRZI TULGI EZLUK JRUST QZLUKEURFT JNLKJ JNRXR S"

print "Exercise 1.2a: "
decode_caesar(code1)
print

#shows the order in which I tried to solve the problem
#after some trial and error
print "Exercise 1.4a: "
decode1 = decode_substitution_manually(code2,"J","t")
print decode1 
print

decode2 = decode_substitution_manually(decode1,"N","h")
print decode2
print

decode3 = decode_substitution_manually(decode2,"R","e")
print decode3
print

decode4 = decode_substitution_manually(decode3, "I", "a")
print decode4
print

decode5 = decode_substitution_manually(decode4, "T", "i")
print decode5
print

decode6 = decode_substitution_manually(decode5, "Z", "s")
print decode6
print

decode7 = decode_substitution_manually(decode6, "F", "w")
print decode7
print

decode8 = decode_substitution_manually(decode7, "B", "c")
print decode8
print

decode9 = decode_substitution_manually(decode8, "G", "r")
print decode9
print

decode10 = decode_substitution_manually(decode9, "D", "g")
print decode10
print

decode11 = decode_substitution_manually(decode10, "K", "u") 
print decode11
print

decode12 = decode_substitution_manually(decode11, "L", "o") 
print decode12
print

decode13 = decode_substitution_manually(decode12, "V", "v") 
print decode13
print

decode14 = decode_substitution_manually(decode13, "U", "l") 
print decode14
print

decode15 = decode_substitution_manually(decode14, "H", "d") 
print decode15
print

decode16 = decode_substitution_manually(decode15, "O", "m") 
print decode16
print

decode17 = decode_substitution_manually(decode16, "Q", "n") 
print decode17
print

decode18 = decode_substitution_manually(decode17, "S", "y") 
print decode18
print

decode19 = decode_substitution_manually(decode18, "W", "f") 
print decode19
print

decode20 = decode_substitution_manually(decode19, "X", "k") 
print decode20
print

decode21 = decode_substitution_manually(decode20, "E", "b") 
print decode21
print

decode22 = decode_substitution_manually(decode21, "M", "p") 
print decode22
print
		
print "Exercise 1.9b: "
print "GCD is ", euclidean_gcd(85652, 16261)
print

print "Exercise 1.10 as applied to 1.9b: "
print "Extended GCD is ", extended_Euclidean(16261,85652)
print

print "1.16d: ", (357*862*193) % 943
print

print "1.17f: " #using the hint suggested in the problem directions
for x in range(0,11):
	if (x**3 - x**2 + 2*x - 2) % 11 == 0:
		print x
		
	