from ROOT import gRandom

for i in xrange(100):
    print int(gRandom.Uniform()*10)