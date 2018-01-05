class Example(object):

    def __init__(self, a=0, s="default"):
        self.a = a
        self.s = s
        self.list = []
        self.check = 0
    
    def __getattr__(self,attr):
        if attr == 'sum':
            return sum(self.list)
        else:
            return getattr(self,attr)
    
#    # https://docs.python.org/2/reference/datamodel.html#object.__setattr__
#    def __setattr__(self,attr,value):
#        if attr == 'list':
#            self.check += 1
#            self.__dict__[attr] = value
#        else:
#            self.__dict__[attr] = value

    def run(self):
        print "Hello, world!"



if __name__ == '__main__':

    Example().run()
    
    # example to initiate object
    test1 = Example()
    test2 = Example(1,"own string")
    print "\n# a and s"
    print "test1: a=%s, s=\"%s\"" % (test1.a,test1.s)
    print "test2: a=%s, s=\"%s\"" % (test2.a,test2.s)

    # example to use __setattr__
    print "\n# list and sum"
    print "test1: list=%s, sum=%s, check=%s" % (test1.list,test1.sum, test1.check)
    print "test2: list=%s, sum=%s, check=%s" % (test2.list,test2.sum, test2.check)
    test2.list.append(1)
    test2.list.append(2)
    test2.list.append(3)
    print "\n# Append test2.list"
    print "test2: list=%s, sum=%s, check=%s" % (test2.list,test2.sum, test2.check)

    print "\n# Done\n"
