# Author: Izaak Neutelings (July 2017)

def test():
    """Test function."""
    print ">>> test"
    


def testMultiline1():
    """This is a test function with a mulitline
docstring that describes it use.

Run it in the command line like
  $ python methodDocumentation.py"""
    print ">>> testMultiline"
    


def testMultiline2():
    """This is a test function with a mulitline
       docstring that describes it use.
       
       Run it in the command line like
         $ python methodDocumentation.py"""
    print ">>> testMultiline"
    


def testMultiline3():
    """
    This is a test function with a mulitline
    docstring that describes it use.
    
    Run it in the command line like
      $ python methodDocumentation.py
    """
    print ">>> testMultiline"
    


def testMultiline4():
    """
This is a test function with a mulitline
docstring that describes it use.

Run it in the command line like
  $ python methodDocumentation.py
    """
    print ">>> testMultiline"
    


print    
print "-"*50
print test.__doc__
print "-"*50
print testMultiline1.__doc__
print "-"*50
print testMultiline2.__doc__
print "-"*50
print testMultiline3.__doc__
print "-"*50
print testMultiline4.__doc__
print "-"*50
print