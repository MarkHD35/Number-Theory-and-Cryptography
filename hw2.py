#For Math 4351, Number Theory and Cryptography, at Washington University in St. Louis in Spring 2015
#This file is where I did my computer-assisted scratch work for HW 2
#For instructor verification if desired

from code_Math4351hw1 import *

#1.32a
if primitivity_test(2,7): print ("2 is a primitive root of %d" % 7)
if primitivity_test(2,13): print ("2 is a primitive root of %d" % 13)
if primitivity_test(2,19): print ("2 is a primitive root of %d" % 19)
if primitivity_test(2,23): print ("2 is a primitive root of %d" % 23)

#1.32c
print ("%d is a primitive root of %d" %(find_primitive_roots(23)[0],23))
print ("%d is a primitive root of %d" %(find_primitive_roots(29)[0],29))
print ("%d is a primitive root of %d" %(find_primitive_roots(41)[0],41))
print ("%d is a primitive root of %d" %(find_primitive_roots(43)[0],43))
		
	