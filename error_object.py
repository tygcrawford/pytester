from traceback import format_tb

class ErrorObject:
    def __init__(self, error, index, name, args):
        self.args = args
        self.funcName = name
        self.error = error
        self.index = index
        self.tb = self.error.__traceback__
        self.name = type(self.error).__name__
        self.desc = str(self.error)
        errWords = format_tb(self.tb)[len(format_tb(self.tb)) - 1].split(' ')
        self.file = errWords[3][1:len(errWords[3]) - 2]
        self.line = errWords[5][:len(errWords[5]) - 1]
        self.errVerbose = ''.join(format_tb(self.tb))
        self.code = format_tb(self.tb)[len(format_tb(self.tb)) - 1].split('\n')[1].lstrip(' ')

    def getVerbose(self):
        return self.errVerbose

    def __str__(self):
        message  = "\'%s\' Error[%i]:\n" % (self.funcName, self.index)
        message += "\t%s: %s\n" % (self.name, self.desc)
        message += "\tFile: %s\n" % (self.file)
        message += "\tLine: %s\n" % (self.line)
        message += "\tCode: %s\n" % (self.code)
        message += "\tArgs: %s\n" % (self.args)
        return message
