from cStringIO import StringIO
import sys


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self._stringio.getvalue().splitlines()
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


#with Capturing() as output:
#    print "hello world"
#print ">>> captured"
#
#with Capturing(output) as output:  # note the constructor argument
#    print "hello world again"
#print ">>> done"
#print ">>> output:", output


def test(i):
    print "\n>>> test %i" % i
    print ">>> capturing"
    with Capturing() as test_output:
        print "Hello world %i times" % i
    print ">>> captured"
    print ">>> output: ", test_output
    print ">>> output: ", ''.join(test_output)
#    print ">>> output: ", test_output.read(1)
    print ">>> test %i done" % i


for i in range(1,5):
    test(i)
    print
