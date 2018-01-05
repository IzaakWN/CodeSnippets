import os, sys
import time
# http://stackoverflow.com/questions/3249524/print-in-one-line-dynamically
# http://stackoverflow.com/questions/3160699/python-progress-bar



def printSameLine(string):
    """Print string without making new line. (Write to stdout and flush.)"""
    sys.stdout.write(string+" ")
    sys.stdout.flush()


def counter(N=10):
    """Count to some number on the same line."""
    print ">>> ",
    for i in range(1,max(N,1)+1):
        printSameLine("%i,"%i)
        time.sleep(1)
    print " "


def overCounter(N=10):
    """Count to some number on the same line."""
    print ">>>      ",
    for i in range(1,max(N,1)+1):
        sys.stdout.write("\b"*(5 if i<11 else 6))
        printSameLine("%i..."%i)
        time.sleep(1)
    print " "


def loadingBar(width=10):
    """Updating loading bar for some width."""
    sys.stdout.write(">>> [%s]" % (" " * width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (width+1)) # return to start of line, after '['
    for i in xrange(width):
        time.sleep(1) # do real work here
        sys.stdout.write("=")
        sys.stdout.flush()
    sys.stdout.write("\n")


def main():
    """Main function."""

    print ">>> "
    counter(12)
    overCounter(12)
    loadingBar(12)



if __name__ == '__main__':
    
    print " "
    main()
    print ">>>\n>>> done\n"


