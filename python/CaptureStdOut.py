from cStringIO import StringIO
import sys

print
print ">>> start"
old_stdout = sys.stdout
sys.stdout = mystdout = StringIO()
print "1 lol"
print "2 lol"
sys.stdout = old_stdout
print ">>> stop"
print mystdout.getvalue()
print ">>> done"

print ">>> start2"
old_stdout2 = sys.stdout
sys.stdout = mystdout2 = StringIO()
print "3 lol"
print "4 lol"
sys.stdout = old_stdout2
print ">>> stop2"
print mystdout2.getvalue(),
print ">>> done2"
print