from ROOT import THStack, TH1D, gRandom
from math import sqrt

hist1 = TH1D("hist1","hist1",10,0,100)
hist2 = TH1D("hist2","hist2",10,0,100)
hist1.Sumw2()
hist2.Sumw2()
stack = THStack("stack","stack")

for i in xrange(1000):
    weight1 = gRandom.Gaus(1,0.1)
    weight2 = gRandom.Gaus(1,0.2)
    hist1.Fill(gRandom.Gaus(55,20),weight1)
    hist2.Fill(gRandom.Gaus(50,25),weight2)
    
stack.Add(hist1)
stack.Add(hist2)

hist_stack = stack.GetStack().Last()
print "\n>>> hist_stack = stack.GetStack().Last()"
print ">>>   hist_stack = %s" % hist_stack
print ">>>   type(hist_stack) = %s" % type(hist_stack)
print ">>>   hist_stack.GetName() = %s" % hist_stack.GetName()
print ">>>   hist_stack.GetTitle() = %s" % hist_stack.GetTitle()

print "\n>>> comparing integrals"
print ">>>   stack = %s" % hist_stack.Integral()
print ">>>   hist1 = %s" % hist1.Integral()
print ">>>   hist2 = %s" % hist2.Integral()

print "\n>>> comparing entries"
print ">>>   stack = %s" % hist_stack.GetEntries()
print ">>>   hist1 = %s" % hist1.GetEntries()
print ">>>   hist2 = %s" % hist2.GetEntries()

print "\n>>> comparing bin contents"
print ">>>   %3s %8s %8s %8s"%("bin","stack","hist1","hist2")
for i in xrange(hist1.GetNbinsX()+1):
    print ">>>   %3d %8.1f %8.1f %8.1f" %\
    (i,hist_stack.GetBinContent(i),hist1.GetBinContent(i),hist2.GetBinContent(i))

print "\n>>> comparing bin errors"
print ">>>   %3s %8s %8s %8s    %8s"%("bin","stack","hist1","hist2","sumw2 of hists")
for i in xrange(hist1.GetNbinsX()+1):
    e1 = hist1.GetBinError(i)
    e2 = hist2.GetBinError(i)
    e_sumw2 = sqrt(e1**2+e2**2)
    print ">>>   %3d %8.1f %8.1f %8.1f    %8.1f" %\
    (i,hist_stack.GetBinError(i),e1,e2,e_sumw2)

print