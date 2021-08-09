# https://stackoverflow.com/questions/2843165/python-how-to-inherite-and-override
# http://blog.thedigitalcatonline.com/blog/2014/05/19/method-overriding-in-python/

class A:
  def f(self):
    print("in f")

  def h(self):
    print("in h")

class B(A):
  def f(self):
    print("in B:f")

def test(x):
  x.f()
  x.h()

test(A())
test(B())