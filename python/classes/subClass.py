# http://www.jesshamrick.com/2011/05/18/an-introduction-to-classes-and-inheritance-in-python/
# https://stackoverflow.com/questions/2843165/python-how-to-inherite-and-override
# http://blog.thedigitalcatonline.com/blog/2014/05/19/method-overriding-in-python/
# https://docs.python.org/2.7/library/functions.html#super



class Animal(object):
  
  def __init__(self,name,age):
    self.name = name
    self.age  = age
  
  def makeNoise(self):
    print ">>> %s makes a noise"%(self.name)
  
  def printName(self):
    print ">>> Animal name = \"%s\""%(self.name)
  
  def printClassification(self):
    print ">>> Animal"


class Dog(Animal):
  
  def __init__(self,name,age):
    Animal.__init__(self,name,age)
    # or super(Dog,self).__init__(name,age)]
  
  def makeNoise(self):
    print ">>> %s says \"%s\""%(self.name,"Woof!")
  
  def printName(self):
    print ">>> Dog name = \"%s\""%(self.name)
  
  def printClassification(self):
    super(Dog,self).printClassification()
    print ">>>   Dog"
  


animal1 = Animal("Carrol",2)
animal2 = Dog("Yeller",4)

print "\n>>> animal 1"
animal1.makeNoise()
animal1.printName()

print ">>>\n>>> animal 2"
animal2.makeNoise()
animal2.printName()
animal2.printClassification()
print


