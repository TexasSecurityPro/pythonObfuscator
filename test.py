# File used to test the effectiveness of the obfuscator
# it needs some work still.

from datetime import datetime
import pandas as pd
import numpy
import re
import string

# Basic Variables
testString = 'This is string!'
otherString = "Quotes don't matter in strings."
integerFive = 5
floatFive = 5.0
flaseFive = integerFive == floatFive
booleanFalse = False
listOfFives = [5, 5, 5, 5, 5]
dictOfNumbers = {0:5, 1:5, 2:6, 3:5, 4:40}

# Functions
def testFunction():
    print('This is a test function!')

def testFunctionWithArgs(arg1, arg2):
    print('This is a test function with arguments!')
    print(arg1)
    print(arg2)

def testFunctionWithArgsAndReturn(arg1, arg2):
    print('This is a test function with arguments and return!')
    print(arg1)
    print(arg2)
    return arg1 + arg2


# Classes
class TestClass:
    def __init__(self):
        self.test = 'This is a test class!'
        print(self.test)

    def testMethod(self):
        print('This is a test method!')

    def testMethodWithArgs(self, arg1, arg2):
        print('This is a test method with arguments!')
        print(arg1)
        print(arg2)

    def testMethodWithArgsAndReturn(self, arg1, arg2):
        print('This is a test method with arguments and return!')
        print(arg1)
        print(arg2)
        return arg1 + arg2


# Test Functions
testFunction()
testFunctionWithArgs(5, 6)
testFunctionWithArgsAndReturn(5, 6)

# Testing each class
testClass = TestClass()
testClass.testMethod()
testClass.testMethodWithArgs(5, 6)
testClass.testMethodWithArgsAndReturn(5, 6)

# Testing each variable
print(testString)
print(otherString)
print(integerFive)
print(floatFive)
print(flaseFive)
print(booleanFalse)
print(listOfFives)
print(dictOfNumbers)

# Testing each library
print(datetime.now())
print(pd.DataFrame())
print(numpy.array([1, 2, 3]))
print(re.search('test', 'This is a test string!'))
