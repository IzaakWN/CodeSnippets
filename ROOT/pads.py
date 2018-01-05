from ROOT import TCanvas, TPad, gDirectory, gPad
import ROOT

def printTPad(canvas):
    print "\n>>> canvas.cd(1)"
    pad = canvas.cd(1)
    print ">>> canvas.cd(1).GetName() = %s" % (pad.GetName())
    print ">>> gPad.GetName() = %s" % (gPad.GetName())

    print "\n>>> canvas.cd(2)"
    pad = canvas.cd(2)
    print ">>> canvas.cd(2).GetName() = %s" % (pad.GetName())
    print ">>> gPad.GetName() = %s" % (gPad.GetName())

def addTPads(canvas):
    print "\n>>> gPad.GetName() = %s" % (gPad.GetName())
    print ">>> canvas.ls()"
    canvas.ls()
    pad1 = TPad("pad1","pad1", 0, 0.33, 1, 0.95)
    pad2 = TPad("pad2","pad2", 0, 0.05, 1, 0.30)
    pad1.Draw()
    pad2.Draw()
    ROOT.SetOwnership(pad1, False)
    ROOT.SetOwnership(pad2, False)
    print "\n>>> gPad.GetName() = %s" % (gPad.GetName())
    print ">>> canvas.ls()"
    canvas.ls()
    printTPad(canvas)

canvas = TCanvas("canvas","canvas",100,100,800,600)
addTPads(canvas)

print "\n>>> gPad.GetName() = %s" % (gPad.GetName())
print ">>> canvas.ls()"
canvas.ls()

printTPad(canvas)

print