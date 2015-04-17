# -*- coding: utf-8 -*-
import math
from modularMath import *
from hw4 import *
from random import randint

#infinity for more convenient reference
infinity = float("inf")

#compare equality of (2D) points
def pointsEqual(p1,p2):
   return (p1[0] == p2[0] and p1[1] == p2[1])

#add over elliptic curve
#elliptic curve has form y^2 = a_0 + a_1x + a_2x^2 + a_3x^3ax^3
#(specifically a_2 = 0)
#represented as (a_0,a_1,a_2,a_3)
#points have form (xCoord,yCoord)
#O is represented by x coordinate of infinity

#BASED ON ELLIPTIC CURVE ADDITION ALGORITHM (THEOREM 5.6 in HPS)
def ecAdd(ec,p1,p2):
   x1 = p1[0]
   y1 = p1[1]
   x2 = p2[0]
   y2 = p2[1]
   
   #coefficient on the X term in the elliptic curve
   A = ec[1]
   
   #placeholder so variable doesn’t go out of scope (will be used in computing answer)
   slope = 0

   #one of the points is O, the infinity point
   if p1[0] == infinity:
      return p2
   elif p2[0] == infinity:
      return p1

   #vertical line: answer is O, which lies on every vertical line
   elif x1 == x2 and y1 == -y2: 
      return (infinity,infinity) 
   else:
      if pointsEqual(p1,p2):
         slope = (3.0*x1**2 + A)/(2*y1)
      else: 
         slope = 1.0*(y2 - y1)/(x2 - x1)

   solX = slope**2 - x1 - x2
   solY = slope*(x1 - solX) - y1
   return (solX,solY)
    

#THIS IS BASED ON THE STEPS IN EX. 5.1: MORE INTUITIVE BUT FAILS TO TAKE INTO ACCOUNT O, VERTICAL LINES, ETC.
#ecAdd is an implementation of the Elliptic Curve Addition Algorithm
def ecAdd_old(ec,p1,p2):
   line = calculateLine(p1,p2)
   #slope (i.e. m)
   slope = line[0]
   #y-intercept (i.e. b)
   intercept = line[1]

   #now we have the form (mx+b)^2 = a_0 + a_1x + a_2x^2 + a_3x^3ax^3
   #i.e. m^2x^2 + 2bmx + b^2 = a_0 + a_1x + a_2x^2 + a_3x^3ax^3
   #so we need to subtract b^2 from a_0, 2bm from a_1, and m^2 from a_2
   #get a new cubic polynomial, two of whose roots we know (x-coordinates of points on line)
   #need to get the third root to get (the negative of) the x-coordinate we need
   coeff0 = ec[0] - intercept**2
   coeff1 = ec[1] - 2*intercept*slope
   coeff2 = ec[2] - slope**2
   coeff3 = ec[3]
   cubicPolynomial = (coeff0,coeff1,coeff2,coeff3)

   #we know that cubicPolynomial[0], the constant factor, must be a product of the all the roots
   #two of the polynomial’s roots are the x-coordinates of the known points
   #so we can solve for the third root that we want
   root1 = -p1[0]
   root2 = -p2[0]
   root3 = -cubicPolynomial[0]/(1.0*root1*root2)

   #use the equation of the line to calculate the y-coordinate
   root3_yCoord = line[0]*root3 + line[1]

   #return a new point composed of the third root and its corresponding y-coordinate on the line, reflected about the x-axis
   return (root3,-root3_yCoord)

#calculate point between line
#points have form (xCoord,yCoord)
#lines have form y = mx+b
#represented as (m,b)
def calculateLine(p1,p2):
   x1 = p1[0]
   y1 = p1[1]
   x2 = p2[0]
   y2 = p2[1]
   slope = 1.0*(y2 - y1)/(x2 - x1)
   intercept = y1 - slope*x1
   return (slope,intercept)

#ecAdd over finite field (with modulus)
#assume: coordinates of points are in the field of integers mod the modulus
#TODO: maybe just make extra parameter in other ecAdd method
#TODO: either way support modular operations for subtract and multiply
def ecAdd_mod(ec,p1,p2,modulus):
   x1 = p1[0]
   y1 = p1[1]
   x2 = p2[0]
   y2 = p2[1]
   
   #coefficient on the X term in the elliptic curve
   A = ec[1]
   
   #placeholder so variable doesn’t go out of scope (will be used in computing answer)
   slope = 0

   #one of the points is O, the infinity point
   if p1[0] == infinity:
      return p2
   elif p2[0] == infinity:
      return p1

   #vertical line: answer is O, which lies on every vertical line
   elif x1 == x2 and y1 == -y2:
      return (infinity,infinity) 
   else:
      if pointsEqual(p1,p2):
         slope = ((3*x1**2 + A)%modulus) * inverse((2*y1)%modulus,modulus)
         #if inverse(2*y1,modulus) == 0:
            #print "Inverse is 0 mod ", modulus
            #return (-infinity,infinity)
            #print "Inverse is 0 mod ", modulus
         slope = slope % modulus
      else: 
         slope = ((y2 - y1)%modulus) * inverse((x2 - x1)%modulus,modulus)
         #if inverse(x2 - x1,modulus) == 0:
            #print "Inverse is 0 mod ", modulus
            #return (-infinity,infinity)
            #print "Inverse is 0 mod ", modulus
         slope = slope % modulus
   
   solX = (slope**2 - x1 - x2)%modulus

   solY = (slope*(x1 - solX) - y1)%modulus
   #print modulus
   return (solX,solY)

#subtraction with elliptic curves
#subtract p1 from p2
#basically add the reflection of p2 around x-axis (same x-coordinate, negative of y-coordinate)
def ecSubtract(ec,p1,p2):
   reflected_p2 = (p2[0],-p2[1])
   return ecAdd(ec,p1,reflected_p2)

#scalar (integer) multiplication on elliptic curve
#calls a helper method (so user doesn’t have to pass in extra parameter)
def ecMultiply(ec,point,scalar):
   if scalar == 1:
      return point
   else: 
      initialFactor = 1
      return ecMultiply_helper(ec,point,point,scalar,initialFactor)

#method that actually performs integer multiplication on elliptic curve
#recursive: compute 2p = p + p, then 3p = 2p + p…(factor)p = (factor - 1)p + p 
#(factor-1)p is the sum point 
def ecMultiply_helper(ec,sumPoint,point,scalar,factor):
   newPoint = ecAdd(ec,sumPoint,point)
   newFactor = factor + 1

   #haven’t completed the multiplications
   if newFactor < scalar:
      return ecMultiply_helper(ec,newPoint,point,scalar,newFactor)

   #completed multiplications, return the answer, which is accumulated in the new point
   else:
      return newPoint

#SAME AS SCALAR MULTIPLICATION IMPLEMENTATION ABOVE, BUT W.R.T. A MODULUS
#TODO: REFACTOR INTO ABOVE CODE
#scalar (integer) multiplication on elliptic curve
#calls a helper method (so user doesn’t have to pass in extra parameter)
def ecMultiply_mod(ec,point,scalar,modulus):
   if scalar == 1:
      return point
   else: 
      initialFactor = 1
      return ecMultiply_mod_helper(ec,point,point,scalar,initialFactor,modulus)

#method that actually performs integer multiplication on elliptic curve
#recursive: compute 2p = p + p, then 3p = 2p + p…(factor)p = (factor - 1)p + p 
#(factor-1)p is the sum point 
def ecMultiply_mod_helper(ec,sumPoint,point,scalar,factor,modulus):
   newPoint = ecAdd_mod(ec,sumPoint,point,modulus)
   newFactor = factor + 1

   #haven’t completed the multiplications
   if newFactor < scalar:
      return ecMultiply_mod_helper(ec,newPoint,point,scalar,newFactor,modulus)

   #completed multiplications, return the answer, which is accumulated in the new point
   else:
      return newPoint

#calculate points on an elliptic curve that are in a field F_p (integers mod p)
def ecPointsInField(ec,modulus):
   pointsList = [(infinity,infinity)] #start off by adding O
   for x in range(0,modulus):
      #substitute each x into elliptic curve equation
      #recall that ec[2] is 0 (no X^2 term in an elliptic curve)
      ecY2 = ec[0] + ec[1]*x + ec[3]*x**3
      sqrts_ecY2 = sqrt_mod(modulus,ecY2)
      if len(sqrts_ecY2) > 0:
         for y in sqrts_ecY2:
            pointsList.append((x,y))
   return pointsList

#takes in an integer N that is the product of 2 primes and factors it
#using Lenstra's algorithm
#FIXME
def ecFactor(N):
   #choose random values
   A = randint(0,N)
   a = randint(0,N)
   b = randint(0,N)

   #create point and elliptic curve
   point = (a,b)
   #modular calculation of the constant coefficient
   coeff0 = (b**2 % N) - (a**3 % N) - (A*a % N)
#   while coeff0 < 0:
#      coeff0 += N
   coeff0 = coeff0 % N

   #elliptic curve
   ec = (coeff0,A,0,1)

   #loop up to a "specified bound" which we set to be up to N
   for j in range(2,N):
      oldPoint = point
      point = ecMultiply_mod(ec,point,j,N)
      #if this calculation fails we've found a nontrivial divisor of N
      if point[0] == -infinity:
         print("failed to perform calculation at %d!" % j)
         divisor = (point[0] - oldPoint[0]) % N
         if divisor < N:
            return (divisor, N/divisor)
         elif divisor == N: #try again with new curve
            return ecFactor(N)

   


#********UNIT TESTS**********

#basic unit tests of line calculation
#more extensive ones may be ideal but this is a very simple function
def test_line():
   if calculateLine((1,2),(2,4)) != (2,0):
      print "1"
      return False
   if calculateLine((2,6),(3,3)) != (-3,12):
      print "2"
      return False
   if calculateLine((-2,11),(1,8)) != (-1,9):
      print "4"
      return False
   return True

#basic unit tests of elliptic curve addition (Example 5.1 from HPS)
#HOWEVER I BELIEVE THEY HAVE A SIGN ERROR
def test_ecAdd():
   roundingError = 0.001
   sumPoint = ecAdd((18,-15,0,1),(7,16),(1,2))
   expected = (-23.0/9,170/27.0)
   if abs(sumPoint[0] - expected[0]) > roundingError or abs(sumPoint[1] - expected[1]) > roundingError:
      return False
   return True

#basic unit tests for subtraction
#more extensive ones perhaps useful (this just manually reflects a point and confirms that ecSubtract reflects correctly)
def test_ecSubtract():
   ec = (17,0,0,1)
   p1 = (-1,4)
   p2 = (-2,5)
   p2_reflected = (-2,-5)
   addReflection = ecAdd(ec,p1,p2_reflected)
   subtraction = ecSubtract(ec,p1,p2)
   return pointsEqual(addReflection,subtraction)

#basic unit tests for subtraction
#more extensive ones perhaps useful (this only tests multiplication by 2)
def test_ecMultiply():
   ec = (17,0,0,1)
   p1 = (-1,4)
   addSamePoint = ecAdd(ec,p1,p1)
   times2 = ecMultiply(ec,p1,2)
   return pointsEqual(addSamePoint,times2)

#basic unit tests of calculating points on elliptic curve in a finite field
def test_ecPointsInField():
   ec = (8,3,0,1)
   points = ecPointsInField(ec,13)
   if len(points) != 9:
      return False
   if not (points == [(infinity,infinity),(1,5),(1,8),(2,3),(2,10),(9,6),(9,7),(12,2),(12,11)]):
      return False
   return True

#unit test for elliptic curve addition over finite field
#from Example 5.24 in HPS
def test_ecAdd_mod():
   p1 = (9,7)
   p2 = (1,8)
   ec = (8,3,0,1)
   mod = 13
   sum_mod = ecAdd_mod(ec,p1,p2,mod)
   return pointsEqual(sum_mod,(2,10))

#unit test for elliptic curve multiplication over finite field
#from Example 5.24 in HPS
def test_ecMultiply_mod():
   point = (9,7)
   curve = (8,3,0,1)
   scalar = 2
   modulus = 13
   if not pointsEqual(ecMultiply_mod(curve,point,scalar,modulus),(9,6)):
      print "failed test 1"
      return False

   point = (3466,2996)
   ec = (19,14,0,1)
   mod = 6887
   x3mod = ecMultiply_mod(ec,point,3,mod)
   #print x3mod
   return pointsEqual(x3mod,(3067,396))

#basic unit tests for elliptic curve factorization
def test_ecFactor():
   factorization187 = ecFactor(187)
   return False
   #return ( pointsEqual(factorization187,(11,17)) or pointsEqual(factorization187,(17,11)) )

#run the unit tests
def runTests():
   testsPassed = True
   if test_line():
      print "line calculation appears to be working"
   else:
      testsPassed = False
      print "line calculation failed" 

   if test_ecAdd():
      print "elliptic curve addition appears to be working"
   else:
      testsPassed = False
      print "elliptic curve addition failed"

   if test_ecSubtract():
      print "elliptic curve subtraction appears to be working"
   else:
      testsPassed = False
      print "elliptic curve subtraction failed"

   if test_ecMultiply():
      print "elliptic curve multiplication appears to be working"
   else:
      testsPassed = False
      print "elliptic curve multiplication failed"

   if test_ecPointsInField():
      print "calculation of points in field appears to be working"
   else:
      testsPassed = False
      print "calculation of points in field failed"

   if test_ecAdd_mod():
      print "elliptic curve addition over finite field appears to be working"
   else:
      testsPassed = False
      print "elliptic curve addition over finite field failed"

   if test_ecMultiply_mod():
      print "elliptic curve multiplication over finite field appears to be working"
   else:
      testsPassed = False
      print "elliptic curve multiplication over finite field failed"

   if test_ecFactor():
      print "elliptic curve factorization appears to be working"
   else:
      testsPassed = False
      print "elliptic curve factorization failed"
   
   #print out aggregate results
   if testsPassed:
      print "All tests passed!"
   else:
      print "Some tests failed (see printout for more details)"

   #return aggregate results (in case we want to do something with this later)
   return testsPassed
if __name__ == "__main__":
   runTests()

   '''
   #problem 5.2
   ec52 = (17,0,0,1)
   P52 = (-1,4)
   Q52 = (2,5)
   print "Problem 5.2: "
   print "P + Q = ", ecAdd(ec52,P52,Q52)
   print "P - Q = ", ecSubtract(ec52,P52,Q52)
   print "2P = ", ecMultiply(ec52,P52,2)
   print "2Q = ", ecMultiply(ec52,Q52,2)
   print

   print "Problem 5.5a: "
   ec55a = (2,3,0,1)
   print "The set of points $E(F_7)$ is the set of solutions to $Y^2 = X^3 + 3X + 2$ over $F_7$: ",
   print ecPointsInField(ec55a,7)
   print

   print "Problem 5.6a: "
   ec56a = (2,1,0,1)
   EF5_56a = ecPointsInField(ec56a,5)
   
   #column headers
   print "            ",
   for point in EF5_56a:
      print("(%.3f,%.3f)   " % (point[0],point[1])),
   print

   #table values
   for point1 in EF5_56a:
      #row headers
      print("(%.3f,%.3f)   " % (point1[0],point1[1])),

      for point2 in EF5_56a:
         sum = ecAdd_mod(ec56a,point1,point2,5)
         print("(%.3f,%.3f)   " % (sum[0],sum[1])),
      print
   print
   
   print "Problem 5.7c,d: "
   ec57 = (1,1,0,1)
   mod57c = 7
   mod57d = 11

   EFp57c = ecPointsInField(ec57,mod57c)
   print EFp57c
   print "5.7c size of E(F_p): ", len(EFp57c)
   traceF57c = mod57c+1-len(EFp57c)
   print "5.7c trace of Frobenius: ", traceF57c
   print "5.7d 2sqrt(p): ", 2*math.sqrt(mod57c)

   EFp57d = ecPointsInField(ec57,mod57d)
   print EFp57c
   print "5.7d size of E(F_p): ", len(EFp57d)
   traceF57d = mod57d+1-len(EFp57d)
   print "5.7d trace of Frobenius: ", traceF57d
   print "5.7d 2sqrt(p): ", 2*math.sqrt(mod57d)

   print
   '''

   print "5.18a:"
   N = 589
   point = (2,5)

   #elliptic curve
   ec = (9,4,0,1)
   print ecFactor(N)

   factors = factor(N)
   print factors

   print inverse(5,13)