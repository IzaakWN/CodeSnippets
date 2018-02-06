from cStringIO import StringIO
import sys

class capturing(object):
    """Capture"""

    def __init__(self,**kwargs):
        self.old_stdout = sys.stdout
        self.captured0 = StringIO()
        sys.stdout = self.captured0

    def stop(self):
        sys.stdout = self.old_stdout
        self.captured0.close()

    def captured(self):
        sys.stdout = self.old_stdout
        out = self.captured0.getvalue()
        self.captured0.close()
        if '\n' in out[-2:]: out = out[:-1]
        return out



print
print ">>> start"
capture = capturing()
print "1 lol"
print "2 lol"
captured = capture.captured()
print ">>> stop"
print captured
print ">>> done"

print
print ">>> start2"
capture2 = capturing()
print "3 lol"
print "4 lol"
captured2 = capture2.captured()
print ">>> stop2"
print captured2
print ">>> done2"
print