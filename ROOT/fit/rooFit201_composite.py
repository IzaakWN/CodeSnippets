# ADDITION AND CONVOLUTION
# Composite p.d.f with signal and background component
#
#   pdf = f_bkg * bkg(x,a0,a1) + (1-fbkg) * (f_sig1 * sig1(x,m,s1 + (1-f_sig1) * sig2(x,m,s2)))
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf201_composite.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf201_composite.C.html
#         https://github.com/clelange/roofit/blob/master/rf201_composite.py
#
# See also RooFit chapter 3 "Signal and Background - Composite models"
#         https://root.cern.ch/download/doc/RooFit_Users_Manual_2.91-33.pdf

import ROOT
from ROOT import gPad, TCanvas, TLegend,\
                 kBlue, kRed, kGreen, kOrange, kMagenta, kPink, kAzure, kDashed, kDotted, kDashDotted, kTRUE, kFALSE
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussian, RooChebychev, RooAddPdf
from ROOT.RooFit import Title, LineColor, LineStyle, LineWidth, Range, Name, Components, Binning



def rooFit201():
    
    print ">>> setup model component: gaussian signals and Chebychev polynomial background..."
    x      = RooRealVar("x","x",0,11)
    mean   = RooRealVar("mean","mean of gaussians",5)
    sigma1 = RooRealVar("sigma1","width of gaussians",0.5)
    sigma2 = RooRealVar("sigma2","width of gaussians",1)
    sig1   = RooGaussian("sig1","Signal component 1",x,mean,sigma1)
    sig2   = RooGaussian("sig2","Signal component 2",x,mean,sigma2)
    
    a0  = RooRealVar("a0","a0",0.5,0.,1.)
    a1  = RooRealVar("a1","a1",-0.2,0.,1.)
    bkg = RooChebychev("bkg","Background",x,RooArgList(a0,a1))
    
    
    
    print ">>>\n>>> METHOD 1 - Two RooAddPdfs"
    print ">>> add signal components..."
    # Sum the signal components into a composite signal p.d.f.
    sig1frac = RooRealVar("sig1frac","fraction of component 1 in signal",0.8,0.,1.)
    sig      = RooAddPdf("sig","Signal",RooArgList(sig1,sig2),RooArgList(sig1frac))
    
    print ">>> add signal and background..."
    # Sum the composite signal and background
    bkgfrac = RooRealVar("bkgfrac","fraction of background",0.5,0.,1.)
    model   = RooAddPdf("model","g1+g2+a",RooArgList(bkg,sig),RooArgList(bkgfrac))
    
    print ">>> sample, fit and plot model..."
    data = model.generate(RooArgSet(x),1000) # RooDataSet
    model.fitTo(data)
    frame1 = x.frame(Title("Example of composite pdf=(sig1+sig2)+bkg")) # RooPlot
    data.plotOn(frame1,Binning(50),Name("data"))
    model.plotOn(frame1,Name("model"))
    
    # Overlay the background component of model with a dashed line
    argset1 = RooArgSet(bkg)
    model.plotOn(frame1,Components(argset1),LineWidth(2),Name("bkg")) #,LineStyle(kDashed)
    
    # Overlay the background+sig2 components of model with a dotted line
    argset2 = RooArgSet(bkg,sig2)
    model.plotOn(frame1,Components(argset2),LineWidth(2),LineStyle(kDashed),LineColor(kAzure-4),Name("bkgsig2")) #,LineStyle(kDotted)
    
    print "\n>>> structure of composite pdf:"
    model.Print("t") # "tree" mode
    
    print "\n>>> parameters:"
    params = model.getVariables() # RooArgSet
    params.Print("v")
    params.Print()
    
    print "\n>>> params.find(\"...\").getVal():"
    print ">>>   sigma1  = %.2f"   % params.find("sigma1").getVal()
    print ">>>   sigma2  = %.2f"   % params.find("sigma2").getVal()
    print ">>>   bkgfrac = %5.2f"  % params.find("bkgfrac").getVal()
    print ">>>   sig1frac = %5.2f" % params.find("sig1frac").getVal()
    
    print ">>>\n>>> components:"
    comps   = model.getComponents() # RooArgSet
    sig     = comps.find("sig")     # RooAbsArg
    sigVars = sig.getVariables()    # RooArgSet
    sigVars.Print()
    
    
    
    print ">>>\n>>> METHOD 2 - One RooAddPdf with recursive fractions"
    # Construct sum of models on one go using recursive fraction interpretations
    #   model2 = bkg + (sig1 + sig2)
    model2 = RooAddPdf("model","g1+g2+a",RooArgList(bkg,sig1,sig2),RooArgList(bkgfrac,sig1frac),kTRUE)
    
    # NB: Each coefficient is interpreted as the fraction of the
    # left-hand component of the i-th recursive sum, i.e.
    #   sum4 = A + ( B + ( C + D ) )
    # with fraction fA, fB and fC expands to
    #   sum4 = fA*A + (1-fA)*(fB*B + (1-fB)*(fC*C + (1-fC)*D))
    
    print ">>> plot recursive addition model..."
    argset3 = RooArgSet(bkg,sig2)
    model2.plotOn(frame1,LineColor(kRed),LineStyle(kDashDotted),LineWidth(3),Name("model2"))
    model2.plotOn(frame1,Components(argset3),LineColor(kMagenta),LineStyle(kDashDotted),LineWidth(3),Name("bkgsig22"))
    model2.Print("t")
    
    
    
    print ">>> draw pdfs and fits on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,800,600)
    legend = TLegend(0.57,0.87,0.95,0.65)
    legend.SetTextSize(0.030)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    gPad.SetLeftMargin(0.14); gPad.SetRightMargin(0.02)
    frame1.GetYaxis().SetLabelOffset(0.008)
    frame1.GetYaxis().SetTitleOffset(1.4)
    frame1.GetYaxis().SetTitleSize(0.045)
    frame1.GetXaxis().SetTitleSize(0.045)
    frame1.Draw()
    legend.AddEntry("data",    "data",                            'LEP')
    legend.AddEntry("model",   "composite model",                 'L')
    legend.AddEntry("model2",  "composite model (method 2)",      'L')
    legend.AddEntry("bkg",     "background only",                 'L')
    legend.AddEntry("bkgsig2", "background + signal 2",           'L')
    legend.AddEntry("bkgsig22","background + signal 2 (method 2)",'L')
    legend.Draw()
    canvas.SaveAs("rooFit201.png")
    


if __name__ == '__main__':
    rooFit201()
    print ">>>\n>>> Done.\n"
    

