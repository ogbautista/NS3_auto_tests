class Ns3Time:
    def __init__ (self, texttime):
        amount, units = texttime[:-2], texttime[-2:]
        if units == 'ns':
            convFactor = 1e6
        elif units == 'us':
            convFactor = 1e3
        elif units == 'ms':
            convFactor = 1
        else:
            raise ValueError ("Unknown time unit: {}".format(units))
        self.mstime = float(amount)/convFactor

    def getSeconds(self):
        return self.mstime / 1000

    def getMilliSeconds(self):
        return self.mstime

    def getMicroSeconds(self):
        return mstime*1000

    def getNanoSeconds(self):
        return mstime*1e6
