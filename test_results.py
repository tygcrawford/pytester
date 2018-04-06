class TestResults:
    args = None
    realEval = None
    intendedEval = None
    errorName = None
    passed = None
    index = None
    errPredicted = None
    long = None
    testEval = None

    def __init__(self, name):
        self.name = name

    def __str__(self):
        d = "  |  "
        errorStr = "No " if self.errorName is None else "Yes"
        predictedStr = "Yes" if self.errPredicted else "No "

        if(self.long):
            message =  "\'%s\' Test[%i]:\n" % (self.name, self.index)
            message += "\tErrors: %s\n" % (errorStr)
            message += "\tPassed: %s\n" % (self.passed)
            message += "\tArg: %s\n" % (str(self.args))

            if(self.errorName is None):
                message += "\tReal Eval: %s\n" % (str(self.realEval))
                if self.testEval:
                    message += "\tIntended Eval: %s\n" % (str(self.intendedEval))
            else:
                if self.testEval:
                    message += "\tIntended Eval: %s\n" % (str(self.intendedEval))
                    message += "\tError Predicted: %s\n" % (predictedStr)
                message += "\tError Name: %s\n" % (self.errorName)

        else:
            message = "\'%s\' Test[%i]%sErrors: %s%sPassed: %s%sArg: %s%s"
            message = message % (self.name, self.index, d, errorStr, d, self.passed, d, str(self.args), d)

            if(self.errorName is None):
                message += "Real Eval: %s%s" % (str(self.realEval), d)
                if self.testEval:
                    message += "Intended Eval: " + str(self.intendedEval)
            else:
                if self.testEval:
                    message += "Intended Eval: " + str(self.intendedEval) + d
                    message += "Error Predicted: " + predictedStr + d
                message += "Error Name: " + self.errorName
        return message

    __repr__ = __str__
