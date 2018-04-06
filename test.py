from functools import reduce
from inspect import getargspec
from pytester.test_results import TestResults
from termcolor import cprint
from pytester.error_object import ErrorObject

# Build TestArguments function that takes in a dictionary
# Rename vars


class Test:
    args = []
    argEval = []
    nextIndex = 0

    def __init__(self, function, args, argEval=None,
                 name="New", long=False, consoleOutput=True,
                 print_errors=False):
        self.long = long
        self.print_errors = print_errors
        self.testEval = False if argEval is None else True
        self.function = function
        self.args = args
        self.argEval = argEval
        self.size = len(args)
        reducer = lambda x, y: x if x >= y else y
        mapper = lambda x: len(str(x))
        self.lagestArg = reduce(reducer, map(mapper, self.args))
        self.argsString = " , ".join(getargspec(self.function).args)
        self.results = [None] * self.size
        self.errors = [None] * self.size
        self.name = name
        self.consoleOutput = consoleOutput

        if self.consoleOutput:
            print("\nNew Test \'%s\' Created" % (self.name))
            message = "Function: %s ( %s )\n"
            messageArgs = (self.function.__name__, self.argsString)
            message = message % messageArgs
            print(message)

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
        try:
            self.results[index] = self.runFunction(index)
        except Exception as e:
            return ErrorObject(e, index, self.name, self.args[index])
        return None

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
                testOut.error = True
                self.errors[index] = error
                testOut.errorName = error.name
                try:
                    passedErrorName = self.argEval[index].__name__
                    testOut.passed = passedErrorName == testOut.errorName
                    if(testOut.passed):
                        testOut.errPredicted = True
                # (TypeError, AttributeError) as e: <- if broken
                except Exception:
                    testOut.passed = False

            self.results[index] = testOut
            return testOut

    def next(self):
        try:
            testOut = self.test(self.nextIndex)
            if self.consoleOutput:
                if(testOut.passed and self.consoleOutput):
                    print(testOut)
                else:
                    cprint(testOut, 'red')
                if self.print_errors and testOut.error:
                    self.printError(self.nextIndex)
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
        except Exception as e:
            raise e

    def allResults(self):
        passedAll = True
        for i in range(0, self.size):
            if self.results[i] is None:
                output = self.test(i)
                self.results[i] = output
            else:
                output = self.results[i]

            passedAll = not output.passed
            if self.consoleOutput:
                if(output.passed):
                    print(output)
                else:
                    cprint(output, 'red')
                if self.print_errors and output.error:
                    self.printError(i)

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
            message = (
                "\nAll tests have been ran and the "
                "function \'%s\' has passed all tests!\n"
            )
            cprint(message % self.name, 'green', attrs=['bold'])
        else:
            message = (
                "\nAll tests have been ran and the "
                "function \'%s\' has failed %i tests!\n"
            )
            cprint(message % (self.name, notPassed), 'red', attrs=['bold'])

    def printError(self, index):
        if self.errors[index] is None:
            print("There is no error for this test.\n")
        else:
            cprint(self.errors[index], 'red')

    def resultsCompleted(self):
        for i in self.results:
            if i is None:
                return False
        return True
