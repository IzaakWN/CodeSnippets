from ROOT import THStack, TH1D, gRandom
from math import sqrt

hist1 = TH1D("hist1","hist1",10,0,100)
hist1.Sumw2()

for i in xrange(1000):
    weight1 = gRandom.Gaus(1,0.1)
    hist1.Fill(gRandom.Gaus(55,20),weight1)

bincontents1 = [ ]
for i, binc in enumerate(hist1):
    bincontents1.append((i,binc,hist1.GetBinError(i)))

print "\n>>> before scaling"
print ">>>   hist1.Integral()   = %s" % hist1.Integral()
print ">>>   hist1.GetEntries() = %s" % hist1.GetEntries()

scale = 0.5
hist1.Scale(scale)
bincontents2 = [ ]
for i, binc in enumerate(hist1):
    bincontents2.append((i,binc,hist1.GetBinError(i)))

print "\n>>> after scaling with scale=%s"%scale
print ">>>   hist1.Integral()   = %s" % hist1.Integral()
print ">>>   hist1.GetEntries() = %s" % hist1.GetEntries()

print "\n>>> comparing bin contents"
print ">>>   %3s %20s %20s"%("","before scaling","after scaling")
print ">>>   %3s    %8s %8s    %8s %8s"%("bin","content","error","content","error")
for (i,b1,e1),(i,b2,e2) in zip(bincontents1,bincontents2):
    print ">>>   %3d    %8.1f %8.2f    %8.1f %8.2f" % (i,b1,e1,b2,e2)

print