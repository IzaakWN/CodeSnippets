# ADDITION AND CONVOLUTION
# Options for plotting components of composite pdfs
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf205_compplot.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf205_compplot.C.html
#         https://github.com/clelange/roofit/blob/master/rf205_compplot.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen, kAzure, kCyan, kYellow, kDotted, kDashed
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussian, RooChebychev, RooExponential, RooAddPdf
from ROOT.RooFit import Title, LineColor, LineStyle, Range, Name, Invisible, Components



def rooFit205():
    
    print ">>> setup model signal components: gaussians..."
    x      = RooRealVar("x","x",0,10)
    mean   = RooRealVar("mean","mean of gaussians",5)
    sigma1 = RooRealVar("sigma1","width of gaussians",0.5) 
    sigma2 = RooRealVar("sigma2","width of gaussians",1)
    sig1   = RooGaussian("sig1","Signal component 1",x,mean,sigma1)
    sig2   = RooGaussian("sig2","Signal component 2",x,mean,sigma2)
    sig1frac = RooRealVar("sig1frac","fraction of component 1 in signal",0.8,0.,1.)
    sig      = RooAddPdf("sig","Signal",RooArgList(sig1,sig2),RooArgList(sig1frac))
    
    print ">>> setup model background components: Chebychev polynomial plus exponential..."
    a0    = RooRealVar("a0","a0",0.5,0.,1.)
    a1    = RooRealVar("a1","a1",-0.2,0.,1.)
    bkg1  = RooChebychev("bkg1","Background 1",x,RooArgList(a0,a1))
    alpha = RooRealVar("alpha","alpha",-1)
    bkg2  = RooExponential("bkg2","Background 2",x,alpha)
    bkg1frac = RooRealVar("bkg1frac","fraction of component 1 in background",0.2,0.,1.)
    bkg      = RooAddPdf("bkg","Signal",RooArgList(bkg1,bkg2),RooArgList(bkg1frac))
    
    print ">>> sum signal and background component..."
    bkgfrac = RooRealVar("bkgfrac","fraction of background",0.5,0.,1.)
    model   = RooAddPdf("model","g1+g2+a",RooArgList(bkg,sig),RooArgList(bkgfrac))
    
    print ">>> setup basic plot with data and full pdf..."
    data   = model.generate(RooArgSet(x),1000) # RooDataSet
    frame1 = x.frame(Title("Component plotting of pdf=(sig1+sig2)+(bkg1+bkg2)")) # RooPlot
    data.plotOn(frame1, Name("data"))
    model.plotOn(frame1,Name("model"))
    
    print ">>> clone frame for reuse..."
    frame2 = frame1.Clone("frame2") # RooPlot
    frame2.SetTitle("Get components with regular expressions")
    
    print ">>> make omponent by object reference..."
    # Plot multiple background components specified by object reference
    # Note that specified components may occur at any level in object tree
    # (e.g bkg is component of 'model' and 'sig2' is component 'sig')
    argset1 = RooArgSet(bkg)
    argset2 = RooArgSet(bkg2)
    argset3 = RooArgSet(bkg,sig2)
    model.plotOn(frame1,Components(argset1),LineColor(kRed),                   Name("bkgs1"))
    model.plotOn(frame1,Components(argset2),LineStyle(kDashed),LineColor(kRed),Name("bkg2")) 
    model.plotOn(frame1,Components(argset3),LineStyle(kDotted),                Name("bkgssig21"))
    
    
    
    print "\n>>> make component by name / regular expressions..."
    model.plotOn(frame2,Components("bkg"),      LineColor(kAzure-4),                   Name("bkgs2"))     # by name
    model.plotOn(frame2,Components("bkg1,sig2"),LineColor(kAzure-4),LineStyle(kDotted),Name("bkg1sig22")) # by name
    model.plotOn(frame2,Components("sig*"),     LineColor(kAzure-4),LineStyle(kDashed),Name("sigs2"))     # with regexp (wildcard *)
    model.plotOn(frame2,Components("bkg1,sig*"),LineColor(kYellow), LineStyle(kDashed),Name("bkg1sigs2"))  # with regexp (,) #Invisible()
    
    
    
    print "\n>>> draw pfds and fits on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,1400,600)
    legend1 = TLegend(0.22,0.85,0.4,0.65)
    legend2 = TLegend(0.22,0.85,0.4,0.65)
    for legend in [legend1,legend2]:
        legend.SetTextSize(0.032)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
    canvas.Divide(2)
    canvas.cd(1)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    frame1.GetYaxis().SetLabelOffset(0.008)
    frame1.GetYaxis().SetTitleOffset(1.6)
    frame1.GetYaxis().SetTitleSize(0.045)
    frame1.GetXaxis().SetTitleSize(0.045)
    frame1.Draw()
    legend1.AddEntry("data",     "data",    'LEP')
    legend1.AddEntry("model",    "model",   'L')
    legend1.AddEntry("bkgs1",    "bkg",     'L')
    legend1.AddEntry("bkg2",     "bkg2",    'L')
    legend1.AddEntry("bkgssig21","bkg,sig2",'L')
    legend1.Draw()
    canvas.cd(2)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    frame2.GetYaxis().SetLabelOffset(0.008)
    frame2.GetYaxis().SetTitleOffset(1.6)
    frame2.GetYaxis().SetTitleSize(0.045)
    frame2.GetXaxis().SetTitleSize(0.045)
    frame2.Draw()
    legend2.AddEntry("data",    "data", 'LEP')
    legend2.AddEntry("model",   "model",'L')
    legend2.AddEntry("bkgs2",    "\"bkg\"",      'L')
    legend2.AddEntry("bkg1sig22","\"bkg1,sig2\"",'L')
    legend2.AddEntry("sigs2",    "\"sig*\"",     'L')
    legend2.AddEntry("bkg1sigs2","\"bkg1,sig*\"",'L')
    legend2.Draw()
    canvas.SaveAs("rooFit205.png")
    


if __name__ == '__main__':
    rooFit205()
    print ">>>\n>>> Done.\n"
    

