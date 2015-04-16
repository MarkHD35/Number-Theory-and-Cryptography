# -*- coding: utf-8 -*-
import math
from modularMath import *

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
         slope = (3.0*x1^2 + A)/(2*y1)
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

   #completed multiplcations, return the answer, which is accumulated in the new point
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

#basic unit tests of calculating points on elliptic curve in a finite field
def test_ecPointsInField():
   ec = (8,3,0,1)
   points = ecPointsInField(ec,13)
   if len(points) != 9:
      return False
   if not (points == [(infinity,infinity),(1,5),(1,8),(2,3),(2,10),(9,6),(9,7),(12,2),(12,11)]):
      return False
   return True

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

   if test_ecPointsInField():
      print "calculation of points in field appears to be working"
   else:
      testsPassed = False
      print "calculation of points in field failed"
   
   #print out aggregate results
   if testsPassed:
      print "All tests passed!"
   else:
      print "Some tests failed (see printout for more details)"

   #return aggregate results (in case we want to do something with this later)
   return testsPassed
if __name__ == "__main__":
   runTests()
   