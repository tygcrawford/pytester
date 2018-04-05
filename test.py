from functools import reduce
from inspect import getargspec
from pytester.test_results import TestResults
from termcolor import cprint

#write in an array string deconstructor so you can take in stuff like that from files so you can test an object
#this allows for larger test batches and even construction of test batches with other python scripts

class Test:
    args = []
    argEval = []
    nextIndex = 0

    def __init__(self, function, args, argEval = None, name = "New", long = False, consoleOutput = True):
        self.testEval = False if argEval is None else True
        self.long = long
        self.function = function
        self.args = args
        self.argEval = argEval
        self.name = name
        self.size = len(args)
        self.lagestArg = reduce(lambda x, y: x if x >= y else y, map(lambda x: len(str(x)), self.args))
        self.results = [None] * self.size
        self.consoleOutput = consoleOutput

        if self.consoleOutput:
            print("\nNew Test \'%s\' Created" % (self.name))
            print("Function: %s ( %s )\n" % (self.function.__name__, " , ".join(getargspec(self.function).args)))

    def getTestsCompleted(self):
        countDone = 0
        for i in range(0, self.size):
            if i is not None:
                countDone += 1
        return countDone

    def runFunction(self, index):
        arg = self.args[index]

        if(type(arg) is tuple and len(getargspec(self.function).args) > 1):
            return self.function(*arg)
        else:
            return self.function(arg)

    def getErrors(self, index):
        error = None
        try:
            self.results[index] = self.runFunction(index)
        except Exception as e:
            error = type(e).__name__
        return error

    def test(self, index):
        if(self.results[index] is not None):
            return self.results[index]
        else:
            testOut = TestResults(self.name)
            error = self.getErrors(index)

            testOut.testEval = self.testEval
            testOut.long = self.long
            testOut.index = index
            testOut.args = self.args[index]

            if self.testEval:
                testOut.intendedEval = self.argEval[index]

            if(error is None):
                testOut.realEval = self.results[index]
                if(self.testEval):
                    testOut.passed = testOut.realEval == testOut.intendedEval
                else:
                    testOut.passed = True
            else:
                testOut.errorName = error
                try:
                    testOut.passed = self.argEval[index].__name__ == testOut.errorName
                    if(testOut.passed):
                        testOut.errPredicted = True
                except: # (TypeError, AttributeError) as e: <- if broken
                    testOut.passed = False

            self.results[index] = testOut
            return testOut

    def printTest(self, index):
        print(self.test(index))

    def next(self):
        try:
            testOut = self.test(self.nextIndex)
            if self.consoleOutput:
                if(testOut.passed and self.consoleOutput):
                    print(testOut)
                else:
                    colored(testOut, 'red')
            self.nextIndex += 1
            countDone = self.getTestsCompleted()
            if countDone == self.size and self.consoleOutput:
                self.endPrint()

            if self.consoleOutput:
                return testOut.passed
            else:
                return testOut

        except IndexError:
            raise IndexError("You have already tested all args provided")

    def allResults(self):
        passedAll = True
        for i in range(0, self.size):
            if self.results[i] is None:
                output = self.test(i)
                self.results[i] = output
            else:
                output = self.results[i]

            if(output.passed == False):
                passedAll = False
            if self.consoleOutput:
                if(output.passed):
                    print(output)
                else:
                    cprint(output, 'red', attrs=['bold'])
        if self.consoleOutput:
            self.endPrint()
            return passedAll
        else:
            return list(self.results)

    def endPrint(self):
        passedAll = True
        notPassed = 0
        for result in self.results:
            if not result.passed:
                notPassed += 1
                passedAll = False

        if passedAll:
            message = "\nAll tests have been ran and the function \'%s\' has passed all tests!"
            cprint(message % self.name, 'green', attrs=['bold'])
        else:
            message = "\nAll tests have been ran and the function \'%s\' has failed %i tests!"
            cprint(message % (self.name, notPassed), 'red', attrs=['bold'])
