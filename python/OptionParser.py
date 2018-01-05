from optparse import OptionParser
import sys, os
import ConfigParser

# https://docs.python.org/2/library/optparse.html

argv = sys.argv
parser = OptionParser()
parser.add_option("-b", "--boolean", dest="boolean", default=False, action='store_true',
                  help="set a boolean, e.g. for an option.")
parser.add_option("-s", "--string", dest="string", default=None, action='store',
                  metavar="STRING",help="set a string, e.g. to input a filename.")
parser.add_option("-n","--number", type='int', dest="number", default=None, action='store',
                  help="set a number")
(opts, args) = parser.parse_args(argv)



def main():

    print "\nOption parser:"
    print ">>> opts = %s " % opts # dictionairy
    print ">>> args = %s " % args # list

    print "\nYou have chosen the following options:"
    if opts.boolean:
        print ">>> boolean = True"
    else:
        print ">>> boolean = False"
    # print ">>> opts.boolean = %s " % opts.boolean
    print ">>> string = %s" % opts.string
    print ">>> number = %s" % opts.number



if __name__ == '__main__':
    main()
    print "\nDone."